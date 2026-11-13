"""
PSX Parser - Production-grade parser with AST integration
Supports full PSX capability with modern architecture

Changes from previous version
──────────────────────────────
* Replaced SIGALRM timeout (Unix-only) with monotonic-clock deadlines.
* All tag forms (elements, components, fragments) go through the same
  recursive-descent engine — no regex fallback for components.
* _match_brace() counts delimiters properly so nested expressions like
  {obj['key']}, {fn({'a': 1})}, and template literals never truncate early.
* Thread-safe: state lives on the call stack; a threading.local pool
  provides one PSXParser instance per thread — no shared mutable state.
* _attrs() returns an is_self_closing flag instead of relying on
  post-hoc index arithmetic.
* _children() breaks on any unexpected closing tag to prevent the
  stuck-parser increment from corrupting the position.
* All print() debug statements replaced with logging calls.
* Dead code (_parse_element_fallback, unused regex patterns) removed.
* Type hint for _node_to_child corrected to include List as a possible
  return type (Fragment case).

Additional Fixes Applied:
* Removed the hardcoded `_RAW_CODE:` prefix for the `code` attribute.
* Added proper string escaping (`\"` and `\'`) in attributes so inline
  JS doesn't break the parser.
* Added an interceptor for inline JavaScript in `{}` blocks so the
  parser doesn't try to evaluate JS as Python expressions.
"""

import re
import html as _html
import time
import logging
import threading
from typing import Any, Dict, List, Optional, Tuple, Union

from dataclasses import dataclass, field

from .ast_nodes import (
    PSXNode, PSXNodeUnion,
    ElementNode, TextNode, ExpressionNode,
    ComponentNode, FragmentNode,
    PSXASTParser, PSXNodeValidator, PSXNodeOptimizer,
)
from .runtime import PSXRuntime, process_python_logic

log = logging.getLogger(__name__)

# ── Module-level constants ─────────────────────────────────────────────────────

#: HTML void elements + common SVG leaf elements that never have children.
SELF_CLOSING_TAGS: frozenset = frozenset({
    'area', 'base', 'br', 'col', 'command', 'embed', 'hr', 'img', 'input',
    'keygen', 'link', 'meta', 'menuitem', 'param', 'source', 'track', 'wbr',
    'circle', 'ellipse', 'line', 'path', 'polygon', 'polyline', 'rect',
})

#: Default wall-clock budget for a single parse call (seconds).
PARSE_TIMEOUT: float = 5.0

#: Hard iteration cap per parse to guard against pathological inputs.
MAX_ITERATIONS: int = 10_000

#: Keywords that indicate inline JavaScript rather than Python expressions
_JS_KEYWORDS = (
    '=>', 'function', 'return ', 'this.', 'document.', 'window.', 
    'console.', 'var ', 'let ', 'const ', '.classList', 'querySelector', 
    'getElementById', 'addEventListener'
)
_CTRL_KW = ('if ', 'for ', 'while ', 'try', 'elif ', 'else', 'def ', 'class ', 'import ', 'from ')


# ── Internal exception ─────────────────────────────────────────────────────────

class _ParseTimeout(Exception):
    """Raised when a parse call exceeds its time budget."""


# ── Expression boundary helper ─────────────────────────────────────────────────

def _match_brace(code: str, start: int) -> int:
    """
    Given that ``code[start] == '{'``, return the *exclusive* end index
    after the matching ``'}'``.
    """
    assert code[start] == '{', f"Expected '{{' at index {start}, got {code[start]!r}"
    depth: int = 0
    i: int = start
    n: int = len(code)
    in_str: Optional[str] = None

    while i < n:
        ch = code[i]
        if in_str:
            if ch == '\\':
                i += 2          # skip escaped character
                continue
            if ch == in_str:
                in_str = None
        else:
            if ch in ('"', "'", '`'):
                in_str = ch
            elif ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    return i + 1
        i += 1

    return n   # malformed — caller handles gracefully


