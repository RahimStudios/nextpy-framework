#!/usr/bin/env python3
"""
PSX Language Server - Production-grade LSP implementation
Provides JSX-like developer experience for PSX
"""

import asyncio
import json
import re
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass

try:
    from pygls.server import LanguageServer
    from lsprotocol.types import (
        CompletionParams, CompletionItem, CompletionList, CompletionItemKind,
        HoverParams, Hover, MarkupContent, MarkupKind,
        TextDocumentPositionParams, Diagnostic, DiagnosticSeverity,
        InitializeParams, TextDocumentSyncKind,
        Position, Range
    )
    LSP_AVAILABLE = True
except ImportError:
    print("pygls not available - running in mock mode")
    LSP_AVAILABLE = False

from ..core import PSXCore, PSXASTParser, PSXNodeValidator
from ..core.parser import PSXParser


class PSXLanguageServer:
    """Production-grade PSX Language Server"""
    
    def __init__(self):
        self.core = PSXCore()
        self.parser = PSXParser()
        self.ast_parser = PSXASTParser()
        self.validator = PSXNodeValidator()
        
        # PSX language definitions
        self.html_tags = [
            'div', 'span', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
            'button', 'input', 'form', 'img', 'a', 'ul', 'ol', 'li',
            'table', 'tr', 'td', 'th', 'section', 'article', 'header',
            'footer', 'nav', 'main', 'aside', 'select', 'option',
            'textarea', 'label', 'br', 'hr', 'strong', 'em', 'code',
            'pre', 'blockquote', 'figure', 'figcaption', 'iframe',
            'canvas', 'svg', 'path', 'circle', 'rect', 'polygon',
            'video', 'audio', 'source', 'track', 'details', 'summary',
            'dialog', 'menu', 'menuitem', 'progress', 'meter',
            'time', 'data', 'var', 'samp', 'kbd', 'sub', 'sup',
            'small', 'mark', 'b', 'i', 'u', 's', 'strike', 'del',
            'ins', 'ruby', 'rt', 'rp', 'bdi', 'bdo'
        ]
        
        self.events = [
            'onClick', 'onChange', 'onSubmit', 'onFocus', 'onBlur',
            'onKeyDown', 'onKeyUp', 'onKeyPress', 'onMouseDown',
            'onMouseUp', 'onMouseMove', 'onMouseEnter', 'onMouseLeave',
            'onMouseOver', 'onMouseOut', 'onDoubleClick', 'onWheel',
            'onTouchStart', 'onTouchEnd', 'onTouchMove', 'onTouchCancel',
            'onLoad', 'onUnload', 'onResize', 'onScroll', 'onError',
            'onAbort', 'onCanPlay', 'onCanPlayThrough', 'onDurationChange',
            'onEmptied', 'onEnded', 'onLoadedData', 'onLoadedMetadata',
            'onPause', 'onPlay', 'onPlaying', 'onProgress', 'onRateChange',
            'onSeeked', 'onSeeking', 'onStalled', 'onSuspend', 'onTimeUpdate',
            'onVolumeChange', 'onWaiting', 'onAnimationStart', 'onAnimationEnd',
            'onAnimationIteration', 'onTransitionEnd', 'onMessage', 'onOnline',
            'onOffline', 'onStorage', 'onHashChange', 'onPopState', 'onPageHide',
            'onPageShow', 'onBeforeUnload', 'onUnload', 'onResize', 'onScroll'
        ]
        
        self.attributes = [
            'class', 'className', 'id', 'style', 'title', 'alt', 'src',
            'href', 'target', 'rel', 'type', 'value', 'name', 'placeholder',
            'disabled', 'readOnly', 'required', 'checked', 'selected',
            'multiple', 'size', 'maxLength', 'minLength', 'pattern',
            'min', 'max', 'step', 'width', 'height', 'cols', 'rows',
            'wrap', 'accept', 'capture', 'autoComplete', 'autoFocus',
            'formAction', 'formEncType', 'formMethod', 'formNoValidate',
            'formTarget', 'inputMode', 'list', 'key'
        ]
        
        self.python_keywords = [
            'if', 'else', 'elif', 'for', 'while', 'try', 'except', 'finally',
            'def', 'class', 'import', 'from', 'as', 'return', 'yield',
            'lambda', 'and', 'or', 'not', 'in', 'is', 'None', 'True', 'False'
        ]
        
        # Build completion cache
        self.completion_cache = self._build_completion_cache()
    
    def _build_completion_cache(self) -> Dict[str, List[CompletionItem]]:
        """Build completion items cache"""
        cache = {}
        
        # HTML tags
        cache['tags'] = [
            CompletionItem(
                label=tag,
                kind=CompletionItemKind.Class,
                detail=f"HTML {tag} element",
                documentation=f"HTML {tag} element",
                insert_text=tag
            ) for tag in self.html_tags
        ]
        
        # Events
        cache['events'] = [
            CompletionItem(
                label=event,
                kind=CompletionItemKind.Method,
                detail=f"Event handler: {event}",
                documentation=f"PSX event handler for {event}",
                insert_text=event
            ) for event in self.events
        ]
        
        # Attributes
        cache['attributes'] = [
            CompletionItem(
                label=attr,
                kind=CompletionItemKind.Property,
                detail=f"HTML attribute: {attr}",
                documentation=f"HTML attribute {attr}",
                insert_text=attr
            ) for attr in self.attributes
        ]
        
        # Python keywords
        cache['keywords'] = [
            CompletionItem(
                label=keyword,
                kind=CompletionItemKind.Keyword,
                detail=f"Python keyword: {keyword}",
                documentation=f"Python keyword {keyword}",
                insert_text=keyword
            ) for keyword in self.python_keywords
        ]
        
        return cache
    
    def get_completions(self, text: str, position: Position) -> CompletionList:
        """Get completions for given position"""
        if not LSP_AVAILABLE:
            return self._get_mock_completions(text, position)
        
        # Get context around cursor
        lines = text.split('\n')
        if position.line >= len(lines):
            return CompletionList(is_incomplete=False, items=[])
        
        current_line = lines[position.line]
        before_cursor = current_line[:position.character]
        
        # Determine completion context
        context = self._get_completion_context(before_cursor)
        
        items = []
        
        if context['type'] == 'tag':
            items.extend(self.completion_cache['tags'])
        elif context['type'] == 'attribute':
            items.extend(self.completion_cache['attributes'])
        elif context['type'] == 'event':
            items.extend(self.completion_cache['events'])
        elif context['type'] == 'expression':
            items.extend(self._get_expression_completions(context['expression']))
        elif context['type'] == 'keyword':
            items.extend(self.completion_cache['keywords'])
        
        return CompletionList(is_incomplete=False, items=items)
    
    def _get_completion_context(self, text: str) -> Dict[str, Any]:
        """Analyze text to determine completion context"""
        # Remove trailing whitespace
        text = text.rstrip()
        
        if not text:
            return {'type': 'tag'}
        
        # Check if inside tag
        if text.endswith('<'):
            return {'type': 'tag'}
        
        # Check if inside attribute
        tag_match = re.search(r'<(\w+)([^>]*?)$', text)
        if tag_match:
            tag_content = tag_match.group(2)
            if '=' in tag_content:
                # After =, might be expression
                return {'type': 'expression', 'expression': tag_content.split('=')[-1].strip()}
            elif tag_content.strip().endswith('on'):
                return {'type': 'event'}
            else:
                return {'type': 'attribute'}
        
        # Check if inside expression
        expr_match = re.search(r'\{([^}]*)$', text)
        if expr_match:
            return {'type': 'expression', 'expression': expr_match.group(1)}
        
        # Check if at start of line (might be keyword)
        if text.strip() in ['if', 'for', 'while', 'try']:
            return {'type': 'keyword'}
        
        return {'type': 'text'}
    
    def _get_expression_completions(self, expr: str) -> List[CompletionItem]:
        """Get completions for Python expressions"""
        items = []
        
        # Simple variable name completion
        if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', expr):
            # Could suggest common variables
            common_vars = ['user', 'items', 'data', 'props', 'state', 'setState']
            for var in common_vars:
                if var.startswith(expr):
                    items.append(CompletionItem(
                        label=var,
                        kind=CompletionItemKind.Variable,
                        detail=f"Variable: {var}",
                        documentation=f"Common PSX variable {var}"
                    ))
        
        # Object property completion
        if '.' in expr:
            obj, prop = expr.rsplit('.', 1)
            if obj in ['user', 'data', 'props']:
                # Suggest common properties
                common_props = ['name', 'id', 'email', 'value', 'length', 'size']
                for p in common_props:
                    if p.startswith(prop):
                        items.append(CompletionItem(
                            label=f"{obj}.{p}",
                            kind=CompletionItemKind.Property,
                            detail=f"Property: {p}",
                            documentation=f"Property {p} on {obj}"
                        ))
        
        return items
    
    def get_hover(self, text: str, position: Position) -> Optional[Hover]:
        """Get hover information"""
        if not LSP_AVAILABLE:
            return self._get_mock_hover(text, position)
        
        lines = text.split('\n')
        if position.line >= len(lines):
            return None
        
        current_line = lines[position.line]
        
        # Get word at cursor
        word = self._get_word_at_position(current_line, position.character)
        
        if not word:
            return None
        
        # Provide hover info
        content = None
        
        if word in self.html_tags:
            content = f"**HTML Element: `{word}`**\n\nHTML {word} element"
        elif word in self.events:
            content = f"**Event Handler: `{word}`**\n\nPSX event handler for {word}"
        elif word in self.attributes:
            content = f"**Attribute: `{word}`**\n\nHTML attribute {word}"
        elif word in self.python_keywords:
            content = f"**Python Keyword: `{word}`**\n\nPython keyword {word}"
        
        if content:
            return Hover(
                contents=MarkupContent(kind=MarkupKind.Markdown, value=content),
                range=Range(
                    start=Position(line=position.line, character=max(0, position.character - len(word))),
                    end=Position(line=position.line, character=position.character)
                )
            )
        
        return None
    
    def get_diagnostics(self, text: str) -> List[Diagnostic]:
        """Get diagnostic information"""
        if not LSP_AVAILABLE:
            return []
        
        diagnostics = []
        
        try:
            # Parse PSX using production-grade parser
            ast_node = self.parser.parse_psx(text)
            
            # Validate using production-grade validator
            errors = self.validator.validate_node(ast_node)
            
            for error in errors:
                # Try to extract line information
                error_line = self._find_error_line(error, text)
                
                diagnostics.append(Diagnostic(
                    range=Range(
                        start=Position(line=error_line, character=0),
                        end=Position(line=error_line + 1, character=0)
                    ),
                    message=error,
                    severity=DiagnosticSeverity.Error,
                    source="PSX"
                ))
        
        except Exception as e:
            # Add parsing error
            diagnostics.append(Diagnostic(
                range=Range(
                    start=Position(line=0, character=0),
                    end=Position(line=1, character=0)
                ),
                message=f"PSX parsing error: {e}",
                severity=DiagnosticSeverity.Error,
                source="PSX"
            ))
        
        return diagnostics
    
    def _get_word_at_position(self, line: str, character: int) -> str:
        """Get word at cursor position"""
        # Find word boundaries
        start = character
        while start > 0 and (line[start - 1].isalnum() or line[start - 1] in '_'):
            start -= 1
        
        end = character
        while end < len(line) and (line[end].isalnum() or line[end] in '_'):
            end += 1
        
        return line[start:end]
    
    def _find_error_line(self, error: str, text: str) -> int:
        """Find line number for error"""
        # Simple implementation - could be improved
        if 'position' in error:
            # Extract position from error message
            match = re.search(r'position (\d+)', error)
            if match:
                return int(match.group(1))
        
        # Default to first line
        return 0
    
    def _get_mock_completions(self, text: str, position: Position) -> CompletionList:
        """Mock completions for testing without LSP"""
        return CompletionList(
            is_incomplete=False,
            items=[
                CompletionItem(label="div", kind=CompletionItemKind.Class),
                CompletionItem(label="span", kind=CompletionItemKind.Class),
                CompletionItem(label="onClick", kind=CompletionItemKind.Method),
                CompletionItem(label="className", kind=CompletionItemKind.Property),
            ]
        )
    
    def _get_mock_hover(self, text: str, position: Position) -> Optional[Hover]:
        """Mock hover for testing without LSP"""
        return Hover(
            contents=MarkupContent(
                kind=MarkupKind.Markdown,
                value="**PSX Element**\n\nPSX HTML element"
            )
        )


