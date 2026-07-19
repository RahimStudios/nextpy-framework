"""
Debug utilities for NextPy development
Provides error tracking, logging, and debug panel support
"""

import traceback
import sys
from typing import Optional, Dict, Any
from fastapi import Request
from starlette.responses import HTMLResponse


class ErrorTracker:
    """Track and format errors for debug panel"""
    
    def __init__(self):
        self.last_error: Optional[Dict[str, Any]] = None
    
    def capture_error(self, exc: Exception, request: Optional[Request] = None) -> Dict[str, Any]:
        """Capture error details"""
        tb = traceback.format_exc()
        exc_type, exc_value, exc_tb = sys.exc_info()
        
        # Get file and line number
        tb_list = traceback.extract_tb(exc_tb)
        last_frame = tb_list[-1] if tb_list else None
        
        error_data = {
            "type": exc.__class__.__name__,
            "message": str(exc),
            "traceback": tb,
            "file": last_frame.filename if last_frame else None,
            "line": last_frame.lineno if last_frame else None,
            "path": request.url.path if request else None,
        }
        
        self.last_error = error_data
        return error_data
    
    def get_last_error(self) -> Optional[Dict[str, Any]]:
        """Get last captured error"""
        return self.last_error
    
    def clear_error(self):
        """Clear last error"""
        self.last_error = None


error_tracker = ErrorTracker()


async def render_error_page(error: Dict[str, Any]) -> HTMLResponse:
    """Render error page with debug info"""
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>NextPy Error</title>
        <!-- rely on compiled CSS instead of CDN -->
        <link href="/tailwind.css" rel="stylesheet">
        <style>
            .animate-pulse {{ animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite; }}
            @keyframes pulse {{
                0%, 100% {{ opacity: 1; }}
                50% {{ opacity: .5; }}
            }}
        </style>
    </head>
    <body class="bg-gray-900">
        <div class="fixed bottom-0 left-0 right-0 z-50 text-red-100 border-t-4 border-red-600 shadow-2xl bg-red-950">
            <div class="max-w-full">
                <div class="flex items-center justify-between p-4 bg-red-900">
                    <div class="flex items-center gap-3">
                        <span class="text-2xl">⚠️</span>
                        <div>
                            <h3 class="text-lg font-bold">{error.get('type', 'Error')}</h3>
                            <p class="text-sm text-red-200">{error.get('message', 'An error occurred')}</p>
                        </div>
                    </div>
                </div>
                <div class="p-4">
                    <h4 class="mb-2 font-mono text-sm font-bold">Traceback:</h4>
                    <pre class="p-3 overflow-x-auto font-mono text-xs text-red-100 bg-black rounded bg-opacity-30">{error.get('traceback', '')}</pre>
                </div>
                <div class="p-4 border-t border-red-800">
                    <h4 class="mb-2 font-mono text-sm font-bold">Location:</h4>
                    <p class="text-sm"><span class="text-red-300">{error.get('file', 'unknown')}</span> line <span class="font-bold">{error.get('line', '?')}</span></p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(html, status_code=500)
