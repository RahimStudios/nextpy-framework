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
        # Pattern to match JSX elements
        self.jsx_pattern = re.compile(r'(<[^>]+>)', re.MULTILINE | re.DOTALL)
        self.return_pattern = re.compile(r'return\s*\(\s*(<.*?>)\s*\)', re.MULTILINE | re.DOTALL)
        self.simple_return_pattern = re.compile(r'return\s+(<.*?>)', re.MULTILINE | re.DOTALL)
        
    def find_jsx_blocks(self, content: str) -> List[Tuple[int, int, str]]:
        """Find all JSX blocks in the content"""
        jsx_blocks = []
        
        # Find return statements with JSX
        for match in self.return_pattern.finditer(content):
            start, end = match.span()
            jsx_content = match.group(1)
            jsx_blocks.append((start, end, jsx_content))
        
        # Find simple return statements
        for match in self.simple_return_pattern.finditer(content):
            start, end = match.span()
            jsx_content = match.group(1)
            jsx_blocks.append((start, end, jsx_content))
        
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
                if '<' in content and '>' in content and 'from nextpy.psx import psx' not in content and 'import psx' not in content:
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
                if '<' in content and '>' in content and 'from nextpy.psx import psx' not in content and 'import psx' not in content:
                    imports_to_add.append('psx')
                
                # Add the imports
                if imports_to_add:
                    import_statement = f"from nextpy.psx import {', '.join(imports_to_add)}"
                    lines.insert(import_index, import_statement)
                    content = '\n'.join(lines)
            elif 'from nextpy.true_jsx import jsx' not in content and 'import jsx' not in content:
                # Find the first import line or add at the top
                lines = content.split('\n')
                import_index = 0
                
                for i, line in enumerate(lines):
                    if line.strip().startswith('import ') or line.strip().startswith('from '):
                        import_index = i + 1
                    elif line.strip() and not line.startswith('#'):
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
            
            # Look for JSX patterns
            return bool(self.return_pattern.search(content) or 
                       self.simple_return_pattern.search(content))
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
