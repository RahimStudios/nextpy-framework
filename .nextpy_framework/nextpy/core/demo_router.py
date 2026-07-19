"""
Demo Router - Serves built-in demo pages when no project exists
Detects if user is in a NextPy project and shows demo pages if not
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
from .demo_pages_simple import DEMO_ROUTES


class DemoRouter:
    """Router for demo pages when no project is created"""
    
    def __init__(self):
        self.demo_routes = DEMO_ROUTES
    
    def is_nextpy_project(self, current_dir: Path = None) -> bool:
        """Check if current directory is a NextPy project"""
        if current_dir is None:
            current_dir = Path.cwd()
        
        # Check for NextPy project indicators
        indicators = [
            'pages',          # Pages directory
            'main.py',        # Entry point
            'requirements.txt', # Dependencies
            'pyproject.toml',  # Project config
            '.nextpy_framework' # Framework directory
        ]
        
        return any((current_dir / indicator).exists() for indicator in indicators)
    
    def get_demo_page(self, path: str) -> Optional[callable]:
        """Get demo page for given path"""
        # Clean the path
        path = path.rstrip('/') or '/'
        
        # Return matching demo page
        return self.demo_routes.get(path)
    
    def should_serve_demo(self, current_dir: Path = None) -> bool:
        """Check if demo pages should be served"""
        # Don't serve demo if we're in a NextPy project
        return not self.is_nextpy_project(current_dir)
    
    def get_demo_routes(self) -> Dict[str, callable]:
        """Get all demo routes"""
        return self.demo_routes.copy()
    
    def list_demo_routes(self) -> list:
        """List all available demo routes"""
        return list(self.demo_routes.keys())


# Global demo router instance
demo_router = DemoRouter()