def _position(code: str, index: int) -> Tuple[int, int]:
    """Return 1-based (line, column) of ``index`` within ``code``."""
    line = code.count('\n', 0, index) + 1
    last_nl = code.rfind('\n', 0, index)
    return line, index - last_nl


# ── PSXElement (legacy shim) ───────────────────────────────────────────────────

@dataclass
class PSXElement:
    """
    Legacy PSX element, retained for backwards compatibility.
    """
    tag:      str
    props:    Dict[str, Any]                  = field(default_factory=dict)
    children: List[Union[str, 'PSXElement']]  = field(default_factory=list)
    key:      Optional[str]                   = None

    def to_ast(self) -> ElementNode:
        events:     Dict[str, Any] = {}
        attributes: Dict[str, Any] = {}

        for k, v in self.props.items():
            if k.startswith('on') and callable(v):
                events[k] = v.__name__
            else:
                attributes[k] = v

        ast_children: List[PSXNode] = []
        for child in self.children:
            if isinstance(child, str):
                ast_children.append(TextNode(content=child))
            elif isinstance(child, PSXElement):
                ast_children.append(child.to_ast())
            elif isinstance(child, PSXNode):
                ast_children.append(child)

        return ElementNode(
            tag=self.tag,
            attributes=attributes,
            events=events,
            children=ast_children,
            key=self.key,
            self_closing=self.tag in SELF_CLOSING_TAGS,
        )

    def to_html(self, context: Dict[str, Any] = None) -> str:
        ctx: Dict[str, Any] = {}
        stored_ctx = getattr(self, '_psx_context', None)
        if stored_ctx:
            ctx = dict(stored_ctx)
            if '_lambda_handlers' not in ctx:
                ctx['_lambda_handlers'] = {}
                if stored_ctx is not None:
                    stored_ctx['_lambda_handlers'] = ctx['_lambda_handlers']
        if context:
            ctx.update(context)

        runtime = PSXRuntime(ctx)

        ast_node = getattr(self, '_ast_node', None)
        if ast_node is not None:
            return runtime._render_node(ast_node)

        return runtime._render_node(self.to_ast())


# ── AST → PSXElement converters ────────────────────────────────────────────────

def _node_to_child(
    node: PSXNodeUnion,
    context: Dict[str, Any],
) -> Union[str, PSXElement, List[Union[str, 'PSXElement']]]:
    if isinstance(node, TextNode):
        return node.content

    if isinstance(node, ExpressionNode):
        try:
            result = PSXRuntime(context).evaluate_ast_expression(node)
            if isinstance(result, PSXElement):
                return result
            return result.to_html() if hasattr(result, 'to_html') else str(result)
        except Exception:
            return node.expression

    if isinstance(node, (ElementNode, ComponentNode)):
        tag = node.tag  if isinstance(node, ElementNode) else node.name
        raw = node.attributes if isinstance(node, ElementNode) else node.props
        key = getattr(node, 'key', None)
        kids = _children_to_elements(node.children, context)
        el = PSXElement(
            tag=tag,
            props={**raw, **({'key': key} if key else {})},
            children=kids,
        )
        el._ast_node    = node       # type: ignore[attr-defined]
        el._psx_context = context    # type: ignore[attr-defined]
        return el

    if isinstance(node, FragmentNode):
        return _children_to_elements(node.children, context)

    return str(node)


def _children_to_elements(
    nodes: List[PSXNodeUnion],
    context: Dict[str, Any],
) -> List[Union[str, PSXElement]]:
    out: List[Union[str, PSXElement]] = []
    for node in nodes:
        converted = _node_to_child(node, context)
        if isinstance(converted, list):
            out.extend(converted)
        else:
            out.append(converted)
    return out


# ── Parser ─────────────────────────────────────────────────────────────────────

