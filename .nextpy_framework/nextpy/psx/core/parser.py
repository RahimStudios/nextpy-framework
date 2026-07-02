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
"""

import re
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


# ── Internal exception ─────────────────────────────────────────────────────────

class _ParseTimeout(Exception):
    """Raised when a parse call exceeds its time budget."""


# ── Expression boundary helper ─────────────────────────────────────────────────

def _match_brace(code: str, start: int) -> int:
    """
    Given that ``code[start] == '{'``, return the *exclusive* end index
    after the matching ``'}'``.

    Handles:
    * Arbitrarily nested ``{}`` blocks.
    * Single-quoted, double-quoted, and back-tick string literals
      (including escaped characters inside them).

    Returns ``len(code)`` for malformed input so callers degrade gracefully.
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


# ── PSXElement (legacy shim) ───────────────────────────────────────────────────

@dataclass
class PSXElement:
    """
    Legacy PSX element, retained for backwards compatibility.

    ``_ast_node`` and ``_psx_context`` are set externally after construction
    (they carry information needed for rendering but are not part of the
    public API surface).
    """
    tag:      str
    props:    Dict[str, Any]                  = field(default_factory=dict)
    children: List[Union[str, 'PSXElement']]  = field(default_factory=list)
    key:      Optional[str]                   = None

    def to_ast(self) -> ElementNode:
        """Convert this PSXElement into a production-grade :class:`ElementNode`."""
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
        """Render this element to an HTML string."""
        ctx: Dict[str, Any] = {}
        stored_ctx = getattr(self, '_psx_context', None)
        if stored_ctx:
            ctx = dict(stored_ctx)
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
    """
    Convert one AST node to its ``PSXElement``-child equivalent.

    :class:`FragmentNode` flattens into a plain list so callers must handle
    both scalar and list return values (see :func:`_children_to_elements`).
    """
    if isinstance(node, TextNode):
        return node.content

    if isinstance(node, ExpressionNode):
        try:
            result = PSXRuntime(context).evaluate_ast_expression(node)
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
        # Fragments flatten — callers must extend, not append
        return _children_to_elements(node.children, context)

    return str(node)


