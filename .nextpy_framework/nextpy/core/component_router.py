"""
NextPy Component Router - Enhanced router for component-based pages
Supports both template-based and component-based rendering
"""

import os
import re
import json
import time
import hashlib
import importlib.util
import threading
from collections import OrderedDict
from pathlib import Path
from typing import AsyncIterator, Dict, List, Optional, Callable, Any, Tuple
from dataclasses import dataclass, field
from pydantic import BaseModel

_DEBUG = os.environ.get("NEXTPY_DEBUG") == "1"

from .router import Route, DynamicRoute, RouteParams
from .component_renderer import ComponentRenderer


@dataclass
class ComponentRoute(Route):
    """A route that renders components instead of templates"""
    use_components: bool = True
    renderer: ComponentRenderer = field(default_factory=ComponentRenderer)
    special_chains: Dict[str, List[Path]] = field(default_factory=dict)


class ComponentRouter:
    """
    Enhanced router that supports both template-based and component-based pages
    Automatically detects which rendering system to use based on file content
    Supports Next.js-style special files: layout, page, loading, error, not-found, etc.
    """
    
    # Special file names (Next.js-style)
    SPECIAL_FILES = {
        'layout', 'page', 'loading', 'error', 'not-found', 
        'template', 'middleware', 'head', 'route'
    }
    
    def __init__(self, pages_dir: str = "pages", templates_dir: str = "templates"):
        self.pages_dir = Path(pages_dir)
        self.templates_dir = Path(templates_dir)
        self.routes: List[Route] = []
        self.api_routes: List[Route] = []
        self._route_cache: Dict[str, Route] = {}
        self.renderer = ComponentRenderer()

        # Caches (per-process). Page HTML caching is what makes repeat SPA
        # navigations to dynamic routes fast: the expensive component/layout
        # render only runs on a miss.
        self._layout_cache: Dict[str, Tuple[float, Optional[Callable]]] = {}
        self._metadata_cache: Dict[str, Tuple[float, Dict[str, Any]]] = {}
        self._page_cache: "OrderedDict[str, Dict[str, Any]]" = OrderedDict()
        self._layout_sig_cache: Dict[str, Tuple[str, str]] = {}
        self._cache_ttl = float(os.environ.get("NEXTPY_PAGE_CACHE_TTL", "30"))
        self._cache_max = int(os.environ.get("NEXTPY_PAGE_CACHE_SIZE", "128"))

    # ------------------------------------------------------------------
    # Cache management
    # ------------------------------------------------------------------
    def invalidate_cache(self) -> None:
        """Drop all render/layout caches (used by hot reload / tests)."""
        self._layout_cache.clear()
        self._metadata_cache.clear()
        self._page_cache.clear()
        self._layout_sig_cache.clear()

    def is_cacheable(self, route: Route, context: Optional[Dict[str, Any]] = None) -> bool:
        """Return ``True`` when a rendered page may be safely reused.

        Personalised responses (cookies / Authorization) and pages using
        ``getServerSideProps`` are never cached.
        """
        context = context or {}
        request = context.get("request")
        if request is not None:
            if getattr(request, "cookies", None):
                return False
            headers = getattr(request, "headers", {}) or {}
            if headers.get("authorization") or headers.get("cookie"):
                return False

        try:
            module = route.renderer.load_component_module(route.file_path)
        except Exception:
            return False

        if module is not None and (
            hasattr(module, "getServerSideProps")
            or hasattr(module, "get_server_side_props")
        ):
            return False
        return True

    def _route_cache_key(self, route: Route, context: Dict[str, Any]) -> str:
        params = context.get("params") or {}
        query = context.get("query") or {}
        return "|".join(
            (
                str(route.file_path),
                json.dumps(params, sort_keys=True, default=str),
                json.dumps(query, sort_keys=True, default=str),
            )
        )

    def _page_dependencies(self, route: Route) -> List[Tuple[str, float]]:
        paths = [route.file_path]
        paths.extend(getattr(route, "layout_chain", []) or [])
        deps: List[Tuple[str, float]] = []
        for path in paths:
            try:
                deps.append((str(path), Path(path).stat().st_mtime))
            except OSError:
                continue
        return deps

    def _cache_lookup(self, key: str, route: Route) -> Tuple[Optional[str], bool]:
        """Return ``(html, stale)`` without deleting stale ISR entries."""
        entry = self._page_cache.get(key)
        if not entry:
            return None, False

        # Invalidate when the page or any layout changed on disk.
        for path, mtime in entry["deps"]:
            try:
                if Path(path).stat().st_mtime != mtime:
                    self._page_cache.pop(key, None)
                    return None, False
            except OSError:
                self._page_cache.pop(key, None)
                return None, False

        age = time.time() - entry["timestamp"]
        revalidate = entry.get("revalidate")
        ttl = self._cache_ttl if revalidate is None else float(revalidate)
        stale = age > ttl
        self._page_cache.move_to_end(key)
        return entry["html"], stale

    def _cache_get(self, key: str, route: Route) -> Optional[str]:
        html, stale = self._cache_lookup(key, route)
        return None if stale else html

    def _cache_set(
        self,
        key: str,
        route: Route,
        html: str,
        revalidate: Optional[int] = None,
    ) -> None:
        self._page_cache[key] = {
            "html": html,
            "timestamp": time.time(),
            "deps": self._page_dependencies(route),
            "revalidate": revalidate,
            "refreshing": False,
        }
        self._page_cache.move_to_end(key)
        while len(self._page_cache) > self._cache_max:
            self._page_cache.popitem(last=False)

    def get_revalidate(self, route: Route) -> Optional[int]:
        """Return the page's ISR interval (``None`` means use global TTL)."""
        renderer = getattr(route, "renderer", None)
        if renderer is not None and hasattr(renderer, "get_revalidate"):
            try:
                value = renderer.get_revalidate(route.file_path)
                if value is not None:
                    return int(value)
            except Exception:
                pass
        try:
            module = route.renderer.load_component_module(route.file_path)
            value = getattr(module, "revalidate", None)
            return int(value) if value is not None else None
        except Exception:
            return None

    def _schedule_refresh(
        self,
        key: str,
        route: Route,
        context: Dict[str, Any],
        include_layout: bool,
        revalidate: Optional[int],
    ) -> None:
        """Refresh a stale ISR entry in the background (stale-while-revalidate)."""
        entry = self._page_cache.get(key)
        if entry is None or entry.get("refreshing"):
            return
        entry["refreshing"] = True
        safe_context = {
            name: value for name, value in context.items()
            if name not in ("request", "response", "req")
        }

        def _refresh() -> None:
            try:
                html = self._render_component_route(route, safe_context, include_layout)
                if not self._is_error_html(html):
                    self._cache_set(key, route, html, revalidate)
            finally:
                current = self._page_cache.get(key)
                if current is not None:
                    current["refreshing"] = False

        threading.Thread(
            target=_refresh,
            name=f"nextpy-isr-{hashlib.md5(key.encode()).hexdigest()[:8]}",
            daemon=True,
        ).start()

    def get_layout_signature(self, route: Route) -> str:
        """Stable signature of a route's layout chain (path + mtime)."""
        cache_key = str(route.file_path)
        chain = [str(p) for p in (getattr(route, "layout_chain", []) or [])]

        parts: List[str] = []
        for path in chain:
            try:
                parts.append(f"{path}:{Path(path).stat().st_mtime}")
            except OSError:
                parts.append(path)
        stamp = "|".join(parts)

        cached = self._layout_sig_cache.get(cache_key)
        if cached and cached[0] == stamp:
            return cached[1]

        signature = hashlib.md5(stamp.encode("utf-8")).hexdigest()[:16]
        self._layout_sig_cache[cache_key] = (stamp, signature)
        return signature
        
    def scan_pages(self) -> None:
        """Scan pages directory and register all routes"""
        if not self.pages_dir.exists():
            return
            
        # Scan for .py, .py.jsx and .psx files
        extensions = ["*.py", "*.py.jsx", "*.psx"]
        for ext in extensions:
            for file_path in self.pages_dir.rglob(ext):
                relative_parts = file_path.relative_to(self.pages_dir).parts
                if any(part.startswith("_") or part == "actions" for part in relative_parts):
                    continue
                
                # Skip special files - they're handled separately
                stem = file_path.stem
                if stem in self.SPECIAL_FILES:
                    continue
                    
                route = self._create_route_from_file(file_path)
                if route:
                    if route.is_api:
                        self.api_routes.append(route)
                    else:
                        self.routes.append(route)
                    
        self._sort_routes()
        
    def _create_route_from_file(self, file_path: Path) -> Optional[Route]:
        """Create a Route object from a Python file"""
        relative_path = file_path.relative_to(self.pages_dir)
        parts = list(relative_path.parts)
        
        is_api = parts[0] == "api" if parts else False
        
        route_parts = []
        param_names = []
        is_dynamic = False
        is_catch_all = False
        
        for part in parts:
            if part.endswith(".py.jsx"):
                part = part[:-7]
            elif part.endswith(".psx"):
                part = part[:-4]
            elif part.endswith(".py"):
                part = part[:-3]

            if part == "index":
                continue
                
            catch_all_match = re.match(r"\[\.\.\.(\w+)\]", part)
            dynamic_match = re.match(r"\[(\w+)\]", part)
            
            if catch_all_match:
                param_name = catch_all_match.group(1)
                param_names.append(param_name)
                route_parts.append(f"(?P<{param_name}>.+)")
                is_dynamic = True
                is_catch_all = True
            elif dynamic_match:
                param_name = dynamic_match.group(1)
                param_names.append(param_name)
                route_parts.append(f"(?P<{param_name}>[^/]+)")
                is_dynamic = True
            else:
                route_parts.append(part)
                
        if is_api and route_parts and route_parts[0] == "api":
            route_parts = route_parts[1:]
            
        path = "/" + "/".join(route_parts) if route_parts else "/"
        
        if is_api:
            path = "/api" + path if path != "/" else "/api"
            
        pattern = None
        if is_dynamic:
            pattern_str = "^" + path.replace("/", r"\/") + "$"
            pattern_str = re.sub(r"\\\(\?P", "(?P", pattern_str)
            pattern_str = pattern_str.replace(r"\[", "[").replace(r"\]", "]")
            pattern_str = pattern_str.replace(r"\+", "+")
            try:
                pattern = re.compile(pattern_str)
            except re.error:
                pattern = re.compile("^" + path + "$")
                
        # Check if this is a component-based page
        use_components = self._is_component_page(file_path)
        
        route_path = path
        
        handler = self._load_handler(file_path, use_components)
        
        # Build special file chains for this route
        special_chains = self._build_special_files_chain(file_path)
        layout_chain = special_chains['layout']
        
        route_class = ComponentRoute if use_components else (DynamicRoute if is_dynamic else Route)
        
        route = route_class(
            path=route_path,
            file_path=file_path,
            handler=handler,
            is_api=is_api,
            is_dynamic=is_dynamic,
            param_names=param_names,
            pattern=pattern,
            layout_chain=layout_chain
        )
        
        # Add component-specific attributes
        if use_components:
            route.use_components = True
            route.renderer = self.renderer
            route.special_chains = special_chains
        
        return route
        
    def _is_component_page(self, file_path: Path) -> bool:
        """Check if a page uses components or templates with enhanced JSX detection"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Enhanced JSX patterns for more robust detection
            jsx_patterns = [
                'return (',
                'default = ',
                'className=',
                '<div',
                '<h1',
                '<h2',
                '<h3',
                '<p',
                '<button',
                '<section',
                '<article',
                '<header',
                '<footer',
                '<nav',
                '<main',
                '<aside',
                '<span',
                '<img',
                '<a',
                '<ul',
                '<ol',
                '<li',
                '<form',
                '<input',
                '<label',
                '<select',
                '<textarea',
                'export function',
                'def.*return.*<',
                'jsx(',
                'render_jsx(',
                'from nextpy.true_jsx',
                'from .jsx import',
                'getServerSideProps',
                'getStaticProps',
                'props.get(',
                'props = props or',
                'function.*Component',
                r'const.*=.*\(.*\)',
                'className=',
                'htmlFor=',
                'onClick=',
                'onChange=',
                'onSubmit=',
                'href=',
                'src=',
                'alt=',
                'placeholder=',
                'type=',
                'value=',
                'disabled=',
                'readOnly=',
                'required=',
                'checked=',
                'selected=',
                'multiple=',
                'accept=',
                'maxLength=',
                'minLength=',
                'pattern=',
                'min=',
                'max=',
                'step=',
                'autoComplete=',
                'autoFocus=',
                'tabIndex=',
                'accessKey=',
                'draggable=',
                'hidden=',
                'spellCheck=',
                'contentEditable=',
                'dir=',
                'lang=',
                'title=',
                'style=',
                'id=',
                'name=',
                'data-',
                'aria-',
                'role=',
            ]
            
            # Check for template indicators (to differentiate from JSX)
            template_indicators = [
                'def get_template(',
                'getServerSideProps',
                'getStaticProps',
                'return "',
                'templates/',
                '.html',
                '{% extends',
                '{% block',
                '{% include',
                '{% for',
                '{% if',
                '{{ ',
                '}}',
                '|filter',
                '{% end',
                'jinja2',
                'render_template(',
            ]
            
            # Enhanced scoring system with weighted patterns
            component_score = 0
            template_score = 0
            
            # Weight JSX patterns more heavily
            for pattern in jsx_patterns:
                if '*' in pattern:
                    # Regex pattern
                    if re.search(pattern, content):
                        component_score += 2
                else:
                    # Simple string pattern
                    count = content.count(pattern)
                    if count > 0:
                        component_score += count * 2
            
            # Additional JSX-specific checks
            if file_path.suffix == '.py.jsx':
                component_score += 10  # Strong indicator
            
            # Check for JSX return patterns
            jsx_return_patterns = [
                r'return\s*\(\s*<',
                r'return\s+<',
                r'default\s*=\s*\w+',
                r'function\s+\w+\s*\(.*\)\s*{',
                r'const\s+\w+\s*=\s*\(.*\)\s*=>',
            ]
            
            for pattern in jsx_return_patterns:
                if re.search(pattern, content, re.MULTILINE):
                    component_score += 3
            
            # Check for component imports
            component_import_patterns = [
                r'from\s+.*components',
                r'import\s+.*from\s+.*components',
                r'import\s+{.*}',
                r'from\s+nextpy\.',
                r'from\s+\.jsx',
            ]
            
            for pattern in component_import_patterns:
                if re.search(pattern, content):
                    component_score += 2
            
            # Weight template patterns
            for pattern in template_indicators:
                if pattern in content:
                    template_score += 3
            
            # Special checks for template files
            if file_path.suffix == '.py' and not file_path.name.endswith('.jsx'):
                # Check if it looks like a traditional template page
                if 'def get_template(' in content and 'return "' in content:
                    template_score += 5
            
            # Debug information (can be removed in production)
            # print(f"File: {file_path.name}, Component Score: {component_score}, Template Score: {template_score}")
            
            return component_score > template_score
            
        except Exception as e:
            # If there's an error reading the file, default to False
            print(f"Error checking if {file_path} is component page: {e}")
            return False
        
    def _load_handler(self, file_path: Path, use_components: bool = False) -> Optional[Callable]:
        """Load the appropriate handler based on rendering type"""
        if use_components:
            return self._create_component_handler(file_path)
        else:
            return self._create_template_handler(file_path)
    
    def _create_component_handler(self, file_path: Path) -> Callable:
        """Create a handler for component-based pages"""
        def handler(context: Dict[str, Any] = None):
            if context is None:
                context = {}
            return self.renderer.render_page(file_path, context)
        return handler
    
    def _create_template_handler(self, file_path: Path) -> Optional[Callable]:
        """Load the traditional template-based handler using JSX transformer"""
        try:
            # Use JSX transformer for consistent loading
            from ..jsx_transformer import JSXTransformer
            transformer = JSXTransformer()
            module = transformer.load_jsx_module(file_path, file_path.stem)
            
            if module:
                for func_name in ["handler", "page", "get", "post", "default"]:
                    if hasattr(module, func_name):
                        return getattr(module, func_name)
        except Exception:
            # Fallback to regular import if JSX transformer fails
            try:
                spec = importlib.util.spec_from_file_location(
                    file_path.stem, 
                    file_path
                )
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    for func_name in ["handler", "page", "get", "post", "default"]:
                        if hasattr(module, func_name):
                            return getattr(module, func_name)
            except Exception:
                pass  # Silently fail if both methods fail
                
        return None
    
    def _find_special_file(self, directory: Path, file_name: str) -> Optional[Path]:
        """Find a special file (layout, loading, error, etc.) in a directory with .psx priority"""
        # Check .psx first (higher priority), then .py
        psx_file = directory / f"{file_name}.psx"
        py_file = directory / f"{file_name}.py"
        
        if psx_file.exists():
            return psx_file
        elif py_file.exists():
            return py_file
        return None
    
    def _build_special_files_chain(self, page_file_path: Path) -> Dict[str, List[Path]]:
        """Build chains for all special files (layout, loading, error, etc.) for a route"""
        special_chains = {
            'layout': [],
            'loading': [],
            'error': [],
            'not-found': [],
            'template': []
        }
        
        # Start from the page's directory and work up to the root
        current_dir = page_file_path.parent
        
        while current_dir != self.pages_dir.parent:
            # Check for each special file type
            for file_type in special_chains.keys():
                special_file = self._find_special_file(current_dir, file_type)
                if special_file:
                    special_chains[file_type].append(special_file)
            
            # Move up one directory
            current_dir = current_dir.parent
        
        # Reverse all chains to get inside-out order (root last)
        for file_type in special_chains:
            special_chains[file_type].reverse()
        
        return special_chains
    
    def _build_layout_chain(self, page_file_path: Path) -> List[Path]:
        """Build the layout chain for a given page file (inside-out order)"""
        special_chains = self._build_special_files_chain(page_file_path)
        return special_chains['layout']
    
    def _load_layout(self, layout_path: Path) -> Optional[Callable]:
        """Load a layout function, caching it by file modification time."""
        try:
            mtime = layout_path.stat().st_mtime
        except OSError:
            return None

        cache_key = str(layout_path)
        cached = self._layout_cache.get(cache_key)
        if cached is not None and cached[0] == mtime:
            return cached[1]

        layout_func: Optional[Callable] = None
        try:
            # For .psx files, use JSX transformer to compile first
            if layout_path.suffix == '.psx':
                try:
                    from ..jsx_transformer import JSXTransformer
                    transformer = JSXTransformer()
                    module = transformer.load_jsx_module(layout_path, layout_path.stem)

                    if module:
                        if hasattr(module, "Layout"):
                            layout_func = getattr(module, "Layout")
                        elif hasattr(module, "layout"):
                            layout_func = getattr(module, "layout")
                except Exception as e:
                    print(f"Warning: Failed to load .psx layout with JSX transformer: {e}")

            if layout_func is None:
                # For .py files, import normally
                spec = importlib.util.spec_from_file_location(
                    layout_path.stem,
                    layout_path
                )
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)

                    # Look for Layout function
                    if hasattr(module, "Layout"):
                        layout_func = getattr(module, "Layout")
                    elif hasattr(module, "layout"):
                        layout_func = getattr(module, "layout")

        except Exception as e:
            print(f"Warning: Failed to load layout from {layout_path}: {e}")

        self._layout_cache[cache_key] = (mtime, layout_func)
        return layout_func
    
    def _extract_layout_metadata(self, layout_path: Path) -> Dict[str, Any]:
        """Extract metadata from a layout file (title, description, theme, etc.)"""
        try:
            mtime = layout_path.stat().st_mtime
        except OSError:
            return {}

        cache_key = str(layout_path)
        cached = self._metadata_cache.get(cache_key)
        if cached is not None and cached[0] == mtime:
            return dict(cached[1])

        metadata: Dict[str, Any] = {}
        try:
            # For .py files, check for metadata variables
            if layout_path.suffix == '.py':
                spec = importlib.util.spec_from_file_location(
                    layout_path.stem,
                    layout_path
                )
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)

                    # Check for common metadata variables
                    if hasattr(module, 'metadata'):
                        metadata.update(module.metadata)
                    if hasattr(module, 'title'):
                        metadata['title'] = module.title
                    if hasattr(module, 'description'):
                        metadata['description'] = module.description
                    if hasattr(module, 'theme'):
                        metadata['theme'] = module.theme
        except Exception as e:
            print(f"Warning: Failed to extract metadata from {layout_path}: {e}")

        self._metadata_cache[cache_key] = (mtime, dict(metadata))
        return metadata
    
    def _merge_route_metadata(self, special_chains: Dict[str, List[Path]]) -> Dict[str, Any]:
        """Merge metadata from all layout chains (parent layouts override child layouts)"""
        merged_metadata = {}
        
        # Merge metadata from layout chain (root to leaf, so leaf overrides root)
        layout_chain = special_chains.get('layout', [])
        for layout_path in layout_chain:
            metadata = self._extract_layout_metadata(layout_path)
            merged_metadata.update(metadata)
        
        return merged_metadata
        
    def _sort_routes(self) -> None:
        """Sort routes so static routes come before dynamic ones"""
        def route_priority(route: Route) -> Tuple[int, int, str]:
            if route.is_catch_all:
                return (2, len(route.param_names), route.path)
            elif route.is_dynamic:
                return (1, len(route.param_names), route.path)
            else:
                return (0, 0, route.path)
                
        self.routes.sort(key=route_priority)
        self.api_routes.sort(key=route_priority)
        
    def match(self, url_path: str) -> Optional[Tuple[Route, Dict[str, str]]]:
        """Find a route that matches the given URL path"""
        url_path = url_path.rstrip("/") or "/"
        
        if url_path in self._route_cache:
            route = self._route_cache[url_path]
            params = route.matches(url_path) or {}
            return (route, params)
            
        routes = self.api_routes if url_path.startswith("/api") else self.routes
        
        for route in routes:
            params = route.matches(url_path)
            if params is not None:
                if not route.is_dynamic:
                    self._route_cache[url_path] = route
                return (route, params)
                
        return None
        
    def render_route(
        self,
        route: Route,
        context: Dict[str, Any] = None,
        include_layout: bool = True,
    ) -> str:
        """Render a route using the appropriate renderer with support for loading/error states.

        Args:
            route: The matched route.
            context: Rendering context (params, query, request, ...).
            include_layout: When ``False`` only the page component is rendered
                (used for SPA fragment responses where the client keeps the
                existing layout).
        """
        if context is None:
            context = {}

        if isinstance(route, ComponentRoute) and route.use_components:
            cacheable = self.is_cacheable(route, context)
            cache_key = None
            revalidate = self.get_revalidate(route)
            if cacheable:
                mode = "full" if include_layout else "frag"
                cache_key = self._route_cache_key(route, context) + "|" + mode
                cached, stale = self._cache_lookup(cache_key, route)
                if cached is not None:
                    if stale:
                        self._schedule_refresh(
                            cache_key, route, context, include_layout, revalidate
                        )
                    return cached

            html = self._render_component_route(route, context, include_layout)

            # Never cache error pages; they should be retried next time.
            if cache_key is not None and not self._is_error_html(html):
                resolved_revalidate = self.get_revalidate(route)
                if resolved_revalidate is not None:
                    revalidate = resolved_revalidate
                self._cache_set(cache_key, route, html, revalidate)
            return html

        elif route.handler and callable(route.handler):
            return route.handler(context)
        else:
            return f"<h1>Route {route.path} has no handler</h1>"

    async def render_route_stream(
        self,
        route: Route,
        context: Dict[str, Any] = None,
        include_layout: bool = True,
    ) -> AsyncIterator[str]:
        """Render a route as a stream of HTML chunks.

        A page can define ``streaming = True`` for chunked output, or provide
        its own ``stream(context)`` generator for true data streaming.
        """
        from .streaming import stream_route

        context = context or {}
        module = None
        if isinstance(route, ComponentRoute):
            try:
                module = route.renderer.load_component_module(route.file_path)
            except Exception:
                module = None
        if module is not None and hasattr(module, "stream"):
            async for chunk in stream_route(module, context, ""):
                yield chunk
            return

        html = self.render_route(route, context, include_layout)
        async for chunk in stream_route(module, context, html):
            yield chunk

    @staticmethod
    def _is_full_document(element: Any) -> bool:
        """Return True when a rendered layout is a complete HTML document."""
        ast = getattr(element, "_ast_node", None)
        tag = getattr(ast, "tag", None)
        if tag == "html":
            return True
        html = getattr(element, "html", None)
        if isinstance(html, str):
            return html.lstrip().lower().startswith("<html")
        return False

    @staticmethod
    def _is_error_html(html: str) -> bool:
        stripped = html.lstrip()
        return (
            stripped.startswith("<h1>Error rendering route:")
            or "data-nextpy-error-overlay=\"true\"" in stripped
            or "data-nextpy-error=\"true\"" in stripped
        )

    def _render_component_route(
        self,
        route: ComponentRoute,
        context: Dict[str, Any],
        include_layout: bool = True,
    ) -> str:
        """Render a component route (uncached implementation)."""
        from ..psx import render_psx
        from ..psx.core.parser import PSXElement

        debug = bool(getattr(route.renderer, "debug", False))

        try:
            # Merge layout metadata into context
            if hasattr(route, 'special_chains') and route.special_chains:
                metadata = self._merge_route_metadata(route.special_chains)
                context.update(metadata)
                if debug:
                    if _DEBUG: print(f"DEBUG: Merged metadata: {metadata}")

            # Get the page component (not rendered HTML)
            page_element = route.renderer.get_page_element(route.file_path, context)
            if debug:
                if _DEBUG: print(f"DEBUG: Page element type: {type(page_element)}")

            # Wrapper gives the client router a stable, layout-independent
            # node to swap during SPA fragment navigation.
            #
            # IMPORTANT: preserve the page's AST node. Re-wrapping a PSXElement
            # without ``_ast_node`` makes rendering fall back to ``to_ast()``,
            # which turns ComponentNodes (e.g. <Introduction />) into plain
            # HTML tags and breaks registered/imported components.
            from ..psx.core.ast_nodes import ElementNode, TextNode

            if page_element is None:
                raise ValueError("Page component returned None")

            page_ast = getattr(page_element, '_ast_node', None)
            if page_ast is None and hasattr(page_element, 'to_ast'):
                page_ast = page_element.to_ast()

            if page_ast is not None:
                wrapper_children = [page_ast]
            elif hasattr(page_element, 'to_html'):
                # interactive_component returns a rendered result that has no
                # PSX AST. Preserve its HTML instead of wrapping ``None``.
                wrapper_children = [TextNode(content=page_element.to_html())]
            else:
                wrapper_children = [TextNode(content=str(page_element))]

            wrapper = PSXElement(
                tag='div',
                props={'id': 'nextpy-page'},
                children=[page_element],
            )
            wrapper._ast_node = ElementNode(
                tag='div',
                attributes={'id': 'nextpy-page'},
                events={},
                children=wrapper_children,
                self_closing=False,
            )
            wrapper._psx_context = getattr(page_element, '_psx_context', {}) or context
            page_element = wrapper

            if include_layout:
                # Apply layout chain innermost-first so the root layout wraps everything.
                # layout_chain is stored [root, ..., inner] (reversed from collection order).
                # Iterating reversed() gives [inner, ..., root], so each iteration wraps
                # the current page_element — final result is root(inner(...(page))).
                if hasattr(route, 'layout_chain') and route.layout_chain:
                    for layout_path in reversed(route.layout_chain):
                        layout_func = self._load_layout(layout_path)
                        if debug:
                            if _DEBUG: print(f"DEBUG: Layout function: {layout_func}")
                        if layout_func:
                            try:
                                # Pass the page element directly as children so its _ast_node
                                # reference is preserved and to_html() renders it correctly.
                                children_element = page_element

                                # Add props to context for layout components
                                layout_context = {**context, 'props': context}
                                page_element = layout_func(children=children_element, **layout_context)
                                if debug:
                                    if _DEBUG: print(f"DEBUG: After layout, element type: {type(page_element)}")
                                # A nested layout may already provide the full document
                                # (e.g. /jobs). In that case the root layout must not
                                # wrap it again, otherwise the nested <html>/<body>
                                # document is emitted inside the root document.
                                if self._is_full_document(page_element) and layout_path != route.layout_chain[0]:
                                    break
                            except Exception as e:
                                print(f"Warning: Failed to apply layout {layout_path}: {e}")

            content = render_psx(page_element, context)
            if debug:
                if _DEBUG: print(f"DEBUG: Rendered content length: {len(content)}")
            return content

        except Exception as e:
            print(f"ERROR: Failed to render route: {e}")
            import traceback
            traceback.print_exc()

            if debug:
                from ..server.debug import render_debug_error_html
                return render_debug_error_html(
                    e,
                    request_path=str(getattr(route, "path", "") or ""),
                )

            # Try to render error boundary if available
            if hasattr(route, 'special_chains') and route.special_chains.get('error'):
                error_chain = route.special_chains['error']
                if error_chain:
                    try:
                        error_func = self._load_layout(error_chain[-1])  # Use closest error boundary
                        if error_func:
                            error_element = error_func(error=str(e), **context)
                            return render_psx(error_element, context)
                    except Exception as error_error:
                        print(f"ERROR: Failed to render error boundary: {error_error}")

            return '<h1 data-nextpy-error="true">Internal Server Error</h1>' 
    
    def handle_api_route(self, route: Route, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle API route requests"""
        if isinstance(route, ComponentRoute) and route.use_components:
            return route.renderer.render_api_route(route.file_path, request_data)
        elif route.handler and callable(route.handler):
            return route.handler(request_data)
        else:
            return {'error': f'API route {route.path} has no handler'}
        
    def get_all_routes(self) -> List[Route]:
        """Get all registered routes"""
        return self.routes + self.api_routes
        
    def get_static_routes(self) -> List[Route]:
        """Get only static (non-dynamic) routes for SSG"""
        return [r for r in self.routes if not r.is_dynamic]
        
    def reload_route(self, file_path: Path) -> None:
        """Reload a specific route (for hot reload)"""
        self.routes = [r for r in self.routes if r.file_path != file_path]
        self.api_routes = [r for r in self.api_routes if r.file_path != file_path]
        self._route_cache.clear()
        self.renderer.clear_cache()
        
        if file_path.exists():
            route = self._create_route_from_file(file_path)
            if route:
                if route.is_api:
                    self.api_routes.append(route)
                else:
                    self.routes.append(route)
                    
        self._sort_routes()
    
    def get_component_routes(self) -> List[ComponentRoute]:
        """Get only component-based routes"""
        return [r for r in self.routes if isinstance(r, ComponentRoute) and r.use_components]
    
    def get_template_routes(self) -> List[Route]:
        """Get only template-based routes"""
        return [r for r in self.routes if not (isinstance(r, ComponentRoute) and r.use_components)]


# Export the router instance
component_router = ComponentRouter()
