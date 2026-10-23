"""
NextPy Server Application - FastAPI-based server with complete PSX integration
Handles routing, SSR, API routes, and static file serving using PSX for everything
"""

import os
import re
import sys
import asyncio
import hashlib
import importlib.util
import types
from pathlib import Path
from typing import Any, Callable, Dict, Optional

from fastapi import FastAPI, Request, Response, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from starlette.websockets import WebSocketState

# Import PSX for complete integration
sys.path.insert(0, str(Path(__file__).parent.parent))
from nextpy.psx import (
    compile_psx, render_psx, psx, PSXElement, component,
    useState, useEffect, process_python_logic,
    VNode, create_element, render, update, CLIENT_ROUTER_SCRIPT, CRUD_RUNTIME_SCRIPT
)

from nextpy.core.router import Router
from nextpy.core.component_router import ComponentRouter, ComponentRoute
from nextpy.core.demo_router import demo_router
from nextpy.core.component_renderer import ComponentRenderer, render_api, render_component
from nextpy.core.data_fetching import (
    PageContext,
    execute_data_fetching,
    execute_data_fetching_result,
    PageNotFoundError,
    RedirectError,
)
from nextpy.server.middleware import NextPyMiddleware, CSRFMiddleware, RateLimitMiddleware
from nextpy.security import security_manager
from nextpy.jsx_preprocessor import JSXSyntaxError
from nextpy.websocket import manager, handle_websocket
from nextpy.api import api
from nextpy.server_actions import ServerAction


_api_app: Optional[FastAPI] = None


def get_api_app() -> FastAPI:
    """Return the FastAPI instance created by :func:`create_app`."""
    if _api_app is None:
        raise RuntimeError("NextPy app is not initialized yet")
    return _api_app


