"""
NextPy Builder - Static Site Generation (SSG) with Build Optimization
Builds static HTML files to the out/ directory with code splitting and tree shaking
"""

import os
import shutil
import asyncio
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime

from nextpy.core.router import Route
from nextpy.core.component_router import ComponentRouter, ComponentRoute
from nextpy.core.renderer import Renderer
from nextpy.core.data_fetching import (
    PageContext,
    PropsResult,
    execute_data_fetching,
    execute_data_fetching_result,
    get_static_paths_for_route,
)


class Builder:
    """
    Static Site Generator for NextPy
    Builds all pages to static HTML in the out/ directory
    with optional build optimization (tree shaking, code splitting, minification)
    """
    
    def __init__(
        self,
        pages_dir: str = "pages",
        templates_dir: str = "templates",
        public_dir: str = "public",
        out_dir: str = "out",
        optimize: bool = True,
        minify: bool = True,
        tree_shaking: bool = True,
        code_splitting: bool = True,
    ):
        self.pages_dir = Path(pages_dir)
        self.templates_dir = Path(templates_dir)
        self.public_dir = Path(public_dir)
        self.out_dir = Path(out_dir)
        
        self.optimize = optimize
        self.minify = minify
        self.tree_shaking = tree_shaking
        self.code_splitting = code_splitting
        
        self.router = ComponentRouter(pages_dir, templates_dir)
        self.renderer = Renderer(templates_dir, pages_dir, public_dir)
        
        self.build_manifest: Dict[str, Any] = {
            "version": 1,
            "pages": {},
            "build_time": None,
            "optimization": {},
        }
        
    async def build(self, clean: bool = True) -> Dict[str, Any]:
        """
        Build all pages to static HTML with optional optimization
        
        Args:
            clean: Whether to clean the output directory first
            
        Returns:
            Build manifest with information about built pages
        """
        print("NextPy Build Starting...")
        start_time = datetime.now()

        self._ensure_database()
        
        if clean and self.out_dir.exists():
            shutil.rmtree(self.out_dir)
            
        self.out_dir.mkdir(parents=True, exist_ok=True)
        
        self._copy_public_files()
        
        self.router.scan_pages()
        
        await self._build_static_routes()
        
        await self._build_dynamic_routes()
        
        if self.optimize:
            self._run_optimization()
        
        self._create_sitemap()

        output_files = [
            item for item in self.out_dir.rglob("*") if item.is_file()
        ]
        self.build_manifest["files"] = [
            str(item.relative_to(self.out_dir)) for item in output_files
        ]
        self.build_manifest["assets"] = [
            str(item.relative_to(self.out_dir))
            for item in output_files
            if item.suffix.lower() in {".css", ".js", ".mjs", ".map", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".ico", ".woff", ".woff2", ".ttf"}
        ]
        self.build_manifest["total_size"] = sum(
            item.stat().st_size for item in output_files
        )
        
        self.build_manifest["build_time"] = datetime.now().isoformat()
        self._write_manifest()
        
        duration = (datetime.now() - start_time).total_seconds()
        print(f"\nBuild completed in {duration:.2f}s")
        print(f"Output directory: {self.out_dir}")
        
        return self.build_manifest

    def _ensure_database(self) -> None:
        """Initialize the default database before SSG pages query models."""
        try:
            from nextpy.db import get_db
            get_db()
        except Exception:
            try:
                from nextpy.config import settings
                from nextpy.db import init_db
                init_db(settings.get("database_url"))
            except Exception as exc:
                print(f"  Warning: database initialization skipped: {exc}")
        
    def _copy_public_files(self) -> None:
        """Copy files from public/ to out/"""
        if not self.public_dir.exists():
            return
            
        for item in self.public_dir.rglob("*"):
            if item.is_file():
                relative = item.relative_to(self.public_dir)
                dest = self.out_dir / relative
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, dest)
                
        print(f"Copied public files to {self.out_dir}")
        
    async def _build_static_routes(self) -> None:
        """Build all static (non-dynamic) routes"""
        static_routes = self.router.get_static_routes()
        
        for route in static_routes:
            if route.is_api:
                continue
                
            await self._build_page(route)
            
    async def _build_dynamic_routes(self) -> None:
        """Build dynamic routes using getStaticPaths"""
        dynamic_routes = [r for r in self.router.routes if r.is_dynamic]
        
        for route in dynamic_routes:
            if route.is_api:
                continue
                
            module = self._route_module(route)
            if module:
                paths_result = await get_static_paths_for_route(module)
                for path_config in paths_result.paths:
                    params = path_config.get("params", path_config)
                    await self._build_page(route, params)
                        
    async def _build_page(
        self, 
        route: Route, 
        params: Optional[Dict[str, str]] = None
    ) -> None:
        """Build a single page to static HTML"""
        params = params or {}
        
        path = self._resolve_path(route.path, params)
        
        context = PageContext(
            params=params,
            query={},
        )
        
        try:
            props = {}
            module = self._route_module(route)
            revalidate = None
            if module:
                props, revalidate = await execute_data_fetching_result(module, context)
                if revalidate is not None and hasattr(route, "renderer"):
                    route.renderer.revalidate_cache[str(route.file_path)] = int(revalidate)

            if isinstance(route, ComponentRoute) and getattr(route, "use_components", False):
                render_context = {
                    **props,
                    "params": params,
                    "query": {},
                    "__nextpy_props_loaded": True,
                }
                html = self.router.render_route(
                    route, render_context, include_layout=True
                )
                html = self._inject_runtime_scripts(html)
            else:
                template_name = self._get_template_for_route(route)
                html = await self.renderer.render_async(
                    template_name,
                    context={**props, "params": params},
                )

            output_path = self._get_output_path(path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(html)
            
            self.build_manifest["pages"][path] = {
                "file": str(output_path),
                "params": params,
            }
            
            print(f"  Built: {path} -> {output_path}")
            
        except Exception as e:
            print(f"  Error building {path}: {e}")
            
    def _route_module(self, route: Route) -> Optional[Any]:
        """Load the module for a component route or legacy handler route."""
        if isinstance(route, ComponentRoute):
            try:
                return route.renderer.load_component_module(route.file_path)
            except Exception:
                return None
        if route.handler:
            return self._get_module_from_handler(route.handler)
        return None

    def _inject_runtime_scripts(self, html: str) -> str:
        """Inject client router/CRUD runtimes into a built component page."""
        try:
            from nextpy.psx import CLIENT_ROUTER_SCRIPT, CRUD_RUNTIME_SCRIPT
        except Exception:
            return html

        def _insert(source: str, tag: str) -> str:
            index = source.lower().rfind("</body>")
            if index != -1:
                return source[:index] + tag + source[index:]
            return source + tag

        if "data-nextpy-crud" in html and 'data-nextpy-runtime="crud"' not in html:
            html = _insert(
                html,
                f'<script data-nextpy-runtime="crud">{CRUD_RUNTIME_SCRIPT}</script>',
            )
        if 'data-nextpy-runtime="router"' not in html:
            html = _insert(
                html,
                f'<script data-nextpy-runtime="router">{CLIENT_ROUTER_SCRIPT}</script>',
            )
        return html

    def _resolve_path(self, route_path: str, params: Dict[str, str]) -> str:
        """Resolve a dynamic route path with actual params"""
        path = route_path
        for key, value in params.items():
            path = path.replace(f"(?P<{key}>[^/]+)", value)
            path = path.replace(f"(?P<{key}>.+)", value)
        return path
        
    def _get_template_for_route(self, route: Route) -> str:
        """Get the template name for a route"""
        relative = route.file_path.relative_to(self.pages_dir)
        template_name = str(relative).replace(".py", ".html")
        
        template_path = self.templates_dir / template_name
        if template_path.exists():
            return template_name
            
        return "_page.html"
        
    def _get_output_path(self, path: str) -> Path:
        """Get the output file path for a URL path"""
        if path == "/":
            return self.out_dir / "index.html"
            
        clean_path = path.strip("/")
        if "." in clean_path.rsplit("/", 1)[-1]:
            return self.out_dir / clean_path
        return self.out_dir / clean_path / "index.html"
        
    def _get_module_from_handler(self, handler: Any) -> Optional[Any]:
        """Get the module that contains the handler"""
        if hasattr(handler, "__module__"):
            import sys
            return sys.modules.get(handler.__module__)
        return None
        
    def _run_optimization(self) -> None:
        """
        Run build optimization.

        - Tree shaking / code splitting: module dependency analysis over the
          project (report-only; results stored in the build manifest).
        - Minification: actually rewrites JS/CSS assets in the output dir.
        """
        try:
            from nextpy.build.optimizer import BuildOptimizer, BundleConfig, Minifier

            project_root = Path.cwd()
            entry_points = []
            for route in self.router.routes:
                file_path = getattr(route, "file_path", None)
                if not file_path or route.is_api:
                    continue
                try:
                    entry_points.append(
                        str(Path(file_path).resolve().relative_to(project_root))
                    )
                except ValueError:
                    continue

            config = BundleConfig(
                entry_points=entry_points,
                optimize=self.minify,
                tree_shaking=self.tree_shaking,
                code_splitting=self.code_splitting,
            )
            optimizer = BuildOptimizer(config=config)
            optimizer.analyze_project(str(project_root))

            opt_stats: Dict[str, Any] = {}

            if self.tree_shaking:
                removed = optimizer.perform_tree_shaking()
                opt_stats["tree_shaking"] = {
                    "entry_points": entry_points,
                    "unused_modules": removed,
                    "unused_count": len(removed),
                    "note": "report-only; no files were deleted",
                }

            if self.code_splitting:
                bundles = optimizer.perform_code_splitting()
                opt_stats["code_splitting"] = {
                    "chunk_count": len(bundles),
                    "chunks": {k: len(v) for k, v in bundles.items()},
                }

            if self.minify:
                opt_stats["minification"] = self._minify_output_assets(Minifier)

            try:
                from nextpy.build.assets import AssetBundler
                opt_stats["asset_chunks"] = AssetBundler(
                    self.out_dir, minify=False
                ).bundle(self.build_manifest.get("pages"))
            except Exception as exc:
                opt_stats["asset_chunks"] = {"error": str(exc)}

            opt_stats["bundle_report"] = optimizer.generate_bundle_report()

            self.build_manifest["optimization"] = opt_stats
            print("  Optimization complete")

        except ImportError:
            print("  Warning: Build optimizer not available, skipping optimization")
        except Exception as e:
            print(f"  Warning: Optimization failed: {e}")

    def _minify_output_assets(self, Minifier) -> Dict[str, int]:
        """Minify JS/CSS assets in the output directory"""
        savings = {"js_files": 0, "css_files": 0, "bytes_saved": 0}
        for ext, minify_method in [("js", Minifier.minify_javascript), ("css", Minifier.minify_css)]:
            for asset in self.out_dir.rglob(f"*.{ext}"):
                try:
                    original = asset.read_text()
                    minified = minify_method(original)
                    savings["bytes_saved"] += len(original) - len(minified)
                    if ext == "js":
                        savings["js_files"] += 1
                    else:
                        savings["css_files"] += 1
                    asset.write_text(minified)
                except Exception:
                    continue
        return savings

    def _create_sitemap(self) -> None:
        """Generate sitemap.xml"""
        pages = self.build_manifest["pages"]
        
        sitemap_lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        ]
        
        for path in pages:
            sitemap_lines.append(f"  <url>")
            sitemap_lines.append(f"    <loc>{path}</loc>")
            sitemap_lines.append(f"    <lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod>")
            sitemap_lines.append(f"  </url>")
            
        sitemap_lines.append("</urlset>")
        
        sitemap_path = self.out_dir / "sitemap.xml"
        sitemap_path.write_text("\n".join(sitemap_lines))
        print(f"  Generated: sitemap.xml")
        
    def _write_manifest(self) -> None:
        """Write the build manifest to the output directory"""
        import json
        manifest_path = self.out_dir / "_nextpy" / "build-manifest.json"
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(json.dumps(self.build_manifest, indent=2))


async def build_project(**kwargs) -> Dict[str, Any]:
    """Convenience function to build the project"""
    builder = Builder(**kwargs)
    return await builder.build()