class PSXParser:
    def __init__(self) -> None:
        self.ast_parser = PSXASTParser()
        self.validator  = PSXNodeValidator()
        self.optimizer  = PSXNodeOptimizer()

    def parse_psx(
        self,
        psx_str: str,
        context: Dict[str, Any] = None,
        timeout: float = PARSE_TIMEOUT,
    ) -> PSXNodeUnion:
        context  = context or {}
        psx_str  = process_python_logic(psx_str, context, substitute_expressions=False)
        src      = psx_str.strip()
        deadline = time.monotonic() + timeout

        try:
            node = self._root(src, context, deadline)
        except _ParseTimeout:
            log.warning("PSX parse timeout  src=%.120s…", src)
            return TextNode(content=psx_str)
        except Exception:
            log.error("PSX parse error  src=%.120s…", src, exc_info=True)
            return TextNode(content=psx_str)

        return self.optimizer.optimize_node(node)

    def _root(
        self,
        src: str,
        ctx: Dict[str, Any],
        dl: float,
    ) -> PSXNodeUnion:
        if not src:
            return TextNode(content='')

        if src.startswith('<>'):
            node, _ = self._parse_fragment_short(src, 0, ctx, dl, False)
            return node

        if src.startswith('<'):
            node, _ = self._dispatch(src, 0, ctx, dl, False)
            return node

        return TextNode(content=src)

    def _dispatch(
        self,
        code: str,
        index: int,
        ctx: Dict[str, Any],
        dl: float,
        in_pre_tag: bool = False,
    ) -> Tuple[PSXNodeUnion, int]:
        self._tick(dl)
        assert code[index] == '<'

        peek = index + 1
        tag_start = peek
        n = len(code)
        while peek < n and (code[peek].isalnum() or code[peek] in '-_:.'):
            peek += 1
        tag = code[tag_start:peek]

        if not tag:
            return TextNode(content='<'), index + 1

        if tag[0].isupper():
            return self._parse_component(code, index, ctx, dl, in_pre_tag)

        if tag.lower() == 'fragment':
            el, new_i = self._parse_element(code, index, ctx, dl, in_pre_tag)
            return FragmentNode(children=el.children, shorthand=False), new_i

        return self._parse_element(code, index, ctx, dl, in_pre_tag)

    def _parse_fragment_short(
        self,
        code: str,
        index: int,
        ctx: Dict[str, Any],
        dl: float,
        in_pre_tag: bool = False,
    ) -> Tuple[FragmentNode, int]:
        index += 2
        children, index = self._parse_children(code, index, '</>', ctx, dl, in_pre_tag)
        if code.startswith('</>', index):
            index += 3
        return FragmentNode(children=children, shorthand=True), index

    def _parse_element(
        self,
        code: str,
        index: int,
        ctx: Dict[str, Any],
        dl: float,
        in_pre_tag: bool = False,
    ) -> Tuple[ElementNode, int]:
        self._tick(dl)
        pos = _position(code, index)
        index += 1

        tag, index = self._read_tag_name(code, index)
        tag = tag or 'div'

        attrs, events, spread, self_closing, index = self._read_attrs(
            code, index, ctx, tag
        )

        if not self_closing and tag.lower() in SELF_CLOSING_TAGS:
            self_closing = True

        is_pre_tag = tag.lower() == 'pre'

        if self_closing:
            return ElementNode(
                tag=tag,
                attributes=attrs,
                events=events,
                children=[],
                self_closing=True,
                spread_props=spread,
                position=pos,
            ), index

        closing = f'</{tag}>'
        children, index = self._parse_children(code, index, closing, ctx, dl, is_pre_tag or in_pre_tag)
        if code.startswith(closing, index):
            index += len(closing)

        return ElementNode(
            tag=tag,
            attributes=attrs,
            events=events,
            children=children,
            spread_props=spread,
            position=pos,
        ), index

    def _parse_component(
        self,
        code: str,
        index: int,
        ctx: Dict[str, Any],
        dl: float,
        in_pre_tag: bool = False,
    ) -> Tuple[ComponentNode, int]:
        self._tick(dl)
        pos = _position(code, index)
        index += 1

        name, index = self._read_tag_name(code, index)
        props, events, spread, self_closing, index = self._read_attrs(
            code, index, ctx, name
        )

        if self_closing:
            return ComponentNode(
                name=name,
                props=props,
                events=events,
                children=[],
                spread_props=spread,
                position=pos,
            ), index

        closing = f'</{name}>'
        children, index = self._parse_children(code, index, closing, ctx, dl, in_pre_tag)
        if code.startswith(closing, index):
            index += len(closing)

        return ComponentNode(
            name=name,
            props=props,
            events=events,
            children=children,
            spread_props=spread,
            position=pos,
        ), index

    def _parse_children(
        self,
        code: str,
        index: int,
        sentinel: str,
        ctx: Dict[str, Any],
        dl: float,
        in_pre_tag: bool = False,
    ) -> Tuple[List[PSXNodeUnion], int]:
        nodes: List[PSXNodeUnion] = []
        n     = len(code)
        iters = 0

        while index < n:
            self._tick(dl)
            iters += 1
            if iters > MAX_ITERATIONS:
                log.warning(
                    "MAX_ITERATIONS (%d) hit while parsing children; "
                    "sentinel=%r  position=%d",
                    MAX_ITERATIONS, sentinel, index,
                )
                break

            while index < n and code[index] in ' \t\n\r':
                index += 1
            if index >= n:
                break

            if code.startswith(sentinel, index):
                break

            if code[index:index + 2] == '</':
                log.debug(
                    "Unexpected closing tag at %d while looking for %r; "
                    "stopping children parse",
                    index, sentinel,
                )
                break

            node, new_index = self._parse_child(code, index, ctx, dl, in_pre_tag)

            if new_index <= index:
                log.warning(
                    "Parser made no progress at index %d (tag sentinel=%r); "
                    "skipping one character to continue",
                    index, sentinel,
                )
                index += 1
                continue

            index = new_index

            if node is None:
                continue

            if isinstance(node, TextNode):
                node.content = process_python_logic(node.content, ctx)

            nodes.append(node)

        return nodes, index

    def _parse_child(
        self,
        code: str,
        index: int,
        ctx: Dict[str, Any],
        dl: float,
        in_pre_tag: bool = False,
    ) -> Tuple[Optional[PSXNodeUnion], int]:
        n = len(code)

        while index < n and code[index] in ' \t\n\r':
            index += 1
        if index >= n:
            return None, index

        ch = code[index]

        if ch == '<':
            if code.startswith('<!--', index):
                end = code.find('-->', index)
                return None, (end + 3 if end != -1 else n)

            if code.startswith('<>', index):
                return self._parse_fragment_short(code, index, ctx, dl, in_pre_tag)

            return self._dispatch(code, index, ctx, dl, in_pre_tag)

        # ── Expression ─────────────────────────────────────────────────────
        if ch == '{' and not in_pre_tag:
            end  = _match_brace(code, index)
            expr = code[index + 1 : end - 1].strip()
            if expr:
                # [FIX] Intercept inline JavaScript so it is treated as literal text
                if any(expr.startswith(k) for k in _CTRL_KW) or any(k in expr for k in _JS_KEYWORDS):
                    return TextNode(content=code[index:end]), end
                    
            pexpr = self.ast_parser.parse_expression(expr)
            return ExpressionNode(expression=expr, parsed_expression=pexpr,
                                  position=_position(code, index)), end

        # ── Text ───────────────────────────────────────────────────────────
        start = index
        stop_chars = ('<',) if in_pre_tag else ('<', '{')
        while index < n and code[index] not in stop_chars:
            index += 1
        raw = code[start:index]
        
        if in_pre_tag:
            return TextNode(content=raw), index
        
        parts = self._split_text_with_exprs(raw)
        if not parts:
            return None, index
        if len(parts) == 1:
            return parts[0], index
        return FragmentNode(children=parts, shorthand=True), index

    def _read_tag_name(self, code: str, index: int) -> Tuple[str, int]:
        n = len(code)
        start = index
        while index < n and (code[index].isalnum() or code[index] in '-_:.'):
            index += 1
        return code[start:index], index

    def _read_attrs(
        self,
        code:  str,
        index: int,
        ctx:   Dict[str, Any],
        tag:   str,
    ) -> Tuple[Dict[str, Any], Dict[str, Any], List[str], bool, int]:
        attributes: Dict[str, Any] = {}
        events:     Dict[str, Any] = {}
        spread:     List[str]      = []
        n = len(code)

        while index < n and code[index] not in ('>', '/'):
            while index < n and code[index].isspace():
                index += 1
            if index >= n or code[index] in ('>', '/'):
                break

            if code[index] == '{':
                end  = _match_brace(code, index)
                expr = code[index + 1 : end - 1].strip()
                if expr.startswith('...'):
                    spread.append(expr[3:])
                index = end
                continue

            ks = index
            while index < n and (code[index].isalnum() or code[index] in '-_:.'):
                index += 1
            key = code[ks:index]

            if not key:
                index += 1
                continue

            while index < n and code[index].isspace():
                index += 1

            if index >= n or code[index] != '=':
                attributes[key] = True
                continue

            index += 1
            while index < n and code[index].isspace():
                index += 1

            if index >= n:
                attributes[key] = True
                continue

            # ── Value ───────────────────────────────────────────────────
            is_expr_value = False
            if code[index] == '{':
                end   = _match_brace(code, index)
                value: Any = code[index:end]
                is_expr_value = True
                index = end

            elif code[index] in ('"', "'"):
                q     = code[index]
                index += 1
                vs    = index
                
                # [FIX] Handle escaped quotes so inline JS doesn't break strings
                while index < n:
                    if code[index] == '\\':
                        index += 2  # skip escaped character
                        continue
                    if code[index] == q:
                        break
                    index += 1
                    
                value = code[vs:index]
                if index < n:
                    index += 1   # consume closing quote

            else:
                vs = index
                while index < n and not code[index].isspace() and code[index] not in ('>', '/'):
                    index += 1
                value = code[vs:index]

            # Quoted/bare attribute values are HTML — decode entities once
            # here so the renderer can escape exactly once on emit. Unquoted
            # {expr} values above are code, not HTML, and are left untouched
            # (a quoted "{...}" string is still an HTML value, e.g. the JSON
            # payload of data-psx-motion).
            if not is_expr_value:
                value = _html.unescape(value)

            # ── Categorise ──────────────────────────────────────────────
            if key == 'bind':
                raw_var = (
                    value[1:-1].strip()
                    if isinstance(value, str)
                       and value.startswith('{')
                       and value.endswith('}')
                    else value
                )
                attributes['_bind_target'] = raw_var
                attributes['_bind_type'] = (
                    'checked'
                    if tag.lower() == 'input' and attributes.get('type') == 'checkbox'
                    else 'value'
                )

            elif key == 'ref':
                # ref={name} / ref="name" → data-psx-ref so the client runtime
                # can register the DOM node for useRef/getRef lookups.
                raw = value
                if isinstance(raw, str) and raw.startswith('{') and raw.endswith('}'):
                    raw = raw[1:-1].strip()
                if isinstance(raw, str) and len(raw) >= 2 and raw[0] in ('"', "'") and raw[-1] == raw[0]:
                    raw = raw[1:-1]
                attributes['_psx_ref'] = raw

            elif key.startswith('on'):
                events[key] = value

            else:
                attributes[key] = value

        # ── Consume closing '>' or '/>' ─────────────────────────────────
        is_self_closing = False
        if index < n:
            if code[index:index + 2] == '/>':
                is_self_closing = True
                index += 2
            elif code[index] == '>':
                index += 1

        return attributes, events, spread, is_self_closing, index

    def _split_text_with_exprs(self, text: str) -> List[PSXNodeUnion]:
        nodes: List[PSXNodeUnion] = []
        buf:   List[str]          = []
        i = 0
        n = len(text)

        while i < n:
            if text[i] == '{':
                if buf:
                    nodes.append(TextNode(content=''.join(buf)))
                    buf = []
                end  = _match_brace(text, i)
                expr = text[i + 1 : end - 1].strip()
                if expr:
                    # [FIX] Intercept inline JS for text segments
                    if any(expr.startswith(k) for k in _CTRL_KW) or any(k in expr for k in _JS_KEYWORDS):
                        nodes.append(TextNode(content=text[i:end]))
                        i = end
                        continue
                        
                    pexpr = self.ast_parser.parse_expression(expr)
                    nodes.append(ExpressionNode(expression=expr, parsed_expression=pexpr))
                i = end
            else:
                buf.append(text[i])
                i += 1

        if buf:
            content = ''.join(buf)
            if content.strip():
                nodes.append(TextNode(content=content))

        return nodes

    @staticmethod
    def _tick(deadline: float) -> None:
        if time.monotonic() > deadline:
            raise _ParseTimeout()