def _children_to_elements(
    nodes: List[PSXNodeUnion],
    context: Dict[str, Any],
) -> List[Union[str, PSXElement]]:
    """Recursively convert a list of AST children to ``PSXElement`` children."""
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
    """
    Production-grade PSX parser using recursive descent.

    Design properties
    -----------------
    * **Thread-safe** — all mutable state lives on the call stack.
      The only instance-level state is the stateless helper objects
      (``ast_parser``, ``validator``, ``optimizer``).
    * **Cross-platform** — deadline tracking uses ``time.monotonic()``;
      no UNIX signals.
    * **Unified dispatch** — components go through the same recursive
      engine as elements; no regex short-cut that breaks on nesting.
    * **Robust expressions** — ``_match_brace`` handles arbitrarily
      nested braces so ``{obj['key']}`` and ``{fn({'a': 1})}`` parse
      correctly.
    """

    def __init__(self) -> None:
        self.ast_parser = PSXASTParser()
        self.validator  = PSXNodeValidator()
        self.optimizer  = PSXNodeOptimizer()

    # ── Public API ─────────────────────────────────────────────────────────────

    def parse_psx(
        self,
        psx_str: str,
        context: Dict[str, Any] = None,
        timeout: float = PARSE_TIMEOUT,
    ) -> PSXNodeUnion:
        """
        Parse *psx_str* and return an optimised AST node.

        Falls back to a plain :class:`TextNode` on timeout or parse error
        so callers always receive a usable value.
        """
        context  = context or {}
        psx_str  = process_python_logic(psx_str, context)
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

    # ── Root dispatch ──────────────────────────────────────────────────────────

    def _root(
        self,
        src: str,
        ctx: Dict[str, Any],
        dl: float,
    ) -> PSXNodeUnion:
        """Select the right top-level parser for *src*."""
        if not src:
            return TextNode(content='')

        if src.startswith('<>'):
            node, _ = self._parse_fragment_short(src, 0, ctx, dl, False)
            return node

        if src.startswith('<'):
            node, _ = self._dispatch(src, 0, ctx, dl, False)
            return node

        return TextNode(content=src)

    # ── Tag-level dispatcher ───────────────────────────────────────────────────

    def _dispatch(
        self,
        code: str,
        index: int,
        ctx: Dict[str, Any],
        dl: float,
        in_pre_tag: bool = False,
    ) -> Tuple[PSXNodeUnion, int]:
        """
        Peek at the tag name immediately after ``'<'`` and route to
        :meth:`_parse_element`, :meth:`_parse_component`, or
        :meth:`_parse_fragment_short`.
        """
        self._tick(dl)
        assert code[index] == '<'

        peek = index + 1
        tag_start = peek
        n = len(code)
        while peek < n and (code[peek].isalnum() or code[peek] in '-_:.'):
            peek += 1
        tag = code[tag_start:peek]

        if not tag:
            # Bare '<' with no valid tag name — treat as literal text
            return TextNode(content='<'), index + 1

        if tag[0].isupper():
            return self._parse_component(code, index, ctx, dl, in_pre_tag)

        if tag.lower() == 'fragment':
            # <fragment …> … </fragment> — reuse element parser, wrap result
            el, new_i = self._parse_element(code, index, ctx, dl, in_pre_tag)
            return FragmentNode(children=el.children, shorthand=False), new_i

        return self._parse_element(code, index, ctx, dl, in_pre_tag)

    # ── Fragment ───────────────────────────────────────────────────────────────

    def _parse_fragment_short(
        self,
        code: str,
        index: int,
        ctx: Dict[str, Any],
        dl: float,
        in_pre_tag: bool = False,
    ) -> Tuple[FragmentNode, int]:
        """Parse ``<> … </>`` shorthand fragment."""
        index += 2   # consume '<>'
        children, index = self._parse_children(code, index, '</>', ctx, dl, in_pre_tag)
        if code.startswith('</>', index):
            index += 3
        return FragmentNode(children=children, shorthand=True), index

    # ── Element ────────────────────────────────────────────────────────────────

    def _parse_element(
        self,
        code: str,
        index: int,
        ctx: Dict[str, Any],
        dl: float,
        in_pre_tag: bool = False,
    ) -> Tuple[ElementNode, int]:
        """Parse a single lowercase HTML element recursively."""
        self._tick(dl)
        index += 1   # consume '<'

        tag, index = self._read_tag_name(code, index)
        tag = tag or 'div'

        attrs, events, spread, self_closing, index = self._read_attrs(
            code, index, ctx, tag
        )

        # Intrinsic self-closing check (e.g. <br> without />)
        if not self_closing and tag.lower() in SELF_CLOSING_TAGS:
            self_closing = True

        # Check if this is a <pre> tag
        is_pre_tag = tag.lower() == 'pre'

        if self_closing:
            return ElementNode(
                tag=tag,
                attributes=attrs,
                events=events,
                children=[],
                self_closing=True,
                spread_props=spread,
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
        ), index

    # ── Component ──────────────────────────────────────────────────────────────

    def _parse_component(
        self,
        code: str,
        index: int,
        ctx: Dict[str, Any],
        dl: float,
        in_pre_tag: bool = False,
    ) -> Tuple[ComponentNode, int]:
        """
        Parse a PSX component (UpperCase tag) using the same recursive
        descent engine as :meth:`_parse_element`.

        Previously this was a regex match, which broke on any nested
        component of the same type.
        """
        self._tick(dl)
        index += 1   # consume '<'

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
        ), index

    # ── Children ───────────────────────────────────────────────────────────────

    def _parse_children(
        self,
        code: str,
        index: int,
        sentinel: str,
        ctx: Dict[str, Any],
        dl: float,
        in_pre_tag: bool = False,
    ) -> Tuple[List[PSXNodeUnion], int]:
        """
        Parse child nodes until *sentinel* is found at the current depth.

        Stops on any ``</`` prefix (not just the exact sentinel) to prevent
        an unexpected closing tag from causing the stuck-parser fallback to
        corrupt the buffer position.

        If *in_pre_tag* is True, all content is treated as literal text
        without expression interpolation (for <pre> tags).
        """
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

            # Skip inter-node whitespace
            while index < n and code[index] in ' \t\n\r':
                index += 1
            if index >= n:
                break

            # Exact sentinel (our closing tag)
            if code.startswith(sentinel, index):
                break

            # Any closing tag at this level means we've gone too far
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
        """Parse exactly one child node: element, component, expression, or text."""
        n = len(code)

        # Whitespace already consumed by _parse_children, but guard here too
        # in case _parse_child is called directly.
        while index < n and code[index] in ' \t\n\r':
            index += 1
        if index >= n:
            return None, index

        ch = code[index]

        # ── Markup ─────────────────────────────────────────────────────────
        if ch == '<':
            # HTML comment — skip entirely
            if code.startswith('<!--', index):
                end = code.find('-->', index)
                return None, (end + 3 if end != -1 else n)

            # Fragment shorthand
            if code.startswith('<>', index):
                return self._parse_fragment_short(code, index, ctx, dl, in_pre_tag)

            # Anything else (element or component)
            return self._dispatch(code, index, ctx, dl, in_pre_tag)

        # ── Expression ─────────────────────────────────────────────────────
        if ch == '{' and not in_pre_tag:
            end  = _match_brace(code, index)
            expr = code[index + 1 : end - 1].strip()
            pexpr = self.ast_parser.parse_expression(expr)
            return ExpressionNode(expression=expr, parsed_expression=pexpr), end

        # ── Text (may contain inline {expressions}) ─────────────────────────
        start = index
        # When inside <pre> tag, don't stop at '{' - treat it as literal text
        stop_chars = ('<',) if in_pre_tag else ('<', '{')
        while index < n and code[index] not in stop_chars:
            index += 1
        raw = code[start:index]
        
        # If inside <pre> tag, treat everything as literal text
        if in_pre_tag:
            return TextNode(content=raw), index
        
        parts = self._split_text_with_exprs(raw)
        if not parts:
            return None, index
        if len(parts) == 1:
            return parts[0], index
        # Multiple mixed nodes — wrap in an inline fragment
        return FragmentNode(children=parts, shorthand=True), index

    # ── Low-level readers ──────────────────────────────────────────────────────

    def _read_tag_name(self, code: str, index: int) -> Tuple[str, int]:
        """Read a tag name (alphanumeric + ``-_:.``) from *code* at *index*."""
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
        """
        Read all attributes on an opening tag.

        Returns ``(attributes, events, spread_props, is_self_closing, new_index)``.
        Consumes the closing ``>`` or ``/>``.
        """
        attributes: Dict[str, Any] = {}
        events:     Dict[str, Any] = {}
        spread:     List[str]      = []
        n = len(code)

        while index < n and code[index] not in ('>', '/'):
            # Skip whitespace
            while index < n and code[index].isspace():
                index += 1
            if index >= n or code[index] in ('>', '/'):
                break

            # Spread prop: {...obj}
            if code[index] == '{':
                end  = _match_brace(code, index)
                expr = code[index + 1 : end - 1].strip()
                if expr.startswith('...'):
                    spread.append(expr[3:])
                index = end
                continue

            # Attribute key
            ks = index
            while index < n and (code[index].isalnum() or code[index] in '-_:.'):
                index += 1
            key = code[ks:index]

            if not key:
                index += 1    # skip unexpected character
                continue

            while index < n and code[index].isspace():
                index += 1

            # Boolean attribute (no '=')
            if index >= n or code[index] != '=':
                attributes[key] = True
                continue

            index += 1   # consume '='
            while index < n and code[index].isspace():
                index += 1

            if index >= n:
                attributes[key] = True
                continue

            # ── Value ───────────────────────────────────────────────────
            if code[index] == '{':
                end   = _match_brace(code, index)
                value: Any = code[index:end]   # preserve braces for runtime
                index = end

            elif code[index] in ('"', "'"):
                q     = code[index]
                index += 1
                vs    = index
                while index < n and code[index] != q:
                    index += 1
                value = code[vs:index]
                index += 1   # consume closing quote

            else:
                vs = index
                while index < n and not code[index].isspace() and code[index] not in ('>', '/'):
                    index += 1
                value = code[vs:index]

            # ── Categorise ──────────────────────────────────────────────
            if key == 'bind':
                # Compiler directive; extract the bound variable name only
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
                    if tag.lower() == 'input'
                       and attributes.get('type') == 'checkbox'
                    else 'value'
                )

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
        """
        Split a raw text segment into :class:`TextNode` and
        :class:`ExpressionNode` instances.

        Uses :func:`_match_brace` so nested braces inside expressions
        — e.g. ``{obj['key']}`` or ``{fn({'a': 1})}`` — are handled
        correctly, unlike the former ``re.split(r'({[^}]+})', ...)``
        approach.
        """
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

    # ── Deadline helper ────────────────────────────────────────────────────────

    @staticmethod
    def _tick(deadline: float) -> None:
        """Raise :class:`_ParseTimeout` if the wall-clock deadline has passed."""
        if time.monotonic() > deadline:
            raise _ParseTimeout()


