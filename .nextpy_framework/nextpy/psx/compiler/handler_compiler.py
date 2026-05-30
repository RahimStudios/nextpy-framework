"""
NextPy PSX Handler Compiler - AST-based Handler Extraction and Compilation
Replacing regex-based handler extraction with proper AST parsing
"""

import ast
import inspect
from typing import Dict, List, Any, Optional, Tuple, Callable
from .actions import compile_handler_to_actions, ActionType


class HandlerCompiler(ast.NodeVisitor):
    """AST-based handler compiler extracting and compiling handlers"""
    
    def __init__(self):
        self.handlers: Dict[str, List[Dict[str, Any]]] = {}
        self.current_function: Optional[str] = None
        self.handler_assignments: Dict[str, str] = {}
        self.component_context: Optional[str] = None
    
    def extract_handlers_from_function(self, func: Callable, component_name: Optional[str] = None) -> Dict[str, List[Dict[str, Any]]]:
        """Extract and compile handlers from a component function"""
        self.handlers.clear()
        self.handler_assignments.clear()
        self.component_context = component_name
        
        try:
            # Get the source code
            source = inspect.getsource(func)
            
            # Parse the AST
            tree = ast.parse(source)
            
            # Visit the AST to extract handlers
            self.visit(tree)
            
            # Compile handler assignments (create_onclick, etc.)
            self._compile_handler_assignments()
            
            return self.handlers
            
        except (OSError, SyntaxError, TypeError) as e:
            print(f"Handler extraction error: {e}")
            # Try direct file-based extraction for PSX files
            return self._extract_from_psx_file(func)
    
    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Visit function definition"""
        self.current_function = node.name
        
        # Look for handler assignments within the function
        for child in node.body:
            if isinstance(child, ast.Assign):
                self._visit_assignment(child)
            elif isinstance(child, ast.Expr) and isinstance(child.value, ast.Call):
                self._visit_expression(child.value)
        
        self.current_function = None
    
    def _visit_assignment(self, node: ast.Assign) -> None:
        """Visit assignment to extract handler assignments"""
        if len(node.targets) != 1 or not isinstance(node.targets[0], ast.Name):
            return
        
        target_name = node.targets[0].id
        value = node.value
        
        # Check for create_on... assignments
        if isinstance(value, ast.Call) and isinstance(value.func, ast.Name):
            func_name = value.func.id
            if func_name.startswith('create_on'):
                # Store the assignment for later compilation
                self.handler_assignments[target_name] = ast.unparse(value)
        
        # Check for lambda assignments
        elif isinstance(value, ast.Lambda):
            # Lambda handlers
            lambda_code = ast.unparse(value)
            actions = compile_handler_to_actions(lambda_code, target_name)
            if actions:
                self.handlers[target_name] = actions
    
    def _visit_expression(self, node: ast.Call) -> None:
        """Visit expression to extract direct function calls"""
        # This could be used for inline handlers
        pass
    
    def _compile_handler_assignments(self) -> None:
        """Compile handler assignments to structured actions"""
        for handler_name, assignment_code in self.handler_assignments.items():
            try:
                # Parse the assignment to extract the lambda
                tree = ast.parse(assignment_code)
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.Call):
                        # Extract the lambda argument
                        if node.args and isinstance(node.args[0], ast.Lambda):
                            lambda_node = node.args[0]
                            lambda_code = ast.unparse(lambda_node.body)
                            
                            # Compile to actions
                            actions = compile_handler_to_actions(lambda_code, handler_name)
                            if actions:
                                self.handlers[handler_name] = actions
                            break
            except Exception as e:
                print(f"Handler compilation error for {handler_name}: {e}")
    
    def _extract_from_psx_file(self, func: Callable) -> Dict[str, List[Dict[str, Any]]]:
        """Extract handlers directly from PSX file when inspect.getsource fails"""
        handlers = {}
        
        try:
            # Get the file path from the function
            file_path = None
            if hasattr(func, '__module__'):
                module_name = func.__module__
                # Try to find the PSX file
                import sys
                import os
                
                for path in sys.path:
                    potential_file = os.path.join(path, module_name.replace('.', '/') + '.psx')
                    if os.path.exists(potential_file):
                        file_path = potential_file
                        break
            
            if not file_path:
                # Try to get file from inspect
                try:
                    file_path = inspect.getfile(func)
                    if file_path.endswith('.py'):
                        # This is a compiled Python file, not PSX
                        return {}
                except:
                    return {}
            
            # Read the PSX file directly
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find the component function
            func_name = func.__name__
            func_pattern = rf'^\s*def\s+{re.escape(func_name)}\s*\([^)]*\)\s*:'
            
            lines = content.split('\n')
            func_start = None
            func_indent = 0
            
            for i, line in enumerate(lines):
                if re.match(func_pattern, line):
                    func_start = i
                    func_indent = len(line) - len(line.lstrip(' '))
                    break
            
            if func_start is None:
                return {}
            
            # Extract function body
            func_lines = []
            for i in range(func_start + 1, len(lines)):
                line = lines[i]
                if not line.strip():
                    func_lines.append(line)
                    continue
                
                line_indent = len(line) - len(line.lstrip(' '))
                if line_indent <= func_indent and line.strip():
                    break
                
                func_lines.append(line)
            
            func_content = '\n'.join(func_lines)
            
            # Extract create_onclick handlers using regex
            create_pattern = r'(\w+)\s*=\s*create_onclick\(\s*lambda\s+[^:]+:\s*([^)]+)\)'
            matches = re.findall(create_pattern, func_content)
            
            for handler_name, lambda_code in matches:
                try:
                    # Clean up the lambda code
                    clean_code = lambda_code.strip()
                    
                    # Compile to actions
                    actions = compile_handler_to_actions(clean_code, handler_name)
                    if actions:
                        handlers[handler_name] = actions
                except Exception as e:
                    print(f"Handler compilation error for {handler_name}: {e}")
            
            # Also look for inline lambda handlers
            inline_pattern = r'onclick=\{lambda\s+[^:]+:\s*([^}]+)\}'
            inline_matches = re.findall(inline_pattern, func_content)
            
            for i, lambda_code in enumerate(inline_matches):
                try:
                    clean_code = lambda_code.strip()
                    actions = compile_handler_to_actions(clean_code, f'inline_handler_{i}')
                    if actions:
                        handlers[f'inline_handler_{i}'] = actions
                except Exception as e:
                    print(f"Inline handler compilation error: {e}")
            
            return handlers
            
        except Exception as e:
            print(f"PSX file extraction error: {e}")
            return {}
    
    def extract_inline_handlers(self, html_content: str) -> Dict[str, List[Dict[str, Any]]]:
        """Extract inline handlers from HTML content"""
        inline_handlers = {}
        
        # Look for inline lambda handlers in HTML
        import re
        
        # Pattern to find inline handlers like onclick={lambda e: setCount(count + 1)}
        pattern = r'([a-zA-Z_][a-zA-Z0-9_]*)=\{lambda\s+[^:]+:\s*([^}]+)\}'
        
        matches = re.findall(pattern, html_content)
        for event_type, handler_code in matches:
            try:
                # Clean up the handler code
                clean_code = handler_code.strip()
                
                # Compile to actions
                actions = compile_handler_to_actions(clean_code, f"inline_{event_type}")
                if actions:
                    inline_handlers[f"inline_{event_type}"] = actions
            except Exception as e:
                print(f"Inline handler compilation error: {e}")
        
        return inline_handlers


class EnhancedHandlerExtractor:
    """Enhanced handler extraction using AST parsing"""
    
    def __init__(self):
        self.compiler = HandlerCompiler()
    
    def extract_all_handlers(self, component_func: Callable, component_name: Optional[str] = None) -> Dict[str, List[Dict[str, Any]]]:
        """Extract all handlers from a component"""
        handlers = {}
        
        # Extract function-based handlers
        function_handlers = self.compiler.extract_handlers_from_function(component_func, component_name)
        handlers.update(function_handlers)
        
        # Extract create_on... handlers
        create_handlers = self._extract_create_handlers(component_func)
        handlers.update(create_handlers)
        
        return handlers
    
    def _extract_create_handlers(self, component_func: Callable) -> Dict[str, List[Dict[str, Any]]]:
        """Extract handlers created with create_on... utilities"""
        handlers = {}
        
        try:
            source = inspect.getsource(component_func)
            tree = ast.parse(source)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                        target_name = node.targets[0].id
                        value = node.value
                        
                        if isinstance(value, ast.Call) and isinstance(value.func, ast.Name):
                            func_name = value.func.id
                            if func_name.startswith('create_on'):
                                # Extract the lambda
                                if value.args and isinstance(value.args[0], ast.Lambda):
                                    lambda_node = value.args[0]
                                    lambda_code = ast.unparse(lambda_node.body)
                                    
                                    # Compile to actions
                                    actions = compile_handler_to_actions(lambda_code, target_name)
                                    if actions:
                                        handlers[target_name] = actions
        except Exception as e:
            print(f"Create handler extraction error: {e}")
            # Try direct file-based extraction
            file_handlers = self._extract_from_psx_file(component_func)
            handlers.update(file_handlers)
        
        return handlers
    
    def _extract_from_psx_file(self, func: Callable) -> Dict[str, List[Dict[str, Any]]]:
        """Extract handlers directly from PSX file when inspect.getsource fails"""
        handlers = {}
        
        try:
            # Get the file path from the function
            file_path = None
            if hasattr(func, '__module__'):
                module_name = func.__module__
                print(f"DEBUG: EnhancedHandlerExtractor looking for module: {module_name}")
                # Try to find the PSX file
                import sys
                import os
                import re
                
                # First try to find in pages directory (common NextPy structure)
                pages_paths = [
                    os.path.join(os.getcwd(), 'pages', module_name + '.psx'),
                    os.path.join(os.getcwd(), '..', 'pages', module_name + '.psx'),
                ]
                
                for potential_file in pages_paths:
                    print(f"DEBUG: EnhancedHandlerExtractor checking pages path: {potential_file}")
                    if os.path.exists(potential_file):
                        file_path = potential_file
                        print(f"DEBUG: EnhancedHandlerExtractor found PSX file in pages: {file_path}")
                        break
                
                # If not found in pages, try sys.path
                if not file_path:
                    for path in sys.path:
                        potential_file = os.path.join(path, module_name.replace('.', '/') + '.psx')
                        print(f"DEBUG: EnhancedHandlerExtractor checking sys.path: {potential_file}")
                        if os.path.exists(potential_file):
                            file_path = potential_file
                            print(f"DEBUG: EnhancedHandlerExtractor found PSX file in sys.path: {file_path}")
                            break
            
            if not file_path:
                # Try to get file from inspect
                try:
                    file_path = inspect.getfile(func)
                    if file_path.endswith('.py'):
                        # This is a compiled Python file, not PSX
                        return {}
                except:
                    return {}
            
            # Read the PSX file directly
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find the component function
            func_name = func.__name__
            func_pattern = rf'^\s*def\s+{re.escape(func_name)}\s*\([^)]*\)\s*:'
            
            lines = content.split('\n')
            func_start = None
            func_indent = 0
            
            for i, line in enumerate(lines):
                if re.match(func_pattern, line):
                    func_start = i
                    func_indent = len(line) - len(line.lstrip(' '))
                    break
            
            if func_start is None:
                return {}
            
            # Extract function body
            func_lines = []
            for i in range(func_start + 1, len(lines)):
                line = lines[i]
                if not line.strip():
                    func_lines.append(line)
                    continue
                
                line_indent = len(line) - len(line.lstrip(' '))
                if line_indent <= func_indent and line.strip():
                    break
                
                func_lines.append(line)
            
            func_content = '\n'.join(func_lines)
            
            # Extract create_onclick handlers using regex
            create_pattern = r'(\w+)\s*=\s*create_onclick\(\s*lambda\s+[^:]+:\s*([^)]+)\)'
            matches = re.findall(create_pattern, func_content)
            
            for handler_name, lambda_code in matches:
                try:
                    # Clean up the lambda code
                    clean_code = lambda_code.strip()
                    
                    # Compile to actions
                    actions = compile_handler_to_actions(clean_code, handler_name)
                    if actions:
                        handlers[handler_name] = actions
                except Exception as e:
                    print(f"Handler compilation error for {handler_name}: {e}")
            
            # Also look for inline lambda handlers
            inline_pattern = r'onclick=\{lambda\s+[^:]+:\s*([^}]+)\}'
            inline_matches = re.findall(inline_pattern, func_content)
            
            for i, lambda_code in enumerate(inline_matches):
                try:
                    clean_code = lambda_code.strip()
                    actions = compile_handler_to_actions(clean_code, f'inline_handler_{i}')
                    if actions:
                        handlers[f'inline_handler_{i}'] = actions
                except Exception as e:
                    print(f"Inline handler compilation error: {e}")
            
            return handlers
            
        except Exception as e:
            print(f"PSX file extraction error: {e}")
            return {}


# Global enhanced extractor instance
enhanced_extractor = EnhancedHandlerExtractor()


def extract_handlers_compiled(component_func: Callable, component_name: Optional[str] = None) -> Dict[str, List[Dict[str, Any]]]:
    """Main entry point for enhanced handler extraction"""
    return enhanced_extractor.extract_all_handlers(component_func, component_name)
