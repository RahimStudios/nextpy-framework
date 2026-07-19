"""
PSX Core - Unified production-grade PSX system
Tightly integrated AST, parser, runtime, and evaluator
"""

from typing import Dict, Any

from .ast_nodes import (
    # Core types
    NodeType, LogicType, PSXNode, PSXNodeUnion,
    
    # Node types
    ElementNode, TextNode, ExpressionNode, LogicNode,
    IfNode, ForNode, WhileNode, TryNode,
    ComponentNode, FragmentNode,
    
    # Production-grade utilities
    PSXASTParser, PSXNodeValidator, PSXNodeOptimizer
)

from .evaluator import (
    SafeExpressionEngine,
    safe_eval
)

from .runtime import (
    PSXRuntime, PSXRuntimeError,
    process_python_logic,
    runtime
)

from .parser import (
    # Legacy interface
    PSXElement, PSXParser, psx, render_psx, 
    fragment, key,
    
    # Production-grade interface
    PSXASTParser as ParserASTParser,
    PSXNodeValidator as ParserNodeValidator,
    PSXNodeOptimizer as ParserNodeOptimizer
)


class PSXCore:
    """Unified PSX core system - production-grade integration"""
    
    def __init__(self):
        self.runtime = PSXRuntime()
        self.parser = PSXParser()
        self.ast_parser = PSXASTParser()
        self.validator = PSXNodeValidator()
        self.optimizer = PSXNodeOptimizer()
        self.evaluator = SafeExpressionEngine()
    
    def parse(self, psx_str: str, context: Dict[str, Any] = None) -> PSXNodeUnion:
        """Parse PSX string to optimized AST"""
        ast_node = self.parser.parse_psx(psx_str, context)
        
        # Validate
        errors = self.validator.validate_node(ast_node)
        if errors:
            raise ValueError(f"PSX validation errors: {errors}")
        
        # Optimize
        return self.optimizer.optimize_node(ast_node)
    
    def render(self, ast_node: PSXNodeUnion, context: Dict[str, Any] = None) -> str:
        """Render AST node to HTML"""
        if context:
            self.runtime.update_context(context)
        
        return self.runtime._render_node(ast_node)
    
    def parse_and_render(self, psx_str: str, context: Dict[str, Any] = None) -> str:
        """Parse PSX string and render to HTML in one step"""
        ast_node = self.parse(psx_str, context)
        return self.render(ast_node, context)
    
    def evaluate_expression(self, expression: str, context: Dict[str, Any] = None) -> Any:
        """Safely evaluate expression"""
        if context:
            self.evaluator = SafeExpressionEngine(context)
        
        return self.evaluator.evaluate(expression)
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get performance and usage metrics"""
        return {
            'runtime_cache_size': len(self.runtime._expression_cache),
            'evaluator_safety': 'production_grade',
            'parser_capabilities': [
                'elements', 'components', 'fragments', 
                'expressions', 'events', 'spread_props',
                'self_closing', 'logic_blocks'
            ],
            'ast_features': [
                'parsed_expressions', 'validation', 'optimization',
                'react_level_features', 'production_grade'
            ]
        }


# Global core instance
psx_core = PSXCore()


# Convenience functions for direct usage
def parse_psx(psx_str: str, context: Dict[str, Any] = None) -> PSXNodeUnion:
    """Parse PSX string using production-grade core"""
    return psx_core.parse(psx_str, context)


def render_psx_ast(ast_node: PSXNodeUnion, context: Dict[str, Any] = None) -> str:
    """Render PSX AST node using production-grade core"""
    return psx_core.render(ast_node, context)


def psx_to_html(psx_str: str, context: Dict[str, Any] = None) -> str:
    """Convert PSX string to HTML using production-grade core"""
    return psx_core.parse_and_render(psx_str, context)


def safe_eval_psx(expression: str, context: Dict[str, Any] = None) -> Any:
    """Safely evaluate PSX expression using production-grade core"""
    return psx_core.evaluate_expression(expression, context)


# Export everything
__all__ = [
    # Core unified system
    'PSXCore', 'psx_core',
    
    # Convenience functions
    'parse_psx', 'render_psx_ast', 'psx_to_html', 'safe_eval_psx',
    
    # AST nodes
    'NodeType', 'LogicType', 'PSXNode', 'PSXNodeUnion',
    'ElementNode', 'TextNode', 'ExpressionNode', 'LogicNode',
    'IfNode', 'ForNode', 'WhileNode', 'TryNode',
    'ComponentNode', 'FragmentNode',
    
    # AST utilities
    'PSXASTParser', 'PSXNodeValidator', 'PSXNodeOptimizer',
    
    # Evaluator
    'SafeExpressionEngine', 'safe_eval',
    
    # Runtime
    'PSXRuntime', 'PSXRuntimeError', 'process_python_logic', 'runtime',
    
    # Parser (legacy)
    'PSXElement', 'PSXParser', 'psx', 'render_psx', 'fragment', 'key'
]
