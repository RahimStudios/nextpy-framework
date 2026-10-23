"""
Debug utilities for NextPy development
Provides error tracking, logging, and debug panel support
"""

import html
import linecache
import os
import sys
import traceback
from pathlib import Path
from typing import Any, Dict, List, Optional

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


def _is_project_frame(filename: str) -> bool:
    if not filename or filename.startswith("<"):
        return False
    path = Path(filename).resolve()
    cwd = Path.cwd().resolve()
    if "site-packages" in path.parts or "dist-packages" in path.parts:
        return False
    if ".nextpy_framework" in path.parts:
        return False
    try:
        path.relative_to(cwd)
        return True
    except ValueError:
        return False


def _error_frames(exc: Exception) -> List[Dict[str, Any]]:
    tb = exc.__traceback__
    frames = traceback.extract_tb(tb)
    result: List[Dict[str, Any]] = []
    for frame in frames:
        filename = frame.filename
        line_no = frame.lineno or 0
        source = linecache.getline(filename, line_no).rstrip("\n")
        result.append(
            {
                "file": filename,
                "line": line_no,
                "function": frame.name,
                "source": source,
                "project": _is_project_frame(filename),
            }
        )
    return result


def _code_context(filename: str, line_no: int, radius: int = 4) -> List[Dict[str, Any]]:
    if not filename or not line_no:
        return []
    rows = []
    start = max(1, line_no - radius)
    end = line_no + radius
    for number in range(start, end + 1):
        source = linecache.getline(filename, number)
        if not source:
            continue
        rows.append(
            {
                "number": number,
                "source": source.rstrip("\n"),
                "current": number == line_no,
            }
        )
    return rows


def _suggestion(exc: Exception) -> str:
    name = type(exc).__name__
    if isinstance(exc, ImportError):
        return "Check the import path and make sure the package is installed in the active environment."
    if isinstance(exc, SyntaxError):
        return "Check the highlighted line for unbalanced brackets, quotes, or invalid JSX."
    if isinstance(exc, AttributeError):
        return "The value may be None or the attribute name may be misspelled."
    if isinstance(exc, KeyError):
        return "The dictionary key is missing. Use .get() with a default or verify the data shape."
    if isinstance(exc, TypeError):
        return "Check the function signature and the number or type of arguments being passed."
    if isinstance(exc, ValueError):
        return "A value reached code that could not parse or use it. Inspect the values on the highlighted line."
    if isinstance(exc, FileNotFoundError):
        return "Verify the path is correct relative to the project root."
    if name in {"OperationalError", "ProgrammingError"}:
        return "Check your database URL, schema, and whether migrations or init_db() have run."
    return "Inspect the highlighted line and the traceback frames below."


def render_debug_error_html(
    exc: Exception,
    request_path: Optional[str] = None,
    title: str = "NextPy Error",
) -> str:
    """Render a standalone, readable debug overlay with source context."""
    frames = _error_frames(exc)
    project_frames = [frame for frame in frames if frame["project"]]
    focus = project_frames[-1] if project_frames else (frames[-1] if frames else None)

    if focus:
        location = f"{focus['file']}:{focus['line']}"
        function = focus["function"]
        code_rows = _code_context(focus["file"], focus["line"])
    else:
        location = "unknown location"
        function = "unknown"
        code_rows = []

    code_html = ""
    for row in code_rows:
        line_class = "line current" if row["current"] else "line"
        code_html += (
            f'<div class="{line_class}">'
            f'<span class="ln">{row["number"]}</span>'
            f'<span class="src">{html.escape(row["source"])}</span>'
            "</div>"
        )
    if not code_html:
        code_html = '<div class="line"><span class="ln">-</span><span class="src">Source unavailable</span></div>'

    frame_html = ""
    for frame in frames:
        frame_class = "frame project" if frame["project"] else "frame"
        frame_html += (
            f'<div class="{frame_class}">'
            f'<span class="frame-file">{html.escape(frame["file"])}:{frame["line"]}</span>'
            f'<span class="frame-fn">in {html.escape(frame["function"])}</span>'
            f'<span class="frame-src">{html.escape(frame["source"])}</span>'
            "</div>"
        )

    traceback_text = "".join(
        traceback.format_exception(type(exc), exc, exc.__traceback__)
    )
    message = str(exc) or type(exc).__name__
    path_label = html.escape(request_path or "unknown")
    safe_message = html.escape(message)
    safe_location = html.escape(location)
    safe_function = html.escape(function)
    safe_suggestion = html.escape(_suggestion(exc))

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<style>
:root {{ color-scheme: dark; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; min-height: 100vh; background: #0b0d12; color: #e7eaf0;
       font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif; }}