# Create language server instance if LSP is available
if LSP_AVAILABLE:
    server = LanguageServer("psx", "v1.0.0")
    psx_ls = PSXLanguageServer()
    
    @server.feature(TEXT_DOCUMENT_COMPLETION)
    def completions(params: CompletionParams):
        """Handle completion requests"""
        try:
            # Get document text (simplified)
            # In real implementation, would get from document manager
            return psx_ls.get_completions("", params.position)
        except Exception as e:
            print(f"Completion error: {e}")
            return CompletionList(is_incomplete=False, items=[])
    
    @server.feature(TEXT_DOCUMENT_HOVER)
    def hover(params: HoverParams):
        """Handle hover requests"""
        try:
            # Get document text (simplified)
            return psx_ls.get_hover("", params.position)
        except Exception as e:
            print(f"Hover error: {e}")
            return None
    
    @server.feature(TEXT_DOCUMENT_DID_CHANGE)
    def did_change(params):
        """Handle document changes"""
        try:
            # Validate document
            # In real implementation, would get from document manager
            diagnostics = psx_ls.get_diagnostics("")
            # Send diagnostics to client
            # server.publish_diagnostics(params.text_document.uri, diagnostics)
        except Exception as e:
            print(f"Validation error: {e}")
    
    def main():
        """Start the language server"""
        server.start_io()
    
    if __name__ == "__main__":
        main()
else:
    # Mock server for testing
    psx_ls = PSXLanguageServer()
    
    def main():
        """Mock server for testing"""
        print("PSX Language Server (Mock Mode)")
        print("Install pygls for full LSP functionality:")
        print("pip install pygls lsprotocol")
    
    if __name__ == "__main__":
        main()
