"""
PSX Formatter - Production-grade code formatter for PSX
Provides Prettier-style formatting for PSX files
"""

import re
import ast
from typing import List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class PSXFormatConfig:
    """Configuration for PSX formatting"""
    indent_size: int = 2
    use_tabs: bool = False
    max_line_length: int = 80
    jsx_bracket_same_line: bool = True
    jsx_single_quote: bool = False
    trailing_comma: bool = True


class PSXFormatter:
    """Production-grade PSX formatter"""
    
    def __init__(self, config: PSXFormatConfig = None):
        self.config = config or PSXFormatConfig()
        self.indent_char = '\t' if self.config.use_tabs else ' '
        self.indent_str = self.indent_char * self.config.indent_size
    
    def format(self, code: str) -> str:
        """Format PSX code"""
        try:
            # Parse and format
            formatted_lines = []
            lines = code.split('\n')
            
            i = 0
            while i < len(lines):
                line = lines[i].rstrip()
                
                # Skip empty lines
                if not line.strip():
                    formatted_lines.append('')
                    i += 1
                    continue
                
                # Handle PSX elements
                if self._is_psx_element_start(line):
                    formatted_lines.extend(self._format_psx_element(lines, i))
                    i += self._get_element_lines(lines, i)
                else:
                    # Format regular Python code
                    formatted_lines.append(self._format_python_line(line))
                    i += 1
            
            return '\n'.join(formatted_lines)
        
        except Exception as e:
            # If formatting fails, return original
            return code
    
    def _is_psx_element_start(self, line: str) -> bool:
        """Check if line starts a PSX element"""
        stripped = line.strip()
        return (
            stripped.startswith('<') and 
            not stripped.startswith('</') and
            not stripped.startswith('<!--')
        )
    
    def _get_element_lines(self, lines: List[str], start: int) -> int:
        """Get number of lines for PSX element"""
        depth = 0
        i = start
        
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            
            if '<' in stripped:
                # Count opening tags
                open_tags = len(re.findall(r'<[^/][^>]*>', stripped))
                close_tags = len(re.findall(r'</[^>]*>', stripped))
                self_closing = len(re.findall(r'<[^>]*/>', stripped))
                
                depth += open_tags - close_tags - self_closing
            
            if depth <= 0:
                return i - start + 1
            
            i += 1
        
        return i - start + 1
    
    def _format_psx_element(self, lines: List[str], start: int) -> List[str]:
        """Format a PSX element"""
        element_lines = lines[start:start + self._get_element_lines(lines, start)]
        element_text = '\n'.join(element_lines)
        
        # Parse element
        try:
            formatted = self._format_element_text(element_text)
            return formatted.split('\n')
        except Exception:
            # Fallback to basic formatting
            return [line.rstrip() for line in element_lines]
    
    def _format_element_text(self, text: str) -> str:
        """Format PSX element text"""
        # Extract tag and props
        tag_match = re.match(r'<([a-zA-Z][a-zA-Z0-9-]*)([^>]*?)>', text)
        if not tag_match:
            return text
        
        tag = tag_match.group(1)
        props_str = tag_match.group(2)
        
        # Format props
        formatted_props = self._format_props(props_str)
        
        # Reconstruct
        return text.replace(tag_match.group(0), f'<{tag}{formatted_props}>')
    
    def _format_props(self, props_str: str) -> str:
        """Format element props"""
        if not props_str.strip():
            return ''
        
        # Extract individual props
        props = []
        current_prop = ''
        in_string = False
        string_char = None
        
        i = 0
        while i < len(props_str):
            char = props_str[i]
            
            if char in ['"', "'"] and not in_string:
                in_string = True
                string_char = char
            elif char == string_char and in_string:
                in_string = False
                string_char = None
            elif char in [' ', '\n', '\t'] and not in_string:
                if current_prop.strip():
                    props.append(current_prop.strip())
                current_prop = ''
            else:
                current_prop += char
            
            i += 1
        
        if current_prop.strip():
            props.append(current_prop.strip())
        
        # Format each prop
        formatted_props = []
        for prop in props:
            formatted_prop = self._format_single_prop(prop)
            formatted_props.append(formatted_prop)
        
        # Join props with proper indentation
        if len(formatted_props) == 1:
            return ' ' + formatted_props[0]
        else:
            indent = '\n' + self.indent_str + '  '
            return '\n' + self.indent_str + '  ' + f'\n{self.indent_str}  '.join(formatted_props)
    
    def _format_single_prop(self, prop: str) -> str:
        """Format a single property"""
        # Handle different prop types
        if '=' in prop:
            name, value = prop.split('=', 1)
            name = name.strip()
            value = value.strip()
            
            # Format value based on type
            if value.startswith('{') and value.endswith('}'):
                # Expression - keep as is
                return f'{name}={value}'
            elif value.startswith('"') or value.startswith("'"):
                # String - keep quotes
                return f'{name}={value}'
            else:
                # Attribute - add quotes
                quote = "'" if self.config.jsx_single_quote else '"'
                return f'{name}={quote}{value}{quote}'
        else:
            # Boolean attribute
            return prop
    
    def _format_python_line(self, line: str) -> str:
        """Format regular Python line"""
        # Basic Python formatting
        stripped = line.lstrip()
        if not stripped:
            return ''
        
        # Calculate indentation
        indent_level = len(line) - len(stripped)
        indent = self.indent_char * (indent_level // self.config.indent_size)
        
        return indent + stripped


def format_psx_file(file_path: str, config: PSXFormatConfig = None) -> str:
    """Format a PSX file"""
    formatter = PSXFormatter(config)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        formatted = formatter.format(content)
        
        # Write back if different
        if formatted != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(formatted)
        
        return formatted
    
    except Exception as e:
        print(f"Error formatting {file_path}: {e}")
        return ""


def format_psx_string(code: str, config: PSXFormatConfig = None) -> str:
    """Format PSX code string"""
    formatter = PSXFormatter(config)
    return formatter.format(code)


# CLI interface
if __name__ == "__main__":
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description="Format PSX files")
    parser.add_argument("file", help="PSX file to format")
    parser.add_argument("--indent-size", type=int, default=2, help="Indentation size")
    parser.add_argument("--use-tabs", action="store_true", help="Use tabs instead of spaces")
    parser.add_argument("--max-line-length", type=int, default=80, help="Maximum line length")
    
    args = parser.parse_args()
    
    config = PSXFormatConfig(
        indent_size=args.indent_size,
        use_tabs=args.use_tabs,
        max_line_length=args.max_line_length
    )
    
    formatted = format_psx_file(args.file, config)
    if formatted:
        print(f"Formatted {args.file}")
    else:
        print(f"Failed to format {args.file}")