# ── Thread-local parser pool ───────────────────────────────────────────────────

_tls = threading.local()


def _get_parser() -> PSXParser:
    """
    Return the :class:`PSXParser` instance for the current thread.

    One instance per thread means no shared mutable state even when
    multiple requests are parsed concurrently.
    """
    if not hasattr(_tls, 'parser'):
        _tls.parser = PSXParser()
    return _tls.parser


# ── Public API ─────────────────────────────────────────────────────────────────

def psx(psx_str: str, context: Dict[str, Any] = None) -> PSXElement:
    """
    Parse a PSX string and return a :class:`PSXElement`.

    If *context* is omitted, the caller's local scope is captured
    automatically (plain, non-callable, non-``None`` values only).
    Pass an explicit dict to keep the scope clean and avoid accidental
    exposure of large or sensitive objects.
    """
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
                        and v is not None
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

    # Fragment, Component, or other root forms → wrap in a neutral div
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
    """Render a :class:`PSXElement` (or any value) to an HTML string."""
    if isinstance(element, PSXElement):
        return element.to_html(context)
    return str(element)


def fragment(children: Any) -> str:
    """Join multiple children into a single HTML string."""
    if isinstance(children, list):
        return ''.join(str(c) for c in children)
    return str(children)


def key(key_value: str, element: PSXElement) -> PSXElement:
    """Attach a reconciliation key to a :class:`PSXElement`."""
    element.key = key_value
    return element


__all__ = [
    # Legacy interface
    'PSXElement', 'PSXParser', 'psx', 'render_psx', 'fragment', 'key',
    'process_python_logic',
    # Production AST tools
    'PSXASTParser', 'PSXNodeValidator', 'PSXNodeOptimizer',
]