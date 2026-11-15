"""
NextPy JSX Preprocessor - Transform Python files with JSX syntax to valid Python
Converts <div>...</div> to jsx('<div>...</div>') calls
"""

import re
import os
from pathlib import Path
from typing import Dict, List, Tuple

try:
    from .plugins import plugin_manager, PluginContext
    PLUGINS_AVAILABLE = True
except ImportError:
    PLUGINS_AVAILABLE = False
    plugin_manager = None


class JSXSyntaxError(Exception):
    """Custom exception for JSX syntax errors"""
    
    def __init__(self, message: str, line_number: int = None, column: int = None, file_path: str = None):
        self.message = message
        self.line_number = line_number
        self.column = column
        self.file_path = file_path
        
        # Build detailed error message
        error_parts = ["JSX Syntax Error"]
        if file_path:
            error_parts.append(f"in file '{file_path}'")
        if line_number is not None:
            error_parts.append(f"at line {line_number}")
            if column is not None:
                error_parts.append(f"column {column}")
        
        error_parts.append(f": {message}")
        super().__init__(" ".join(error_parts))


class JSXPreprocessor:
    """Preprocess Python files containing JSX syntax"""
    
    def __init__(self):
        self.jsx_pattern = re.compile(r'(<[^>]+>)', re.MULTILINE | re.DOTALL)

    # Candidate ``return`` keywords at statement position: start of a line,
    # optional indentation, then the keyword.  Candidates are collected on
    # the triple-quote-masked source so ``return <p>…`` samples inside
    # docstrings/snippet strings and ``#`` comments are never seen.
    _RETURN_STMT_RE = re.compile(r'^[ \t]*return\b', re.MULTILINE)

    _TRIPLE_STRING_RE = re.compile(r'""".*?"""|\'\'\'.*?\'\'\'', re.DOTALL)

    @staticmethod
    def _mask_strings(content: str) -> str:
        """Blank out triple-quoted string bodies, preserving length and
        newlines so match positions still map to the original source.

        Snippet/docstring literals routinely contain ``return <p>…`` code
        samples; without masking, the JSX return patterns below match inside
        the string and corrupt it into nested ``psx(\"\"\"…)\"\"\")`` calls.
        Only triple-quoted strings are masked — single/double quoted strings
        are left alone because apostrophes in JSX text would create false
        string spans and hide real JSX blocks.
        """
        def _blank(m):
            s = m.group(0)
            return ''.join('\n' if c == '\n' else ' ' for c in s)
        return JSXPreprocessor._TRIPLE_STRING_RE.sub(_blank, content)

    @staticmethod
    def _is_line_end(s: str, i: int) -> bool:
        """True when only blanks remain between ``i`` and end-of-line/EOF."""
        n = len(s)
        while i < n and s[i] in ' \t\r':
            i += 1
        return i >= n or s[i] == '\n'

    @staticmethod
    def _skip_string(s: str, i: int) -> int:
        """Index just past the string literal opening at ``s[i]`` (``'`` or
        ``"``), honouring escapes and triple-quoted forms.  An unterminated
        single-line string stops at the newline so scanning can continue."""
        n = len(s)
        q = s[i]
        if s.startswith(q * 3, i):
            j = i + 3
            while j < n:
                if s[j] == '\\':
                    j += 2
                    continue
                if s.startswith(q * 3, j):
                    return j + 3
                j += 1
            return n
        j = i + 1
        while j < n:
            c = s[j]
            if c == '\\':
                j += 2
                continue
            if c == q:
                return j + 1
            if c == '\n':
                return j
            j += 1
        return n

    def _find_tag_end(self, s: str, j: int):
        """Index just past the ``>`` closing a tag that starts scanning at
        ``j``, skipping quoted attribute values.  ``None`` at EOF."""
        n = len(s)
        while j < n:
            c = s[j]
            if c == '>':
                return j + 1
            if c == "'" or c == '"':
                j = self._skip_string(s, j)
                continue
            j += 1
        return None

    def _scan_jsx_tag(self, s: str, i: int):
        """Parse the JSX tag opening at ``s[i] == '<'``.

        Returns ``(next_index, depth_delta)`` — ``next_index`` is just past
        the tag's ``>`` and ``depth_delta`` is ``+1`` for an opening element,
        ``-1`` for a closing ``</…>`` tag and ``0`` for self-closing tags,
        comments and declarations.  Returns ``None`` when ``<`` is literal
        text (e.g. ``a < b`` or ``<3``), so the caller treats it as prose.
        """
        n = len(s)
        j = i + 1
        if j >= n:
            return None
        c = s[j]
        if c == '!':
            if s.startswith('<!--', i):
                k = s.find('-->', i + 4)
                return (n if k < 0 else k + 3, 0)
            end = self._find_tag_end(s, j)
            return (None if end is None else (end, 0))
        if c == '?':
            k = s.find('?>', j + 1)
            if k >= 0:
                return (k + 2, 0)
            end = self._find_tag_end(s, j)
            return (None if end is None else (end, 0))
        if c == '/':
            # ``</name>`` closing tag — ``</`` followed by anything else is
            # literal prose (e.g. "a </ b").
            k = j + 1
            if k < n and (s[k].isalpha() or s[k] in '_$'):
                end = self._find_tag_end(s, k)
                return (None if end is None else (end, -1))
            return None
        if c.isalpha() or c in '_$':
            end = self._find_tag_end(s, j)
            if end is None:
                return None
            # ``<tag …/>`` self-closes when ``/`` immediately precedes ``>``.
            return (end, 0 if s[end - 2] == '/' else 1)
        return None

    def _jsx_close_candidates(self, s: str, i: int):
        """Scan JSX starting at ``s[i] == '<'`` and collect every ``)`` that
        could close the ``return (`` paren, as ``(index, top_level)`` pairs
        in scan order.

        Runs on masked source.  In JSX text, tags are parsed (tracking open
        element depth) and ``{`` opens an expression; parens in prose are
        literal.  Inside ``{...}`` a small scanner tracks ``()[]{}``
        nesting, string literals and ``#`` comments.  A ``)`` is a
        candidate only when the rest of its line is blank — so ``(see
        <a>x</a>)`` mid-line prose can't end the block, while ``return
        (<div/> )`` and the canonical ``…</div>\n    )`` layouts can.
        ``top_level`` marks candidates seen with no open element and no open
        expression — the only ones that can really be the ``return (``
        closer; the rest are kept as fallbacks for malformed JSX.
        """
        n = len(s)
        expr = None  # [paren, bracket, brace] counters inside {...}
        depth = 0    # open JSX element depth in text mode
        candidates = []
        while i < n:
            c = s[i]
            if expr is None:
                if c == '{':
                    expr = [0, 0, 0]
                elif c == '<':
                    tag = self._scan_jsx_tag(s, i)
                    if tag is not None:
                        i, delta = tag
                        depth = max(0, depth + delta)
                        continue
                    i += 1
                    continue
                elif c == ')' and self._is_line_end(s, i + 1):
                    candidates.append((i, depth == 0))
                i += 1
                continue
            if c == "'" or c == '"':
                i = self._skip_string(s, i)
                continue
            if c == '#':
                j = s.find('\n', i)
                i = n if j < 0 else j + 1
                continue
            if c == '(':
                expr[0] += 1
            elif c == ')':
                if expr[0] > 0:
                    expr[0] -= 1
                elif (expr[1] == 0 and expr[2] == 0
                      and self._is_line_end(s, i + 1)):
                    # ``)`` at expression top level with a blank rest-of-line
                    # can only be the ``return (`` closer (the ``{`` is
                    # unclosed, so validation will flag the block anyway).
                    candidates.append((i, False))
            elif c == '[':
                expr[1] += 1
            elif c == ']':
                if expr[1] > 0:
                    expr[1] -= 1
            elif c == '{':
                expr[2] += 1
            elif c == '}':
                if expr[2] > 0:
                    expr[2] -= 1
                else:
                    expr = None  # closed the {...} expression
            i += 1
        return candidates

    def _scan_paren_return(self, masked: str, content: str, stmt_start: int,
                           paren_idx: int):
        """Handle ``return ( <jsx> )`` starting at the ``(`` (``paren_idx``).
        Returns a ``(start, end, jsx_content)`` tuple or ``None`` when the
        parenthesised expression is not JSX."""
        n = len(masked)
        i = paren_idx + 1
        while i < n and masked[i] in ' \t\r\n':
            i += 1
        if i >= n or masked[i] != '<':
            return None  # ordinary ``return (expr)``
        candidates = self._jsx_close_candidates(masked, i)
        # Prefer top-level candidates (element depth 0, no open expression);
        # fall back to the rest so malformed JSX still reaches validation.
        ordered = ([c for c in candidates if c[1]] +
                   [c for c in candidates if not c[1]])
        for close, _top in ordered:
            # JSX span: first non-blank after ``(`` .. last non-blank before
            # the candidate ``)``.
            j = close - 1
            while j > paren_idx and masked[j] in ' \t\r\n':
                j -= 1
            jsx_content = content[i:j + 1]
            stripped = jsx_content.strip()
            # A real JSX block is a single element-ish region: starts with
            # ``<`` and ends with ``>`` (matching _validate_jsx_block).  A
            # candidate failing this is prose like ``(i18n)`` at EOL — skip
            # it and try the next ``)``.
            if not (stripped.startswith('<') and stripped.endswith('>')):
                continue
            # Statement region ends after ``)`` plus trailing blanks, as the
            # old regex's ``\)[ \t]*(?=\n|$)`` did.
            end = close + 1
            while end < n and masked[end] in ' \t':
                end += 1
            return (stmt_start, end, jsx_content)
        return None

    def _scan_simple_return(self, masked: str, content: str, stmt_start: int,
                            jsx_start: int):
        """Handle single-line ``return <jsx>…</jsx>`` (no parentheses).
        Conservative: the JSX must fit on one line and end at the last
        ``>`` on that line, mirroring the old ``<[^\\n]+>`` group."""
        n = len(masked)
        eol = masked.find('\n', jsx_start)
        if eol < 0:
            eol = n
        gt = masked.rfind('>', jsx_start, eol)
        if gt < 0:
            return None
        jsx_end = gt + 1
        stripped = content[jsx_start:jsx_end].strip()
        if len(stripped) < 3 or not stripped.startswith('<'):
            return None
        return (stmt_start, jsx_end, content[jsx_start:jsx_end])

    def find_jsx_blocks(self, content: str) -> List[Tuple[int, int, str]]:
        """Find all JSX blocks in the content.

        Returns ``(start, end, jsx_content)`` tuples where
        ``content[start:end]`` is the whole ``return …`` statement region and
        ``jsx_content`` is the exact JSX substring inside it — so the
        replacement logic can do ``content[start:end].replace(jsx_content,
        call)`` exactly as before.
        """
        jsx_blocks = []
        masked = self._mask_strings(content)
        n = len(masked)
        skip_until = -1

        # Candidates come from the masked copy (identical length); JSX text
        # is sliced from the original so string contents survive intact.
        for match in self._RETURN_STMT_RE.finditer(masked):
            if match.start() < skip_until:
                # e.g. prose ``return <code>x</code>`` at line start inside
                # an already-matched ``return (...)`` JSX block.
                continue
            i = match.end()
            while i < n and masked[i] in ' \t\r\n':
                i += 1
            if i >= n:
                continue
            if masked[i] == '(':
                block = self._scan_paren_return(masked, content, match.start(), i)
            elif masked[i] == '<':
                block = self._scan_simple_return(masked, content, match.start(), i)
            else:
                continue
            if block is not None:
                jsx_blocks.append(block)
                skip_until = block[1]

        return jsx_blocks
    
    def transform_jsx_to_function_call(self, jsx_str: str) -> str:
        """Transform JSX string to function call"""
        # Escape the JSX string for Python
        escaped_jsx = jsx_str.replace('"', '\\"').replace('\n', '\\n')
        return f'jsx("{escaped_jsx}")'
    
    def transform_jsx_to_psx_call(self, jsx_str: str) -> str:
        """Transform JSX string to PSX function call with proper context handling"""
        # For PSX, we need to handle expressions properly
        # Don't escape the expressions, keep them as-is for PSX processing
        return f'psx("""{jsx_str}""")'
    
    def preprocess_content(self, content: str, file_path: str = None) -> str:
        """Preprocess content containing JSX with enhanced error handling and plugin support"""
        try:
            # Add import statement if not present
            # Check if this is a PSX component
            is_psx_component = '@component' in content or 'from nextpy.psx import' in content
            
            # Auto-import PSX components if needed (do this first!)
            if is_psx_component:
                lines = content.split('\n')
                import_index = 0
                
                # Find where to insert imports
                for i, line in enumerate(lines):
                    if line.strip().startswith('import ') or line.strip().startswith('from '):
                        import_index = i + 1
                    elif line.strip() and not line.startswith('#'):
                        break
                
                # Check what imports are needed
                imports_to_add = []
                
                # Add component decorator if used but not imported
                if '@component' in content and 'from nextpy.psx import component' not in content and 'import component' not in content:
                    imports_to_add.append('component')
                
                # Add psx function if JSX syntax is detected
                if '<' in content and '>' in content and 'from nextpy.psx import psx' not in content and not re.search(r'\bimport\s+psx\b', content):
                    imports_to_add.append('psx')
                
                # Add the imports
                if imports_to_add:
                    import_statement = f"from nextpy.psx import {', '.join(imports_to_add)}"
                    lines.insert(import_index, import_statement)
                    content = '\n'.join(lines)
            
            # Apply plugins if available
            if PLUGINS_AVAILABLE and plugin_manager:
                plugin_context = PluginContext(
                    file_path=Path(file_path) if file_path else Path("unknown"),
                    file_content=content,
                    metadata={},
                    config={},
                    debug=False
                )
                
                plugin_result = plugin_manager.transform_content(plugin_context)
                
                if not plugin_result.success:
                    # Log plugin errors but continue processing
                    for error in plugin_result.errors:
                        print(f"Plugin error: {error}")
                
                content = plugin_result.content
                
                # Log warnings
                for warning in plugin_result.warnings:
                    print(f"Plugin warning: {warning}")
            
            # Add import statement if not present
            # Check if this is a PSX component
            is_psx_component = '@component' in content or 'from nextpy.psx import' in content
            
            if is_psx_component:
                # Auto-import PSX components if needed
                lines = content.split('\n')
                import_index = 0

                # Find where to insert imports — track paren depth AND the
                # end of each import block so a multi-line
                # ``from x import (\n    a,\n)`` doesn't get the new import
                # injected inside the parentheses.
                depth = 0
                in_import = False
                for i, line in enumerate(lines):
                    stripped = line.strip()
                    if depth == 0 and (stripped.startswith('import ') or stripped.startswith('from ')):
                        in_import = True
                    if in_import:
                        import_index = i + 1
                        depth += line.count('(') - line.count(')')
                        if depth <= 0:
                            depth = 0
                            in_import = False
                        continue
                    if stripped and not stripped.startswith('#'):
                        break

                # Check what imports are needed
                imports_to_add = []

                # Add component decorator if used but not imported
                if '@component' in content and 'from nextpy.psx import component' not in content and 'import component' not in content:
                    imports_to_add.append('component')

                # Add psx function if JSX syntax is detected
                if '<' in content and '>' in content and 'from nextpy.psx import psx' not in content and not re.search(r'\bimport\s+psx\b', content):
                    imports_to_add.append('psx')

                # Add the imports
                if imports_to_add:
                    import_statement = f"from nextpy.psx import {', '.join(imports_to_add)}"
                    lines.insert(import_index, import_statement)
                    content = '\n'.join(lines)
            elif 'from nextpy.true_jsx import jsx' not in content and 'import jsx' not in content:
                # Find the first import line or add at the top — same
                # import-block tracking as above.
                lines = content.split('\n')
                import_index = 0
                depth = 0
                in_import = False

                for i, line in enumerate(lines):
                    stripped = line.strip()
                    if depth == 0 and (stripped.startswith('import ') or stripped.startswith('from ')):
                        in_import = True
                    if in_import:
                        import_index = i + 1
                        depth += line.count('(') - line.count(')')
                        if depth <= 0:
                            depth = 0
                            in_import = False
                        continue
                    if stripped and not stripped.startswith('#'):
                        break

                lines.insert(import_index, 'from nextpy.true_jsx import jsx, render_jsx')
                content = '\n'.join(lines)
            
            # Transform JSX blocks
            jsx_blocks = self.find_jsx_blocks(content)
            
            # Process blocks in reverse order to maintain positions
            for start, end, jsx_content in reversed(jsx_blocks):
                try:
                    # Validate individual JSX block
                    self._validate_jsx_block(jsx_content, content, start, file_path, is_psx=is_psx_component)
                    
                    # Replace JSX with function call
                    if is_psx_component:
                        function_call = self.transform_jsx_to_psx_call(jsx_content)
                    else:
                        function_call = self.transform_jsx_to_function_call(jsx_content)
                    
                    # Replace the original return statement
                    original_return = content[start:end]
                    new_return = original_return.replace(jsx_content, function_call)
                    content = content[:start] + new_return + content[end:]
                except Exception as e:
                    line_num = self._get_line_number(content, start)
                    raise JSXSyntaxError(
                        f"Error processing JSX block: {str(e)}",
                        line_number=line_num,
                        file_path=file_path
                    )
            
            return content
            
        except JSXSyntaxError:
            # Re-raise JSX syntax errors as-is
            raise
        except Exception as e:
            # Wrap other exceptions
            raise JSXSyntaxError(
                f"Unexpected error during JSX preprocessing: {str(e)}",
                file_path=file_path
            )
    
    def preprocess_file(self, file_path: Path) -> str:
        """Preprocess a Python file with JSX"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            raise JSXSyntaxError(
                f"File not found: {file_path}",
                file_path=str(file_path)
            )
        except UnicodeDecodeError as e:
            raise JSXSyntaxError(
                f"Unable to read file (encoding error): {str(e)}",
                file_path=str(file_path)
            )
        except Exception as e:
            raise JSXSyntaxError(
                f"Error reading file: {str(e)}",
                file_path=str(file_path)
            )
        
        return self.preprocess_content(content, str(file_path))
    
    def preprocess_and_save(self, file_path: Path, output_path: Path = None):
        """Preprocess file and save result with error handling"""
        if output_path is None:
            output_path = file_path
        
        try:
            content = self.preprocess_file(file_path)
            
            # Create output directory if it doesn't exist
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
        except JSXSyntaxError:
            # Re-raise JSX syntax errors as-is
            raise
        except Exception as e:
            raise JSXSyntaxError(
                f"Error saving processed file: {str(e)}",
                file_path=str(file_path)
            )
    
    def is_jsx_file(self, file_path: Path) -> bool:
        """Check if file contains JSX syntax"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Look for JSX return blocks — the scanner masks triple-quoted
            # strings internally, so `return <p>` inside code samples
            # doesn't count as real JSX.
            return bool(self.find_jsx_blocks(content))
        except:
            return False
    
    def _validate_jsx_structure(self, content: str, file_path: str = None):
        """Validate basic JSX structure in content"""
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            line_num = i + 1
            stripped = line.strip()
            
            # Check for unclosed tags
            if '<' in stripped and '>' not in stripped:
                # Might be a multi-line JSX, check if it's properly closed later
                continue
            
            # Check for malformed JSX tags
            if '<' in stripped:
                # Count opening and closing tags
                open_tags = len(re.findall(r'<[^/][^>]*>', stripped))
                close_tags = len(re.findall(r'</[^>]*>', stripped))
                self_closing = len(re.findall(r'<[^>]*/>', stripped))
                
                if open_tags > close_tags + self_closing:
                    raise JSXSyntaxError(
                        f"Unclosed JSX tag detected",
                        line_number=line_num,
                        file_path=file_path
                    )
    
    def _validate_jsx_block(self, jsx_content: str, full_content: str, position: int, file_path: str = None, is_psx: bool = False):
        """Validate individual JSX block for syntax errors"""
        # Skip validation for PSX components - PSX handles its own parsing
        if is_psx:
            return
            
        # Remove surrounding whitespace
        jsx_content = jsx_content.strip()
        
        if not jsx_content.startswith('<') or not jsx_content.endswith('>'):
            raise JSXSyntaxError(
                f"Invalid JSX block: must start with '<' and end with '>'",
                file_path=file_path
            )
        
        # First perform balanced-tag checks to catch unclosed/mismatched tags
        self._check_balanced_tags(jsx_content, file_path=file_path)
        self._validate_jsx_structure(jsx_content, file_path=file_path)

        # Then delegate to the shared parser for deeper validation
        try:
            from .true_jsx import parser
            parser.parse_jsx(jsx_content)
        except Exception as e:
            # Rewrap parser errors as JSXSyntaxError for consistency
            raise JSXSyntaxError(str(e), file_path=file_path)
    
    def _check_balanced_tags(self, jsx_str: str, file_path: str = None):
        """Ensure opening and closing tags are properly nested in a JSX block"""
        stack = []
        # simple regex to capture tags; self-closing tags end with '/>'
        tag_pattern = re.compile(r'<(/?)([a-zA-Z][a-zA-Z0-9]*)[^>]*?(/?)>')
        for match in tag_pattern.finditer(jsx_str):
            closing = match.group(1) == '/'
            tag = match.group(2)
            self_close = match.group(3) == '/'
            if closing:
                if not stack or stack[-1] != tag:
                    raise JSXSyntaxError(
                        f"Malformed JSX: closing tag </{tag}> does not match open "+
                        (f"<{stack[-1]}>" if stack else "(none)"),
                        file_path=file_path
                    )
                stack.pop()
            elif not self_close:
                stack.append(tag)
        if stack:
            raise JSXSyntaxError(
                f"Unclosed JSX tag(s): {','.join(stack)}",
                file_path=file_path
            )

    def _get_line_number(self, content: str, position: int) -> int:
        """Get line number for a given position in content"""
        lines_before = content[:position].count('\n')
        return lines_before + 1


# Global preprocessor instance
preprocessor = JSXPreprocessor()


def preprocess_file(file_path: Path, output_path: Path = None) -> str:
    """Convenience function to preprocess a file"""
    return preprocessor.preprocess_and_save(file_path, output_path)


def preprocess_content(content: str, file_path: str = None) -> str:
    """Convenience function to preprocess content with error handling"""
    try:
        return preprocessor.preprocess_content(content, file_path)
    except JSXSyntaxError:
        raise
    except Exception as e:
        raise JSXSyntaxError(
            f"JSX preprocessing failed: {str(e)}",
            file_path=file_path
        )


def is_jsx_file(file_path: Path) -> bool:
    """Convenience function to check if file contains JSX"""
    return preprocessor.is_jsx_file(file_path)