class NextPyApp:
    """
    Enhanced NextPy application class with complete PSX integration
    Wraps FastAPI and provides Next.js-like functionality using PSX for all rendering
    """
    
    def __init__(
        self,
        pages_dir: str = "pages",
        templates_dir: str = "templates",
        public_dir: str = "public",
        out_dir: str = "out",
        debug: bool = False,
        admin_site: Any = None,
    ):
        self.pages_dir = Path(pages_dir)
        self.templates_dir = Path(templates_dir)
        self.public_dir = Path(public_dir)
        self.out_dir = Path(out_dir)
        self.debug = debug
        self.admin_site = admin_site
        self._modules_cache: Dict[str, Any] = {}
        
        if demo_router.should_serve_demo():
            self.router = Router(str(self.pages_dir), str(self.templates_dir))
        else:
            self.router = ComponentRouter(str(self.pages_dir), str(self.templates_dir))
            if hasattr(self.router, "renderer"):
                self.router.renderer.debug = debug
        # keep separate renderers for templates (Jinja) and components
        from ..core import Renderer
        self.template_renderer = Renderer(
            templates_dir=str(self.templates_dir),
            pages_dir=str(self.pages_dir),
            public_dir=str(self.public_dir),
        )
        self.component_renderer = ComponentRenderer(
            debug=debug
        )
        
        # Scan pages for routes
        self.router.scan_pages()
        
        # Check if we should enable demo mode
        if isinstance(self.router, Router) and demo_router.should_serve_demo():
            self.router.enable_demo_mode()
            print("🎉 NextPy Demo Mode - No project detected")
            print("📚 Showing built-in documentation and examples")
            print("💡 Create a project with: nextpy create my-app")
        
        self.app = FastAPI(
            title="NextPy Application",
            debug=debug,
        )
        
        self._setup_middleware()
        self._setup_static_files()
        self._setup_websocket()
        self._load_project_api()
        # Mount declarative application API routes before file-based routes.
        self.app.include_router(api)
        # Mount protected admin routes before page routes so a dynamic page
        # cannot capture /admin.
        if self.admin_site is not None:
            self.admin_site.mount(self.app)
        self._setup_routes()
        # optionally compile tailwind CSS after routes are registered
        try:
            self._ensure_tailwind_compiled()
        except Exception as e:
            if self.debug:
                print(f"Tailwind check/build failed: {e}")
        
    def _setup_middleware(self) -> None:
        """Configure middleware with secure defaults."""
        cors_env = os.getenv("CORS_ORIGINS", "").strip()
        cors_origins = [origin.strip() for origin in cors_env.split(",") if origin.strip()]
        if not cors_origins:
            cors_origins = ["*"]
        allow_credentials = cors_origins != ["*"]

        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=cors_origins,
            allow_credentials=allow_credentials,
            allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
            allow_headers=["*"],
        )

        self.app.add_middleware(NextPyMiddleware)

        csrf_origins = [
            origin for origin in cors_origins if origin != "*"
        ]
        csrf_env = os.getenv("CSRF_TRUSTED_ORIGINS", "").strip()
        if csrf_env:
            csrf_origins.extend(
                origin.strip() for origin in csrf_env.split(",") if origin.strip()
            )
        self.app.add_middleware(
            CSRFMiddleware,
            allowed_origins=csrf_origins,
            enabled=os.getenv("CSRF_PROTECTION", "true").lower()
            in {"1", "true", "yes", "on"},
        )

        try:
            rate_limit = int(os.getenv("RATE_LIMIT_PER_MINUTE", "240"))
            auth_rate_limit = int(os.getenv("AUTH_RATE_LIMIT_PER_MINUTE", "60"))
        except ValueError:
            rate_limit, auth_rate_limit = 240, 60
        self.app.add_middleware(
            RateLimitMiddleware,
            limit_per_minute=rate_limit,
            auth_limit_per_minute=auth_rate_limit,
            enabled=os.getenv("RATE_LIMIT_ENABLED", "true").lower()
            in {"1", "true", "yes", "on"},
        )

        # Add security headers middleware
        @self.app.middleware("http")
        async def add_security_headers(request: Request, call_next):
            response = await call_next(request)

            # Add Content Security Policy
            csp_header = security_manager.create_csp_header()
            response.headers["Content-Security-Policy"] = csp_header

            # Add other security headers
            response.headers["X-Content-Type-Options"] = "nosniff"
            response.headers["X-Frame-Options"] = "DENY"
            response.headers["X-XSS-Protection"] = "1; mode=block"
            response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
            response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
            response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
            response.headers["Cross-Origin-Resource-Policy"] = "same-origin"
            response.headers["X-Permitted-Cross-Domain-Policies"] = "none"
            if request.url.scheme == "https":
                response.headers["Strict-Transport-Security"] = (
                    "max-age=31536000; includeSubDomains"
                )

            return response
        
    def _setup_static_files(self) -> None:
        """Mount static file directories"""
        if self.public_dir.exists():
            # Mount public directory under /static to avoid intercepting all
            # requests. Mounting at "/" previously caused every request to be
            # handled by StaticFiles first, which returned 404 for dynamic
            # pages and API routes.  In a future release we might add a
            # middleware that checks for a file in `public_dir` and serves it
            # before falling back to the app, thus preserving Next.js semantics.
            self.app.mount(
                "/static",
                StaticFiles(directory=str(self.public_dir)),
                name="public",
            )
            # Ensure commonly referenced compiled Tailwind CSS paths are
            # available. Templates may link to `/tailwind.css` or
            # `/public/tailwind.css`; mounting under `/static` would
            # expose the file at `/static/tailwind.css`. For compatibility
            # add explicit routes that serve the compiled file if present.
            try:
                tailwind_file = self.public_dir / "tailwind.css"
                if tailwind_file.exists():
                    from starlette.responses import FileResponse

                    def _tailwind(request, _path=str(tailwind_file)):
                        return FileResponse(_path)

                    # Register both commonly used locations
                    self.app.add_route("/tailwind.css", _tailwind, methods=["GET"])
                    self.app.add_route("/public/tailwind.css", _tailwind, methods=["GET"])
            except Exception:
                # Non-fatal: continue if registration fails
                pass
        nextpy_static = self.out_dir / "_nextpy" / "static"
        if nextpy_static.exists():
            self.app.mount(
                "/_nextpy/static",
                StaticFiles(directory=str(nextpy_static)),
                name="nextpy_static",
            )
            
    def _setup_websocket(self) -> None:
        """Setup WebSocket endpoint for live development tools"""
        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            """Handle WebSocket connections for live development"""
            origin = websocket.headers.get("origin")
            trusted = [
                origin_value.strip()
                for origin_value in os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",")
                if origin_value.strip()
            ]
            if origin and not security_manager.is_trusted_origin(
                origin, websocket.url.netloc, trusted
            ):
                await websocket.close(code=1008)
                return
            await handle_websocket(websocket)
    
    def _load_project_api(self) -> None:
        """Load project API modules before mounting the native API router.

        Both ``api.py`` and ``pages/api.py`` are supported. The latter is
        useful for projects that keep all route-facing Python files together
        under ``pages``; the ``pages/api/`` directory remains file-based API
        routing and is scanned separately.
        """
        api_files = [Path.cwd() / "api.py", self.pages_dir / "api.py"]
        for index, api_file in enumerate(api_files):
            if not api_file.exists():
                continue
            module_name = f"_nextpy_project_api_{index}"
            if module_name in sys.modules:
                continue
            spec = importlib.util.spec_from_file_location(module_name, api_file)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)
            
    def _add_seo_routes(self) -> None:
        """Add special SEO routes for sitemap.xml and robots.txt"""
        from fastapi import Request
        from fastapi.responses import Response
        
        # Sitemap.xml route
        async def sitemap_handler(request: Request):
            try:
                # Try to load the sitemap module
                sitemap_module = self._load_module_from_file(Path("pages/sitemap.xml.py"))
                if sitemap_module and hasattr(sitemap_module, 'get_server_side_props'):
                    context = PageContext(
                        params={},
                        query=dict(request.query_params),
                        req=request,
                    )
                    result = await sitemap_module.get_server_side_props(context)
                    
                    # Return the Response directly
                    return result
                else:
                    # Fallback sitemap
                    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
                    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                    xml += '  <url>\n'
                    xml += f'    <loc>https://nextpy-framework.onrender.com/</loc>\n'
                    xml += f'    <lastmod>2026-03-06</lastmod>\n'
                    xml += '    <changefreq>daily</changefreq>\n'
                    xml += '    <priority>1.0</priority>\n'
                    xml += '  </url>\n'
                    xml += '</urlset>'
                    return Response(content=xml, media_type="application/xml")
            except Exception as e:
                if self.debug:
                    print(f"Error generating sitemap: {e}")
                # Return minimal sitemap on error
                xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
                xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                xml += '  <url>\n'
                xml += f'    <loc>https://nextpy-framework.onrender.com/</loc>\n'
                xml += '  </url>\n'
                xml += '</urlset>'
                return Response(content=xml, media_type="application/xml")
        
        # Robots.txt route
        async def robots_handler(request: Request):
            try:
                # Try to load the robots module
                robots_module = self._load_module_from_file(Path("pages/robots.txt.py"))
                if robots_module and hasattr(robots_module, 'get_server_side_props'):
                    context = PageContext(
                        params={},
                        query=dict(request.query_params),
                        req=request,
                    )
                    result = await robots_module.get_server_side_props(context)
                    
                    # Return the Response directly
                    return result
                else:
                    # Fallback robots.txt
                    robots_content = """User-agent: *
Allow: /

Sitemap: https://nextpy-framework.onrender.com/sitemap.xml
"""
                    return Response(content=robots_content, media_type="text/plain")
            except Exception as e:
                if self.debug:
                    print(f"Error generating robots.txt: {e}")
                # Return minimal robots.txt on error
                robots_content = """User-agent: *
Allow: /
"""
                return Response(content=robots_content, media_type="text/plain")
        
        # Register the SEO routes
        self.app.add_route("/sitemap.xml", sitemap_handler, methods=["GET"])
        self.app.add_route("/robots.txt", robots_handler, methods=["GET"])
        
        # Add debug API routes
        self._add_debug_routes()
        
        # Add server actions endpoint
        self._add_server_actions_routes()
            
    def _add_debug_routes(self) -> None:
        """Add debug API routes for the debug panel"""
        
        # Debug components endpoint
        async def debug_components(request: Request):
            try:
                # Import debug core to get component data
                from ..debug.core import debug_core
                components = debug_core.get_all_components() if debug_core else {}
                return JSONResponse(components)
            except ImportError:
                return JSONResponse({})
            except Exception as e:
                if self.debug:
                    print(f"Debug components error: {e}")
                return JSONResponse({})
        
        # Debug events endpoint
        async def debug_events(request: Request):
            try:
                from ..debug.core import debug_core
                events = debug_core.get_recent_events() if debug_core else []
                return JSONResponse(events)
            except ImportError:
                return JSONResponse([])
            except Exception as e:
                if self.debug:
                    print(f"Debug events error: {e}")
                return JSONResponse([])
        
        # Debug performance endpoint
        async def debug_performance(request: Request):
            try:
                from ..debug.performance import performance_monitor
                metrics = performance_monitor.get_all_metrics() if performance_monitor else {}
                return JSONResponse(metrics)
            except ImportError:
                return JSONResponse({})
            except Exception as e:
                if self.debug:
                    print(f"Debug performance error: {e}")
                return JSONResponse({})
        
        # Debug WebSocket endpoint
        async def debug_websocket(request: Request):
            try:
                from ..debug.websocket import websocket_tracker
                status = websocket_tracker.get_status() if websocket_tracker else {"connected": False, "client_id": None}
                return JSONResponse(status)
            except ImportError:
                return JSONResponse({"connected": False, "client_id": None})
            except Exception as e:
                if self.debug:
                    print(f"Debug WebSocket error: {e}")
                return JSONResponse({"connected": False, "client_id": None})
        
        # Debug session start endpoint
        async def debug_start_session(request: Request):
            try:
                import time
                from ..debug.core import start_debug_session
                session_data = start_debug_session() if start_debug_session else {"session_id": "mock_session", "start_time": time.time()}
                return JSONResponse(session_data)
            except ImportError:
                import time
                return JSONResponse({"session_id": "mock_session", "start_time": time.time()})
            except Exception as e:
                if self.debug:
                    print(f"Debug start session error: {e}")
                import time
                return JSONResponse({"session_id": "mock_session", "start_time": time.time()})
        
        # Debug session end endpoint
        async def debug_end_session(request: Request):
            try:
                from ..debug.core import end_debug_session
                summary = end_debug_session() if end_debug_session else {"mock": "summary"}
                return JSONResponse(summary)
            except ImportError:
                return JSONResponse({"mock": "summary"})
            except Exception as e:
                if self.debug:
                    print(f"Debug end session error: {e}")
                return JSONResponse({"mock": "summary"})
        
        # Debug export endpoint
        async def debug_export(request: Request):
            try:
                import time
                from ..debug.core import debug_core
                data = {
                    "components": debug_core.get_all_components() if debug_core else {},
                    "events": debug_core.get_recent_events() if debug_core else [],
                    "timestamp": time.time()
                }
                return JSONResponse(data)
            except Exception as e:
                if self.debug:
                    print(f"Debug export error: {e}")
                return JSONResponse({})
        
        # Debug clear endpoint
        async def debug_clear(request: Request):
            try:
                from ..debug.core import debug_core
                if debug_core:
                    debug_core.clear_data()
                return JSONResponse({"success": True})
            except ImportError:
                return JSONResponse({"success": True})
            except Exception as e:
                if self.debug:
                    print(f"Debug clear error: {e}")
                return JSONResponse({"success": True})
        
        # Register all debug routes
        self.app.add_route("/__nextpy/debug/components", debug_components, methods=["GET"])
        self.app.add_route("/__nextpy/debug/events", debug_events, methods=["GET"])
        self.app.add_route("/__nextpy/debug/performance", debug_performance, methods=["GET"])
        self.app.add_route("/__nextpy/debug/websocket", debug_websocket, methods=["GET"])
        self.app.add_route("/__nextpy/debug/start", debug_start_session, methods=["POST"])
        self.app.add_route("/__nextpy/debug/end", debug_end_session, methods=["POST"])
        self.app.add_route("/__nextpy/debug/export", debug_export, methods=["GET"])
        self.app.add_route("/__nextpy/debug/clear", debug_clear, methods=["POST"])
            
    def _add_server_actions_routes(self) -> None:
        """Add server actions API endpoints for enhanced client-server communication"""
        
        # List all available server actions
        async def list_actions(request: Request):
            try:
                actions = ServerAction.list_actions()
                return JSONResponse({
                    "actions": actions,
                    "count": len(actions)
                })
            except Exception as e:
                if self.debug:
                    print(f"Server actions list error: {e}")
                return JSONResponse({"error": str(e)}, status_code=500)
        
        # Execute a server action
        from fastapi.responses import Response as FastAPIResponse
        
        async def execute_action(request: Request):
            try:
                data = await request.json()
                action_name = data.get("action")
                params = data.get("params", {})
                
                if not action_name:
                    return JSONResponse({"error": "action name is required"}, status_code=400)
                
                # Create a response object so actions can set cookies/headers
                action_response = FastAPIResponse()
                result = await ServerAction.execute(action_name, request, response=action_response, params=params)
                
                # Build the JSON response with cookies from action_response
                json_response = JSONResponse(result)
                # Copy any cookies set by the action
                for cookie in action_response.headers.getlist("set-cookie"):
                    json_response.headers.append("set-cookie", cookie)
                # Copy any headers set by the action
                for key, value in action_response.headers.items():
                    if key not in ("set-cookie", "content-type", "content-length"):
                        json_response.headers.append(key, value)
                
                return json_response
                
            except HTTPException as exc:
                return JSONResponse(
                    {"error": exc.detail, "success": False},
                    status_code=exc.status_code,
                )
            except Exception as e:
                if self.debug:
                    import traceback
                    traceback.print_exc()
                return JSONResponse({"error": str(e)}, status_code=500)
        
        # Get server action schema
        async def get_action_schema(request: Request, action_name: str):
            try:
                action = ServerAction.get_action(action_name)
                if not action:
                    return JSONResponse({"error": "action not found"}, status_code=404)
                
                # Get type hints for schema
                import inspect
                original = getattr(action, '_original_func', action)
                hints = inspect.get_type_hints(original)
                
                return JSONResponse({
                    "name": action_name,
                    "schema": hints,
                    "doc": action.__doc__
                })
            except Exception as e:
                if self.debug:
                    print(f"Action schema error: {e}")
                return JSONResponse({"error": str(e)}, status_code=500)
        
        # Register server action routes
        self.app.add_route("/__nextpy/actions", list_actions, methods=["GET"])
        self.app.add_route("/__nextpy/actions/execute", execute_action, methods=["POST"])
        self.app.add_route("/__nextpy/actions/{action_name}/schema", get_action_schema, methods=["GET"])
            
    def _convert_route_to_fastapi_path(self, route_path: str) -> str:
        """Convert router path with regex patterns to FastAPI-compatible path"""
        import re
        # Convert (?P<name>pattern) to {name}
        fastapi_path = re.sub(r'\(\?P<(\w+)>[^)]+\)', r'{\1}', route_path)
        return fastapi_path

    def _setup_routes(self) -> None:
        """Setup page routes using the router"""
        
        # Add special SEO routes
        self._add_seo_routes()
        
        # Add all routes from the router
        for route in self.router.get_all_routes():
            if route.is_api:
                # API routes - FIXED: use default argument to capture route correctly
                from fastapi import Request
                def create_api_handler(route_obj):
                    async def api_handler(request: Request):
                        # ``route_obj`` is captured in the closure.  Using it as
                        # a default parameter made FastAPI treat the Route as a
                        # query default and try to deepcopy it, which fails for
                        # routes that reference modules.  ``**kwargs`` is not
                        # supported by FastAPI dependency injection either, so
                        # read path params from the request.
                        return await self._handle_api_request(
                            request, route_obj, dict(request.path_params)
                        )
                    return api_handler
                
                fastapi_path = self._convert_route_to_fastapi_path(route.path)
                self.app.add_api_route(
                    fastapi_path,
                    create_api_handler(route),
                    methods=["GET", "HEAD", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"]
                )
            else:
                # Page routes - FIXED: use default argument to capture route correctly
                def create_page_handler(route_path):
                    async def page_handler(request, **path_params):
                        # FastAPI has already matched dynamic segments. Match the
                        # actual URL again so the framework router can resolve
                        # the slug and provide it to page data fetching.
                        return await self._handle_request(request, request.url.path)
                    return page_handler
                
                fastapi_path = self._convert_route_to_fastapi_path(route.path)
                self.app.add_route(
                    fastapi_path,
                    create_page_handler(route.path),
                    methods=["GET", "HEAD", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"]
                )
        
    def _load_module_from_file(self, file_path: Path, module_name: Optional[str] = None) -> Any:
        """Enhanced module loader with complete PSX support"""
        if not file_path.exists():
            return None
            
        module_name = module_name or file_path.stem
        cache_key = str(file_path)
        
        # Check cache first (unless in debug mode)
        if not self.debug and cache_key in self._modules_cache:
            return self._modules_cache[cache_key]
        
        try:
            # Check if this is a PSX/JSX file before trying PSX loader.
            # API modules must use the normal Python/JSX transformer so
            # ``get``/``post`` handlers remain importable; the PSX page
            # compiler returns a callable component wrapper instead.
            is_api_file = "api" in file_path.parts
            is_psx_file = (
                file_path.suffix in ['.psx'] or file_path.name.endswith('.jsx')
            ) and not is_api_file
            
            # Try PSX loader only for PSX files (preferred method)
            if is_psx_file:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Compile PSX content
                    compiled = compile_psx(content)
                    
                    # Create a module-like object
                    class PSXModule:
                        def __init__(self, compiled_func):
                            self.compiled = compiled_func
                            self.__name__ = module_name
                            self.__file__ = str(file_path)
                        
                        def __call__(self, **kwargs):
                            return self.compiled(**kwargs)
                    
                    module = PSXModule(compiled)
                    
                    # Cache the module (unless in debug mode)
                    if not self.debug:
                        self._modules_cache[cache_key] = module
                    
                    return module
                    
                except ImportError:
                    pass  # PSX not available, fall back to other methods
                except Exception:
                    pass  # PSX compilation failed, fall back to other methods
            
            # API modules written as .psx are plain Python handlers. Compile
            # them directly because spec_from_file_location does not recognize
            # the .psx extension.
            if is_api_file and file_path.suffix == ".psx":
                module = types.ModuleType(module_name)
                module.__file__ = str(file_path)
                code = compile(
                    file_path.read_text(encoding="utf-8"),
                    str(file_path),
                    "exec",
                )
                exec(code, module.__dict__)
                if not self.debug:
                    self._modules_cache[cache_key] = module
                return module

            # Try JSX transformer for backward compatibility
            try:
                from nextpy.jsx_transformer import JSXTransformer
                transformer = JSXTransformer()
                module = transformer.load_jsx_module(file_path, module_name)
                
                if module:
                    # Cache the module (unless in debug mode)
                    if module and not self.debug:
                        self._modules_cache[cache_key] = module
                    
                    return module
                    
            except Exception:
                pass
            
            # Fallback to regular Python import
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Cache the module (unless in debug mode)
                if not self.debug:
                    self._modules_cache[cache_key] = module
                
                return module
            
        except Exception as e:
            if self.debug:
                print(f"Error loading module from {file_path}: {e}")
            return None
        
    @staticmethod
    def _mark_internal_links(html_text: str) -> str:
        """Add SPA navigation attributes to internal anchors.

        Also strips HTMX navigation attributes so the client router is the
        single navigation mechanism (prevents duplicate requests).
        """
        def _replace(match):
            full_tag = match.group(0)
            if 'data-nextpy-link' in full_tag:
                return full_tag
            href_match = re.search(r'href=["\']([^"\']*)["\']', full_tag)
            if not href_match:
                return full_tag
            href = href_match.group(1)
            if not (href.startswith('/') or href.startswith('#')):
                return full_tag
            target_match = re.search(r'(?<![-\w])target=["\']([^"\']*)["\']', full_tag)
            if target_match and target_match.group(1) != '_self':
                return full_tag

            cleaned = re.sub(
                r'\s(?:hx-get|hx-target|hx-swap|hx-push-url|hx-trigger|preload)=["\'][^"\']*["\']',
                '',
                full_tag,
            )
            return cleaned.replace(
                '<a ',
                '<a data-nextpy-link="true" data-nextpy-prefetch="true" ',
                1,
            )

        return re.sub(r'<a\b[^>]*>', _replace, html_text)

    @staticmethod
    def _inject_inline_script(
        html: str, script: str, name: str = "runtime", marker: Optional[str] = None
    ) -> str:
        """Insert an inline script before </body> instead of after </html>.

        Injected scripts carry ``data-nextpy-runtime`` so the client router
        never re-executes them during a full-page swap.
        """
        marker = marker or f'data-nextpy-runtime="{name}"'
        if marker in html:
            return html
        tag = f'<script data-nextpy-runtime="{name}">{script}</script>'
        index = html.lower().rfind('</body>')
        if index != -1:
            return html[:index] + tag + html[index:]
        return html + tag

    @staticmethod
    def _inject_layout_signature(html: str, signature: str) -> str:
        """Expose the layout signature so the client can request fragments."""
        if 'nextpy-layout' in html:
            return html
        marker = f'<meta name="nextpy-layout" content="{signature}">'
        lower = html.lower()
        index = lower.find('</head>')
        if index != -1:
            return html[:index] + marker + html[index:]
        return marker + html

    @staticmethod
    def _page_headers(cacheable: bool, html: str) -> Dict[str, str]:
        etag = '"' + hashlib.md5(html.encode('utf-8')).hexdigest() + '"'
        if cacheable:
            return {
                'Cache-Control': 'private, max-age=30, stale-while-revalidate=120',
                'ETag': etag,
                'X-NextPy-Cacheable': 'true',
            }
        return {
            'Cache-Control': 'no-store',
            'ETag': etag,
            'X-NextPy-Cacheable': 'false',
        }

    @staticmethod
    def _not_modified(request: Request, headers: Dict[str, str]) -> Optional[Response]:
        etag = headers.get('ETag')
        if not etag:
            return None
        if_none_match = request.headers.get('if-none-match', '')
        candidates = {value.strip() for value in if_none_match.split(',')}
        if etag in candidates or if_none_match.strip() == '*':
            return Response(status_code=304, headers=headers)
        return None

    async def _handle_request(self, request: Request, path: str) -> Response:
        """Handle a page request"""
        match = self.router.match(path)
        
        if not match:
            return await self._render_404(request)
            
        route, params = match
        
        # Handle demo pages differently
        if hasattr(self.router, "is_demo_mode") and self.router.is_demo_mode() and str(route.file_path) == "demo":
            return await self._handle_demo_page(request, route, params)
        
        if route.is_api:
            return await self._handle_api_request(request, route, params)
            
        if isinstance(route, ComponentRoute) and getattr(route, "use_components", False):
            context = {
                "params": params,
                "query": dict(request.query_params),
                "request": request,
            }

            module = self._load_module_from_file(route.file_path)
            if module:
                try:
                    page_context = PageContext(
                        params=params,
                        query=dict(request.query_params),
                        req=request,
                    )
                    fetched_props, page_revalidate = await execute_data_fetching_result(module, page_context)
                    context.update(fetched_props)
                    context["__nextpy_props_loaded"] = True
                    if page_revalidate is not None and hasattr(route, "renderer"):
                        route.renderer.revalidate_cache[str(route.file_path)] = int(page_revalidate)
                except Exception as e:
                    if self.debug:
                        print(f"Data fetching error for component route: {e}")

            layout_sig = self.router.get_layout_signature(route)
            want_fragment = (
                request.headers.get("x-nextpy-fragment", "").lower() == "true"
                and request.headers.get("x-nextpy-layout-sig", "") == layout_sig
            )
            cacheable = self.router.is_cacheable(route, context)

            stream_enabled = bool(getattr(module, "streaming", False)) if module else False
            custom_stream = bool(module and callable(getattr(module, "stream", None)))
            if (stream_enabled or custom_stream) and not want_fragment:
                from nextpy.core.streaming import chunk_html

                if custom_stream:
                    async def _stream_body():
                        async for chunk in self.router.render_route_stream(
                            route, context, include_layout=True
                        ):
                            yield chunk
                else:
                    stream_html = self.router.render_route(
                        route, context, include_layout=True
                    )
                    if '<a ' in stream_html:
                        stream_html = self._mark_internal_links(stream_html)
                    stream_html = self._inject_layout_signature(stream_html, layout_sig)
                    if 'data-nextpy-crud' in stream_html:
                        stream_html = self._inject_inline_script(
                            stream_html, CRUD_RUNTIME_SCRIPT, 'crud'
                        )
                    stream_html = self._inject_inline_script(
                        stream_html, CLIENT_ROUTER_SCRIPT, 'router'
                    )

                    async def _stream_body():
                        for chunk in chunk_html(stream_html):
                            yield chunk

                headers = {
                    "Cache-Control": "no-cache",
                    "X-NextPy-Streaming": "true",
                    "X-NextPy-Layout-Sig": layout_sig,
                }
                if cacheable:
                    isr_ttl = self.router.get_revalidate(route) or self.router._cache_ttl
                    headers["Cache-Control"] = (
                        f"public, max-age=0, s-maxage={int(isr_ttl)}, "
                        f"stale-while-revalidate={int(isr_ttl)}"
                    )
                    headers["X-NextPy-ISR"] = "true"
                return StreamingResponse(
                    _stream_body(), media_type="text/html", headers=headers
                )

            html = self.router.render_route(
                route, context, include_layout=not want_fragment
            )

            if '<a ' in html:
                html = self._mark_internal_links(html)

            if not want_fragment:
                html = self._inject_layout_signature(html, layout_sig)
                if 'data-nextpy-crud' in html:
                    html = self._inject_inline_script(
                        html, CRUD_RUNTIME_SCRIPT, 'crud'
                    )
                html = self._inject_inline_script(
                    html, CLIENT_ROUTER_SCRIPT, 'router'
                )

            is_error_html = (
                'data-nextpy-error-overlay="true"' in html
                or 'data-nextpy-error="true"' in html
                or html.lstrip().startswith("<h1>Error rendering route:")
            )
            if is_error_html:
                cacheable = False

            headers = self._page_headers(cacheable, html)
            headers["X-NextPy-Layout-Sig"] = layout_sig
            if want_fragment:
                headers["X-NextPy-Fragment"] = "true"
                title = context.get("title")
                if title:
                    headers["X-NextPy-Title"] = str(title)

            status_code = 500 if is_error_html else 200
            if status_code == 500:
                headers["Cache-Control"] = "no-store"

            not_modified = self._not_modified(request, headers)
            if not_modified is not None:
                return not_modified

            return HTMLResponse(content=html, headers=headers, status_code=status_code)
            
        context = PageContext(
            params=params,
            query=dict(request.query_params),
            req=request,
        )
        
        try:
            props = {}
            component_props = {"params": params}
            module = self._load_module_from_file(route.file_path)
            
            if module:
                props = await execute_data_fetching(module, context)
                component_props = {**props, "params": params}
                
                # Execute the page component to get JSX
                content = ""
                if hasattr(module, 'default'):
                    component = module.default
                    component_props = {**props, "params": params}
                    jsx_element = component(component_props)
                    
                    # Convert JSX/PSX to HTML
                    try:
                        # Try PSX renderer first (preferred)
                        from nextpy.psx import render_psx_component
                        content = render_psx_component(jsx_element, component_props)
                    except ImportError:
                        # Fallback to old JSX renderer
                        try:
                            from nextpy.jsx import render_jsx
                            content = render_jsx(jsx_element)
                        except ImportError:
                            # Fail fast - renderer is required
                            raise RuntimeError("Neither PSX nor JSX renderer available. Please install nextpy.psx module.")
                
                # Apply layout chain (inside-out order)
                if hasattr(route, 'layout_chain') and route.layout_chain:
                    for layout_path in route.layout_chain:
                        layout_func = self.router._load_layout(layout_path)
                        if layout_func:
                            try:
                                # Wrap content with layout
                                layout_element = layout_func(children=content, **component_props)
                                from nextpy.psx import render_psx_component
                                content = render_psx_component(layout_element, component_props)
                            except Exception as e:
                                print(f"Warning: Failed to apply layout {layout_path}: {e}")
                        
            template_name = self._get_template_name(route, module)
            
            html = await self.template_renderer.render_async(
                template_name,
                context={
                    **props,
                    "content": content,
                    "params": params,
                    "query": dict(request.query_params),
                    "request": request,
                },
            )
            
            # Auto-add data-nextpy-link to internal <a> tags for client-side navigation
            if '<a ' in html:
                html = self._mark_internal_links(html)

            # Inject the client-side router on every full page so SPA
            # navigation works even when the first page has no anchors.
            html = self._inject_inline_script(
                html, CLIENT_ROUTER_SCRIPT, 'router'
            )

            cacheable = (
                not request.cookies
                and not request.headers.get('authorization')
                and not (module is not None and hasattr(module, 'getServerSideProps'))
            )
            headers = self._page_headers(cacheable, html)
            not_modified = self._not_modified(request, headers)
            if not_modified is not None:
                return not_modified

            return HTMLResponse(content=html, headers=headers)
            
        except PageNotFoundError:
            return await self._render_404(request)
            
        except RedirectError as e:
            status_code = 308 if e.permanent else 307
            return RedirectResponse(url=e.destination, status_code=status_code)
            
        except Exception as e:
            if self.debug:
                import traceback
                traceback.print_exc()
            return await self._render_error(request, e)
            
    async def _handle_api_request(
        self, 
        request: Request, 
        route,
        params: Optional[Dict[str, str]] = None
    ) -> Response:
        """Dispatch a file-based API request to the correct HTTP method.

        Supports GET, POST, PUT, PATCH, DELETE, HEAD and OPTIONS, dynamic path
        parameters, tuple returns ``(body, status)`` / ``(body, status, headers)``
        and FastAPI ``HTTPException`` responses.
        """
        params = params or {}

        module = self._load_module_from_file(route.file_path)
        if not module:
            return JSONResponse(
                {"error": "Module not found"},
                status_code=500,
            )

        method = request.method.upper()
        handler = (
            getattr(module, method.lower(), None)
            or getattr(module, method, None)
        )

        # A module-level ``handler`` is an explicit catch-all; ``default`` is a
        # page component and must never be used as an API fallback.
        if handler is None and method != "OPTIONS":
            handler = getattr(module, "handler", None)

        if handler is None and method == "HEAD":
            handler = getattr(module, "get", None) or getattr(module, "GET", None)

        if handler is None:
            allowed = self._api_allowed_methods(module)
            if method == "OPTIONS":
                return Response(status_code=204, headers={"Allow": ", ".join(allowed)})
            return JSONResponse(
                {"error": f"Method {method} not allowed for this endpoint"},
                status_code=405,
                headers={"Allow": ", ".join(allowed)},
            )

        try:
            result = await self._call_api_handler(handler, request, params)

            status_code = 200
            headers = None
            if isinstance(result, tuple):
                if len(result) == 2:
                    result, status_code = result
                elif len(result) == 3:
                    result, status_code, headers = result

            if isinstance(result, Response):
                return result
            if result is None:
                return Response(status_code=status_code if status_code != 200 else 204)
            if isinstance(result, (dict, list, str, int, float, bool)):
                response = JSONResponse(result, status_code=status_code)
            else:
                response = JSONResponse({"data": result}, status_code=status_code)
            if headers:
                for key, value in headers.items():
                    response.headers[key] = str(value)
            return response

        except HTTPException as exc:
            return JSONResponse(
                {"detail": exc.detail},
                status_code=exc.status_code,
                headers=exc.headers,
            )
        except RequestValidationError as exc:
            return JSONResponse(
                {"detail": exc.errors()},
                status_code=422,
            )
        except (KeyError, ValueError, TypeError) as exc:
            if self.debug:
                import traceback
                traceback.print_exc()
            return JSONResponse(
                {"error": str(exc) if self.debug else "Invalid request"},
                status_code=400,
            )
        except Exception as exc:
            if self.debug:
                import traceback
                traceback.print_exc()
            return JSONResponse(
                {"error": str(exc) if self.debug else "Internal server error"},
                status_code=500,
            )

    @staticmethod
    def _api_allowed_methods(module: Any) -> list:
        methods = []
        for method in ("GET", "POST", "PUT", "PATCH", "DELETE", "HEAD"):
            if hasattr(module, method.lower()) or hasattr(module, method):
                methods.append(method)
        if "GET" in methods and "HEAD" not in methods:
            methods.append("HEAD")
        methods.append("OPTIONS")
        return methods

    @staticmethod
    async def _call_api_handler(handler: Callable, request: Request, params: Dict[str, str]) -> Any:
        """Call an API handler with the arguments its signature declares."""
        import inspect

        try:
            signature = inspect.signature(handler)
            parameters = signature.parameters
        except (TypeError, ValueError):
            parameters = {}

        positional = [
            p for p in parameters.values()
            if p.kind in (
                inspect.Parameter.POSITIONAL_ONLY,
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
            )
        ]
        has_var_kwargs = any(
            p.kind == inspect.Parameter.VAR_KEYWORD for p in parameters.values()
        )

        def coerce(value: Any, annotation: Any) -> Any:
            if annotation in (int, "int"):
                return int(value)
            if annotation in (float, "float"):
                return float(value)
            if annotation in (bool, "bool"):
                return str(value).lower() in {"1", "true", "yes", "on"}
            return value

        kwargs = {}
        for name, value in params.items():
            if name in parameters and parameters[name].kind in (
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
                inspect.Parameter.KEYWORD_ONLY,
            ):
                kwargs[name] = coerce(value, parameters[name].annotation)

        if has_var_kwargs:
            call = lambda: handler(request, **kwargs)  # noqa: E731
        elif "params" in parameters:
            call = lambda: handler(request, params)  # noqa: E731
        elif kwargs:
            call = lambda: handler(request, **kwargs)  # noqa: E731
        elif len(positional) >= 2:
            # Backwards compatibility for ``handler(request, params)`` where
            # the second parameter has a different name.
            call = lambda: handler(request, params)  # noqa: E731
        else:
            call = lambda: handler(request)  # noqa: E731

        if asyncio.iscoroutinefunction(handler):
            return await call()
        return call()

    def _ensure_tailwind_compiled(self) -> None:
        """Conditionally build Tailwind CSS if env var is set and file is outdated"""
        if os.getenv("NEXTPY_AUTO_BUILD_TAILWIND", "false").lower() != "true":
            return
        tailwind_file = self.public_dir / "tailwind.css"
        styles = Path("styles.css")
        config = Path("tailwind.config.js")
        needs_build = False
        if not tailwind_file.exists():
            needs_build = True
        else:
            try:
                mtime = tailwind_file.stat().st_mtime
                if styles.exists() and styles.stat().st_mtime > mtime:
                    needs_build = True
                if config.exists() and config.stat().st_mtime > mtime:
                    needs_build = True
            except Exception:
                needs_build = True
        if needs_build:
            self._run_tailwind_build()

    def _run_tailwind_build(self) -> None:
        """Invoke npm to compile Tailwind CSS"""
        import subprocess, shutil
        npm = shutil.which("npm")
        if not npm:
            print("[NextPy] npm not available; cannot build Tailwind CSS")
            return
        print("[NextPy] running tailwind CSS build...")
        try:
            subprocess.run([npm, "ci"], check=False)
            subprocess.run([npm, "run", "build:tailwind"], check=False)
        except Exception as e:
            print(f"[NextPy] tailwind build failed: {e}")

    def _get_template_name(self, route, module: Optional[Any] = None) -> str:
        """Get the template name for a route"""
        if module and hasattr(module, "get_template"):
            return module.get_template()
            
        relative = route.file_path.relative_to(self.pages_dir)
        # Handle both .py and .psx files for template naming
        template_name = str(relative).replace(".py", ".html").replace(".psx", ".html")
        
        template_path = self.templates_dir / template_name
        if template_path.exists():
            return template_name
            
        if route.file_path.stem == "index":
            parent_template = self.templates_dir / route.file_path.parent.name / "index.html"
            if parent_template.exists():
                return str(parent_template.relative_to(self.templates_dir))
                
        return "_page.html"
        
    async def _render_404(self, request: Request) -> HTMLResponse:
        """Render the 404 page"""
        try:
            html = await self.template_renderer.render_async(
                "_404.html",
                context={"request": request},
            )
        except Exception:
            html = """
            <!DOCTYPE html>
            <html>
            <head><title>404 - Not Found</title></head>
            <body>
                <h1>404 - Page Not Found</h1>
                <p>The page you're looking for doesn't exist.</p>
            </body>
            </html>
            """
        return HTMLResponse(content=html, status_code=404)
        
    async def _render_error(self, request: Request, error: Exception) -> HTMLResponse:
        """Render enhanced error pages based on error type"""
        if self.debug:
            from nextpy.server.debug import render_debug_error_html

            return HTMLResponse(
                content=render_debug_error_html(error, request_path=request.url.path),
                status_code=500,
                headers={"Cache-Control": "no-store"},
            )
        try:
            # Handle specific error types
            if isinstance(error, JSXSyntaxError):
                return await self._render_jsx_error_page(request, error)
            elif isinstance(error, ImportError):
                return await self._render_import_error_page(request, error)
            elif isinstance(error, (ValueError, TypeError)):
                return await self._render_value_error_page(request, error)
            elif isinstance(error, (AttributeError, KeyError)):
                return await self._render_attribute_error_page(request, error)
            elif isinstance(error, (FileNotFoundError, OSError)):
                return await self._render_file_error_page(request, error)
            elif isinstance(error, (ConnectionError, TimeoutError)):
                return await self._render_network_error_page(request, error)
            else:
                return await self._render_generic_error_page(request, error)
                
        except Exception as fallback_error:
            # Ultimate fallback if error page rendering fails
            return HTMLResponse(
                content=self._get_emergency_error_html(error, fallback_error),
                status_code=500
            )
    
    async def _render_jsx_error_page(self, request: Request, error: JSXSyntaxError) -> HTMLResponse:
        """Render JSX syntax error page"""
        error_details = {
            "message": error.message,
            "file_path": error.file_path,
            "line_number": error.line_number,
            "column": error.column,
            "error_type": "JSX Syntax Error"
        }
        
        try:
            html = await self.template_renderer.render_async(
                "_jsx_error.html",
                context={
                    "request": request,
                    "error": error_details,
                    "debug": self.debug
                },
            )
        except Exception:
            html = self._get_jsx_error_html(error_details)
            
        return HTMLResponse(content=html, status_code=500)
    
    async def _render_import_error_page(self, request: Request, error: ImportError) -> HTMLResponse:
        """Render import error page"""
        error_details = {
            "message": str(error),
            "error_type": "Import Error",
            "suggestions": self._get_import_error_suggestions(error)
        }
        
        try:
            html = await self.template_renderer.render_async(
                "_import_error.html",
                context={
                    "request": request,
                    "error": error_details,
                    "debug": self.debug
                },
            )
        except Exception:
            html = self._get_import_error_html(error_details)
            
        return HTMLResponse(content=html, status_code=500)
    
    async def _render_value_error_page(self, request: Request, error: Exception) -> HTMLResponse:
        """Render value/type error page"""
        error_details = {
            "message": str(error),
            "error_type": type(error).__name__,
            "error_class": error.__class__.__name__
        }
        
        try:
            html = await self.template_renderer.render_async(
                "_value_error.html",
                context={
                    "request": request,
                    "error": error_details,
                    "debug": self.debug
                },
            )
        except Exception:
            html = self._get_value_error_html(error_details)
            
        return HTMLResponse(content=html, status_code=500)
    
    async def _render_attribute_error_page(self, request: Request, error: Exception) -> HTMLResponse:
        """Render attribute/key error page"""
        error_details = {
            "message": str(error),
            "error_type": type(error).__name__,
            "missing_attribute": self._extract_missing_attribute(error)
        }
        
        try:
            html = await self.template_renderer.render_async(
                "_attribute_error.html",
                context={
                    "request": request,
                    "error": error_details,
                    "debug": self.debug
                },
            )
        except Exception:
            html = self._get_attribute_error_html(error_details)
            
        return HTMLResponse(content=html, status_code=500)
    
    async def _render_file_error_page(self, request: Request, error: Exception) -> HTMLResponse:
        """Render file system error page"""
        error_details = {
            "message": str(error),
            "error_type": type(error).__name__,
            "file_path": self._extract_file_path_from_error(error)
        }
        
        try:
            html = await self.template_renderer.render_async(
                "_file_error.html",
                context={
                    "request": request,
                    "error": error_details,
                    "debug": self.debug
                },
            )
        except Exception:
            html = self._get_file_error_html(error_details)
            
        return HTMLResponse(content=html, status_code=500)
    
    async def _render_network_error_page(self, request: Request, error: Exception) -> HTMLResponse:
        """Render network/timeout error page"""
        error_details = {
            "message": str(error),
            "error_type": type(error).__name__,
            "retry_possible": True
        }
        
        try:
            html = await self.template_renderer.render_async(
                "_network_error.html",
                context={
                    "request": request,
                    "error": error_details,
                    "debug": self.debug
                },
            )
        except Exception:
            html = self._get_network_error_html(error_details)
            
        return HTMLResponse(content=html, status_code=503)
    
    async def _render_generic_error_page(self, request: Request, error: Exception) -> HTMLResponse:
        """Render generic error page"""
        error_details = {
            "message": str(error),
            "error_type": type(error).__name__,
            "error_class": error.__class__.__name__
        }
        
        if self.debug:
            import traceback
            error_details["traceback"] = traceback.format_exc()
        
        try:
            html = await self.template_renderer.render_async(
                "_error.html",
                context={
                    "request": request,
                    "error": error_details,
                    "debug": self.debug
                },
            )
        except Exception:
            html = self._get_generic_error_html(error_details)
            
        return HTMLResponse(content=html, status_code=500)
    
    def _get_jsx_error_html(self, error_details: dict) -> str:
        """Generate JSX error HTML fallback"""
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>JSX Syntax Error - NextPy</title>
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif; 
                        padding: 2rem; background: #fef2f2; }}
                .error-container {{ max-width: 800px; margin: 0 auto; }}
                .error-header {{ background: #dc2626; color: white; padding: 1rem; border-radius: 8px 8px 0 0; }}
                .error-content {{ background: white; padding: 2rem; border-radius: 0 0 8px 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
                .error-title {{ font-size: 1.5rem; font-weight: bold; margin-bottom: 1rem; }}
                .error-message {{ color: #dc2626; font-family: monospace; background: #fef2f2; padding: 1rem; border-radius: 4px; margin: 1rem 0; }}
                .error-details {{ background: #f3f4f6; padding: 1rem; border-radius: 4px; margin: 1rem 0; }}
                .error-suggestions {{ background: #ecfdf5; padding: 1rem; border-radius: 4px; margin: 1rem 0; }}
                .code {{ font-family: monospace; background: #1f2937; color: #f3f4f6; padding: 0.5rem; border-radius: 4px; }}
            </style>
        </head>
        <body>
            <div class="error-container">
                <div class="error-header">
                    <h1>🚫 JSX Syntax Error</h1>
                </div>
                <div class="error-content">
                    <div class="error-title">JSX Syntax Error Detected</div>
                    <div class="error-message">{error_details.get('message', 'Unknown JSX syntax error')}</div>
                    
                    {f'<div class="error-details"><strong>File:</strong> {error_details.get("file_path", "Unknown")}</div>' if error_details.get('file_path') else ''}
                    {f'<div class="error-details"><strong>Line:</strong> {error_details.get("line_number", "Unknown")}</div>' if error_details.get('line_number') else ''}
                    {f'<div class="error-details"><strong>Column:</strong> {error_details.get("column", "Unknown")}</div>' if error_details.get('column') else ''}
                    
                    <div class="error-suggestions">
                        <strong>Common JSX Issues:</strong>
                        <ul>
                            <li>Check for unclosed tags: <code>&lt;div&gt;content&lt;/div&gt;</code></li>
                            <li>Ensure proper attribute syntax: <code>className="my-class"</code></li>
                            <li>Verify component names are capitalized: <code>MyComponent</code></li>
                            <li>Check for missing quotes in attributes</li>
                            <li>Ensure proper nesting of elements</li>
                        </ul>
                    </div>
                    
                    {f'<div class="error-suggestions"><strong>Debug Mode:</strong> {"Enabled" if self.debug else "Disabled"}</div>'}
                </div>
            </div>
        </body>
        </html>
        """
    
    def _get_import_error_html(self, error_details: dict) -> str:
        """Generate import error HTML fallback"""
        suggestions = error_details.get('suggestions', [])
        suggestions_html = "\n".join([f"<li>{suggestion}</li>" for suggestion in suggestions])
        
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Import Error - NextPy</title>
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif; 
                        padding: 2rem; background: #fefce8; }}
                .error-container {{ max-width: 800px; margin: 0 auto; }}
                .error-header {{ background: #ca8a04; color: white; padding: 1rem; border-radius: 8px 8px 0 0; }}
                .error-content {{ background: white; padding: 2rem; border-radius: 0 0 8px 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
                .error-message {{ color: #ca8a04; font-family: monospace; background: #fefce8; padding: 1rem; border-radius: 4px; margin: 1rem 0; }}
                .error-suggestions {{ background: #ecfdf5; padding: 1rem; border-radius: 4px; margin: 1rem 0; }}
            </style>
        </head>
        <body>
            <div class="error-container">
                <div class="error-header">
                    <h1>📦 Import Error</h1>
                </div>
                <div class="error-content">
                    <div class="error-title">Module Import Failed</div>
                    <div class="error-message">{error_details.get('message', 'Unknown import error')}</div>
                    
                    <div class="error-suggestions">
                        <strong>Possible Solutions:</strong>
                        <ul>{suggestions_html}</ul>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
    
    def _get_value_error_html(self, error_details: dict) -> str:
        """Generate value error HTML fallback"""
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>{error_details.get('error_type', 'Error')} - NextPy</title>
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif; 
                        padding: 2rem; background: #fef2f2; }}
                .error-container {{ max-width: 800px; margin: 0 auto; }}
                .error-header {{ background: #dc2626; color: white; padding: 1rem; border-radius: 8px 8px 0 0; }}
                .error-content {{ background: white; padding: 2rem; border-radius: 0 0 8px 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
                .error-message {{ color: #dc2626; font-family: monospace; background: #fef2f2; padding: 1rem; border-radius: 4px; margin: 1rem 0; }}
            </style>
        </head>
        <body>
            <div class="error-container">
                <div class="error-header">
                    <h1>⚠️ {error_details.get('error_type', 'Error')}</h1>
                </div>
                <div class="error-content">
                    <div class="error-title">{error_details.get('error_class', 'Runtime Error')}</div>
                    <div class="error-message">{error_details.get('message', 'Unknown error occurred')}</div>
                    {f'<pre>{error_details.get("traceback", "")}</pre>' if self.debug and error_details.get('traceback') else ''}
                </div>
            </div>
        </body>
        </html>
        """
    
    def _get_attribute_error_html(self, error_details: dict) -> str:
        """Generate attribute error HTML fallback"""
        missing_attr = error_details.get('missing_attribute', '')
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Attribute Error - NextPy</title>
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif; 
                        padding: 2rem; background: #fef2f2; }}
                .error-container {{ max-width: 800px; margin: 0 auto; }}
                .error-header {{ background: #dc2626; color: white; padding: 1rem; border-radius: 8px 8px 0 0; }}
                .error-content {{ background: white; padding: 2rem; border-radius: 0 0 8px 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
                .error-message {{ color: #dc2626; font-family: monospace; background: #fef2f2; padding: 1rem; border-radius: 4px; margin: 1rem 0; }}
            </style>
        </head>
        <body>
            <div class="error-container">
                <div class="error-header">
                    <h1>🔍 Attribute Error</h1>
                </div>
                <div class="error-content">
                    <div class="error-title">Missing Attribute or Key</div>
                    <div class="error-message">{error_details.get('message', 'Unknown attribute error')}</div>
                    {f'<div class="error-suggestions"><strong>Missing:</strong> <code>{missing_attr}</code></div>' if missing_attr else ''}
                </div>
            </div>
        </body>
        </html>
        """
    
    def _get_file_error_html(self, error_details: dict) -> str:
        """Generate file error HTML fallback"""
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>File Error - NextPy</title>
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif; 
                        padding: 2rem; background: #fef2f2; }}
                .error-container {{ max-width: 800px; margin: 0 auto; }}
                .error-header {{ background: #dc2626; color: white; padding: 1rem; border-radius: 8px 8px 0 0; }}
                .error-content {{ background: white; padding: 2rem; border-radius: 0 0 8px 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
                .error-message {{ color: #dc2626; font-family: monospace; background: #fef2f2; padding: 1rem; border-radius: 4px; margin: 1rem 0; }}
            </style>
        </head>
        <body>
            <div class="error-container">
                <div class="error-header">
                    <h1>📁 File System Error</h1>
                </div>
                <div class="error-content">
                    <div class="error-title">File Access Error</div>
                    <div class="error-message">{error_details.get('message', 'Unknown file error')}</div>
                    {f'<div class="error-details"><strong>File Path:</strong> <code>{error_details.get("file_path", "Unknown")}</code></div>' if error_details.get('file_path') else ''}
                </div>
            </div>
        </body>
        </html>
        """
    
    def _get_network_error_html(self, error_details: dict) -> str:
        """Generate network error HTML fallback"""
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Network Error - NextPy</title>
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif; 
                        padding: 2rem; background: #fef2f2; }}
                .error-container {{ max-width: 800px; margin: 0 auto; }}
                .error-header {{ background: #f59e0b; color: white; padding: 1rem; border-radius: 8px 8px 0 0; }}
                .error-content {{ background: white; padding: 2rem; border-radius: 0 0 8px 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
                .error-message {{ color: #f59e0b; font-family: monospace; background: #fef2f2; padding: 1rem; border-radius: 4px; margin: 1rem 0; }}
                .retry-button {{ background: #f59e0b; color: white; padding: 0.5rem 1rem; border: none; border-radius: 4px; cursor: pointer; }}
            </style>
        </head>
        <body>
            <div class="error-container">
                <div class="error-header">
                    <h1>🌐 Network Error</h1>
                </div>
                <div class="error-content">
                    <div class="error-title">Connection or Timeout Error</div>
                    <div class="error-message">{error_details.get('message', 'Network error occurred')}</div>
                    <button class="retry-button" onclick="window.location.reload()">Retry</button>
                </div>
            </div>
        </body>
        </html>
        """
    
    def _get_generic_error_html(self, error_details: dict) -> str:
        """Generate generic error HTML fallback"""
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Server Error - NextPy</title>
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif; 
                        padding: 2rem; background: #fef2f2; }}
                .error-container {{ max-width: 800px; margin: 0 auto; }}
                .error-header {{ background: #dc2626; color: white; padding: 1rem; border-radius: 8px 8px 0 0; }}
                .error-content {{ background: white; padding: 2rem; border-radius: 0 0 8px 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
                .error-message {{ color: #dc2626; font-family: monospace; background: #fef2f2; padding: 1rem; border-radius: 4px; margin: 1rem 0; }}
            </style>
        </head>
        <body>
            <div class="error-container">
                <div class="error-header">
                    <h1>💥 Server Error</h1>
                </div>
                <div class="error-content">
                    <div class="error-title">{error_details.get('error_type', 'Server Error')}</div>
                    <div class="error-message">{error_details.get('message', 'An unexpected error occurred')}</div>
                    {f'<pre>{error_details.get("traceback", "")}</pre>' if self.debug and error_details.get('traceback') else ''}
                </div>
            </div>
        </body>
        </html>
        """
    
    def _get_emergency_error_html(self, original_error: Exception, fallback_error: Exception) -> str:
        """Ultimate fallback error page"""
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Critical Error - NextPy</title>
            <style>
                body {{ font-family: monospace; background: #000; color: #ff0000; padding: 2rem; }}
            </style>
        </head>
        <body>
            <h1>🚨 CRITICAL SYSTEM ERROR</h1>
            <p>Original Error: {str(original_error)}</p>
            <p>Fallback Error: {str(fallback_error)}</p>
            <p>Please check the server logs for more information.</p>
        </body>
        </html>
        """
    
    def _get_import_error_suggestions(self, error: ImportError) -> list:
        """Get suggestions for import errors"""
        error_str = str(error).lower()
        suggestions = []
        
        if "no module named" in error_str:
            suggestions.append("Install the missing module using pip")
            suggestions.append("Check if the module name is spelled correctly")
        elif "cannot import" in error_str:
            suggestions.append("Verify the function/class exists in the module")
            suggestions.append("Check for circular imports")
        elif "module not found" in error_str:
            suggestions.append("Ensure the module is in the correct directory")
            suggestions.append("Check PYTHONPATH includes the module directory")
        else:
            suggestions.append("Check if all dependencies are installed")
            suggestions.append("Verify the import statement syntax")
            suggestions.append("Ensure the file exists and is accessible")
        
        return suggestions
    
    def _extract_missing_attribute(self, error: Exception) -> str:
        """Extract missing attribute name from error message"""
        error_str = str(error)
        if "has no attribute '" in error_str:
            start = error_str.find("has no attribute '") + 19
            end = error_str.find("'", start)
            if start > 18 and end > start:
                return error_str[start:end]
        elif "Key '" in error_str:
            start = error_str.find("Key '") + 5
            end = error_str.find("'", start)
            if start > 4 and end > start:
                return error_str[start:end]
        return ""
    
    def _extract_file_path_from_error(self, error: Exception) -> str:
        """Extract file path from error message"""
        error_str = str(error)
        # Try to extract file path from common error patterns
        import re
        
        # Pattern for file paths in error messages
        patterns = [
            r"[\'/]([^\'/]+\.py[\']?)",
            r"file: ([^\s]+)",
            r'File "([^"]+)"',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, error_str)
            if match:
                return match.group(1)
        
        return ""
        
    async def _handle_demo_page(self, request: Request, route, params: Dict[str, str]) -> Response:
        """Handle demo page requests"""
        try:
            # Call the demo page function
            demo_function = route.handler
            if callable(demo_function):
                # Demo pages return JSX elements, render them
                from ..jsx import render_jsx
                jsx_element = demo_function()
                html = render_jsx(jsx_element)
                
                return HTMLResponse(
                    content=html,
                    headers={
                        "Cache-Control": "no-cache, no-store, must-revalidate",
                        "Pragma": "no-cache",
                        "Expires": "0",
                    },
                )
            else:
                return await self._render_404(request)
                
        except Exception as e:
            if self.debug:
                import traceback
                traceback.print_exc()
            return await self._render_error(request, e)
        
    def reload_routes(self) -> None:
        """Reload all routes (for hot reload)"""
        self._modules_cache.clear()
        if hasattr(self.router, "invalidate_cache"):
            self.router.invalidate_cache()
        if demo_router.should_serve_demo():
            self.router = Router(str(self.pages_dir), str(self.templates_dir))
            self.router.enable_demo_mode()
        else:
            self.router = ComponentRouter(str(self.pages_dir), str(self.templates_dir))
        
        self.router.scan_pages()


def create_app(
    pages_dir: str = "pages",
    templates_dir: str = "templates",
    public_dir: str = "public",
    out_dir: str = "out",
    debug: bool = False,
    admin_site: Any = None,
) -> FastAPI:
    """
    Factory function to create a NextPy application
    
    Args:
        pages_dir: Directory containing page files
        templates_dir: Directory containing Jinja2 templates
        public_dir: Directory containing static files
        out_dir: Directory for SSG output
        debug: Enable debug mode
        
    Returns:
        FastAPI application instance
    """
    global _api_app
    nextpy_app = NextPyApp(
        pages_dir=pages_dir,
        templates_dir=templates_dir,
        public_dir=public_dir,
        out_dir=out_dir,
        debug=debug,
        admin_site=admin_site,
    )
    _api_app = nextpy_app.app
    return nextpy_app.app