# ── Thread-local parser pool ───────────────────────────────────────────────────

_tls = threading.local()


def _get_parser() -> PSXParser:
    if not hasattr(_tls, 'parser'):
        _tls.parser = PSXParser()
    return _tls.parser


# ── Public API ─────────────────────────────────────────────────────────────────

def psx(psx_str: str, context: Dict[str, Any] = None) -> PSXElement:
    import inspect

    if context is None:
        captured: Dict[str, Any] = {}
        try:
            frame = inspect.currentframe().f_back
            if frame:
                captured = {
                    k: v
                    for k, v in frame.f_locals.items()
                    if (
                        not k.startswith('_')
                        and not callable(v)
                        and not isinstance(v, type)
                    )
                }
        except Exception:
            pass
        merged: Dict[str, Any] = captured
    else:
        merged = dict(context)

    ast_node = _get_parser().parse_psx(psx_str, merged)

    if isinstance(ast_node, ElementNode):
        el = PSXElement(
            tag=ast_node.tag,
            props=ast_node.attributes,
            children=_children_to_elements(ast_node.children, merged),
            key=ast_node.key,
        )
        el._ast_node    = ast_node   # type: ignore[attr-defined]
        el._psx_context = merged     # type: ignore[attr-defined]
        return el

    if isinstance(ast_node, FragmentNode):
        kids = _children_to_elements(ast_node.children, merged)
    else:
        c    = _node_to_child(ast_node, merged)
        kids = c if isinstance(c, list) else [c]

    el = PSXElement(
        tag='div',
        props={},
        children=kids,
        key=getattr(ast_node, 'key', None),
    )
    el._ast_node    = ast_node   # type: ignore[attr-defined]
    el._psx_context = merged     # type: ignore[attr-defined]
    return el


def render_psx(element: Any, context: Dict[str, Any] = None) -> str:
    if isinstance(element, PSXElement):
        return element.to_html(context)
    return str(element)


def fragment(children: Any) -> str:
    if isinstance(children, list):
        return ''.join(str(c) for c in children)
    return str(children)


def key(key_value: str, element: PSXElement) -> PSXElement:
    element.key = key_value
    return element


__all__ = [
    'PSXElement', 'PSXParser', 'psx', 'render_psx', 'fragment', 'key',
    'process_python_logic',
    'PSXASTParser', 'PSXNodeValidator', 'PSXNodeOptimizer',
]