.nextpy-error-overlay {{ min-height: 100vh; padding: 28px; background:
  radial-gradient(circle at 15% 0%, rgba(239,68,68,.16), transparent 34%),
  radial-gradient(circle at 90% 10%, rgba(168,85,247,.12), transparent 32%), #0b0d12; }}
.shell {{ max-width: 1080px; margin: 0 auto; }}
.top {{ display: flex; align-items: flex-start; justify-content: space-between; gap: 20px;
       padding-bottom: 18px; border-bottom: 1px solid #242936; }}
.brand {{ display: flex; align-items: center; gap: 12px; }}
.mark {{ width: 36px; height: 36px; border-radius: 10px; display: grid; place-items: center;
        background: linear-gradient(135deg, #ef4444, #f97316); color: white; font-weight: 800; }}
.brand h1 {{ margin: 0; font-size: 18px; letter-spacing: -.02em; }}
.brand p {{ margin: 2px 0 0; color: #8b93a7; font-size: 12px; }}
.actions {{ display: flex; gap: 8px; }}
.actions button {{ border: 1px solid #343a4a; background: #151923; color: #d7dce8;
                   border-radius: 8px; padding: 8px 12px; font-size: 12px; cursor: pointer; }}
.actions button:hover {{ background: #1d2330; }}
.type {{ margin-top: 24px; color: #f87171; font: 700 13px ui-monospace, SFMono-Regular, Menlo, monospace;
        text-transform: uppercase; letter-spacing: .08em; }}
.message {{ margin: 8px 0 0; font-size: clamp(20px, 3vw, 30px); line-height: 1.25;
           letter-spacing: -.02em; overflow-wrap: anywhere; }}
.meta {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 10px; margin-top: 20px; }}
.meta-card {{ background: #121620; border: 1px solid #242936; border-radius: 10px; padding: 12px 14px; }}
.meta-card .label {{ color: #7e879c; font-size: 10px; text-transform: uppercase; letter-spacing: .1em; }}
.meta-card .value {{ margin-top: 5px; font: 12px/1.5 ui-monospace, SFMono-Regular, Menlo, monospace;
                     color: #dbe2f0; overflow-wrap: anywhere; }}
.section {{ margin-top: 22px; background: #0f131b; border: 1px solid #242936; border-radius: 12px; overflow: hidden; }}
.section-title {{ padding: 12px 16px; border-bottom: 1px solid #242936; color: #aab2c5;
                  font-size: 12px; font-weight: 700; letter-spacing: .06em; text-transform: uppercase; }}
.code {{ overflow-x: auto; padding: 10px 0; background: #0b0e14; }}
.line {{ display: flex; min-width: max-content; font: 12.5px/1.75 ui-monospace, SFMono-Regular, Menlo, monospace; }}
.line .ln {{ width: 56px; flex: 0 0 56px; padding-right: 14px; text-align: right; color: #525b70; user-select: none; }}
.line .src {{ padding: 0 18px 0 10px; color: #c8d0e0; white-space: pre; }}
.line.current {{ background: rgba(239,68,68,.14); box-shadow: inset 3px 0 0 #ef4444; }}
.line.current .ln {{ color: #fca5a5; }}
.line.current .src {{ color: #fff; }}
.hint {{ margin-top: 18px; padding: 13px 15px; border: 1px solid rgba(245,158,11,.35);
         background: rgba(245,158,11,.08); border-radius: 10px; color: #fcd34d; font-size: 13px; line-height: 1.55; }}
.frames {{ max-height: 280px; overflow: auto; }}
.frame {{ display: grid; grid-template-columns: minmax(240px, 1.1fr) minmax(130px, .5fr) minmax(220px, 1fr);
          gap: 12px; padding: 9px 16px; border-bottom: 1px solid #1a1f2b; font-size: 11.5px; }}
.frame:last-child {{ border-bottom: 0; }}
.frame.project {{ background: rgba(239,68,68,.05); }}
.frame-file {{ font-family: ui-monospace, SFMono-Regular, Menlo, monospace; color: #9fb0d0; overflow-wrap: anywhere; }}
.frame-fn {{ color: #c084fc; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }}
.frame-src {{ color: #758096; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
.trace {{ margin: 0; padding: 14px 16px; max-height: 220px; overflow: auto; color: #9aa5bb;
          font: 11.5px/1.6 ui-monospace, SFMono-Regular, Menlo, monospace; white-space: pre-wrap; }}
.footer {{ margin-top: 18px; color: #5f687c; font-size: 11px; display: flex; justify-content: space-between; gap: 12px; }}
@media (max-width: 720px) {{ .nextpy-error-overlay {{ padding: 16px; }} .frame {{ grid-template-columns: 1fr; gap: 3px; }} }}
</style>
</head>
<body>
<div class="nextpy-error-overlay" data-nextpy-error-overlay="true">
  <div class="shell">
    <div class="top">
      <div class="brand">
        <div class="mark">N</div>
        <div><h1>NextPy Error</h1><p>Development overlay</p></div>
      </div>
      <div class="actions">
        <button onclick="location.reload()">Reload</button>
        <button onclick="document.querySelector('.nextpy-error-overlay').style.display='none'">Dismiss</button>
      </div>
    </div>
    <div class="type">{html.escape(type(exc).__name__)}</div>
    <div class="message">{safe_message}</div>
    <div class="meta">
      <div class="meta-card"><div class="label">Location</div><div class="value">{safe_location}</div></div>
      <div class="meta-card"><div class="label">Function</div><div class="value">{safe_function}</div></div>
      <div class="meta-card"><div class="label">Request</div><div class="value">{path_label}</div></div>
    </div>
    <div class="section">
      <div class="section-title">Code context</div>
      <div class="code">{code_html}</div>
    </div>
    <div class="hint">{safe_suggestion}</div>
    <div class="section">
      <div class="section-title">Traceback frames</div>
      <div class="frames">{frame_html or '<div class="frame"><span class="frame-file">No frames available</span></div>'}</div>
    </div>
    <div class="section">
      <div class="section-title">Full traceback</div>
      <pre class="trace">{html.escape(traceback_text)}</pre>
    </div>
    <div class="footer"><span>Fix the highlighted code, then reload.</span><span>NextPy development mode</span></div>
  </div>
</div>
</body>
</html>"""


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
