"""
NextPy CLI - Command-line interface for NextPy projects
Commands: dev, build, start
"""

import os
import sys
import time
import asyncio
import signal
from pathlib import Path
from typing import Optional

import click
import uvicorn
import subprocess
import shutil

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler

    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False
    Observer = None
    FileSystemEventHandler = None


class HotReloadHandler:
    """Handles file system changes for hot reload with enhanced JSX support"""

    def __init__(self, reload_callback, debug: bool = False):
        self.reload_callback = reload_callback
        self._debounce_timer = None
        self.debug = debug
        self.last_reload_time = 0
        self.reload_cooldown = 0.5  # 500ms cooldown between reloads

        # Enhanced file patterns for better JSX detection
        self.file_patterns = {
            "python": [".py", ".psx"],
            "jsx": [".py.jsx", ".jsx"],
            "templates": [".html", ".htm", ".jinja2", ".j2"],
            "styles": [".css", ".scss", ".sass", ".less"],
            "scripts": [".js", ".ts", ".mjs", ".cjs"],
            "assets": [".json", ".yaml", ".yml", ".toml", ".ini"],
            "config": [
                ".env",
                ".env.example",
                "requirements.txt",
                "package.json",
                "tailwind.config.js",
                "postcss.config.js",
            ],
        }

        # Directories to watch
        self.watch_dirs = {
            "pages",
            "components",
            "templates",
            "public",
            "static",
            "assets",
            "styles",
            "scripts",
            ".nextpy_framework",
        }

        # Files that should always trigger reload
        self.critical_files = {
            "main.py",
            "app.py",
            "config.py",
            "settings.py",
            "requirements.txt",
            "package.json",
            "pyproject.toml",
        }

    def _should_reload_file(self, file_path: str) -> bool:
        """Determine if a file change should trigger reload"""
        file_path = Path(file_path)

        # Always reload critical files
        if file_path.name in self.critical_files:
            return True

        # Check if file is in a watched directory
        parent_dirs = [part.name for part in file_path.parents]
        if not any(dir_name in self.watch_dirs for dir_name in parent_dirs):
            # If not in watched directories, check if it's in root
            if len(parent_dirs) == 0 or parent_dirs[-1] == ".":
                return any(
                    file_path.name.endswith(pattern)
                    for patterns in self.file_patterns.values()
                    for pattern in patterns
                )
            return False

        # Check file extension against all patterns
        all_extensions = []
        for patterns in self.file_patterns.values():
            all_extensions.extend(patterns)

        return any(file_path.name.endswith(ext) for ext in all_extensions)

    def _get_file_type(self, file_path: str) -> str:
        """Categorize file type for logging"""
        file_path = Path(file_path)

        for file_type, extensions in self.file_patterns.items():
            if any(file_path.name.endswith(ext) for ext in extensions):
                return file_type

        return "unknown"

    def _debounce_reload(self, file_path: str = None):
        """Debounce reload calls to prevent excessive reloading"""
        current_time = time.time()

        if current_time - self.last_reload_time < self.reload_cooldown:
            return

        self.last_reload_time = current_time

        if self.debug and file_path:
            file_type = self._get_file_type(file_path)
            click.echo(
                f"  🔄 Hot reload triggered by {file_type} file: {Path(file_path).name}",
                dim=True,
            )

        self._trigger_reload()

    def on_modified(self, event):
        """Handle file modification events"""
        if event.is_directory:
            return

        if self._should_reload_file(event.src_path):
            self._debounce_reload(event.src_path)

    def on_created(self, event):
        """Handle file creation events"""
        if not event.is_directory and self._should_reload_file(event.src_path):
            self._debounce_reload(event.src_path)

    def on_deleted(self, event):
        """Handle file deletion events"""
        if not event.is_directory and self._should_reload_file(event.src_path):
            self._debounce_reload(event.src_path)

    def on_moved(self, event):
        """Handle file move/rename events"""
        if not event.is_directory:
            # Handle both source and destination
            if hasattr(event, "dest_path") and event.dest_path:
                if self._should_reload_file(event.src_path) or self._should_reload_file(
                    event.dest_path
                ):
                    self._debounce_reload(event.dest_path or event.src_path)
            else:
                if self._should_reload_file(event.src_path):
                    self._debounce_reload(event.src_path)

    def _trigger_reload(self):
        """Trigger the reload callback"""
        if self.reload_callback:
            self.reload_callback()

    def setup_file_watcher(self, project_dir: str = "."):
        """Setup enhanced file watcher with specific patterns"""
        if not WATCHDOG_AVAILABLE:
            click.echo(
                "  ⚠️  Watchdog not installed. Hot reload disabled.", fg="yellow"
            )
            click.echo("  Install with: pip install watchdog", fg="yellow")
            return None

        observer = Observer()
        event_handler = WatchdogHotReloadHandler(self._trigger_reload, debug=self.debug)

        # Watch specific directories with recursive monitoring
        for watch_dir in self.watch_dirs:
            dir_path = Path(project_dir) / watch_dir
            if dir_path.exists():
                observer.schedule(event_handler, str(dir_path), recursive=True)
                if self.debug:
                    click.echo(f"  📁 Watching directory: {watch_dir}", dim=True)

        # Also watch root directory for critical files
        root_path = Path(project_dir)
        if root_path.exists():
            observer.schedule(event_handler, str(root_path), recursive=False)

        return observer


if WATCHDOG_AVAILABLE:

    class WatchdogHotReloadHandler(HotReloadHandler, FileSystemEventHandler):
        """Enhanced watchdog handler with better file filtering"""

        pass

else:

    class WatchdogHotReloadHandler(HotReloadHandler):
        """Fallback handler when watchdog is not available"""

        pass


def find_main_module():
    # main.py is always expected at the project root for NextPy projects
    # We ensure the current directory is in sys.path before calling uvicorn.run
    return "main:app"


def _format_size(size_bytes: int) -> str:
    """Format file size in human-readable format"""
    if size_bytes == 0:
        return "0 B"

    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    size = float(size_bytes)

    while size >= 1024.0 and i < len(size_names) - 1:
        size /= 1024.0
        i += 1

    return f"{size:.1f} {size_names[i]}"


@click.group()
@click.version_option(version="3.7.1", prog_name="NextPy")
def cli():
    """NextPy - The Python Web Framework"""
    pass


@cli.command()
@click.option("--port", "-p", default=8000, help="Port to run the server on")
@click.option("--host", "-h", default="0.0.0.0", help="Host to bind to")
@click.option("--reload/--no-reload", default=True, help="Enable hot reload")
@click.option("--debug/--no-debug", default=True, help="Enable debug mode")
def dev(port: int, host: str, reload: bool, debug: bool):
    """Start the development server with enhanced hot reload"""
    click.echo(click.style("\n  NextPy Development Server", fg="cyan", bold=True))
    click.echo(click.style("  ========================\n", fg="cyan"))

    # Set debug environment variable
    if debug:
        os.environ["NEXTPY_DEBUG"] = "true"
        os.environ["DEBUG"] = "true"
        os.environ["DEVELOPMENT"] = "true"
    else:
        os.environ.pop("NEXTPY_DEBUG", None)
        os.environ.pop("DEBUG", None)
        os.environ.pop("DEVELOPMENT", None)

    _ensure_project_structure()

    click.echo(f"  - Mode:     {'Development' if debug else 'Production'}")
    click.echo(f"  - Host:     {host} (accessible at http://localhost:{port})")
    click.echo(f"  - Port:     {port}")
    click.echo(f"  - Reload:   {'Enabled' if reload else 'Disabled'}")
    click.echo(f"  - Debug:    {'Enabled' if debug else 'Disabled'}")

    if reload and not WATCHDOG_AVAILABLE:
        click.echo(
            click.style(
                "  - Watchdog: Not Available (install: pip install watchdog)",
                fg="yellow",
            )
        )
    elif reload:
        click.echo(f"  - Watchdog: Available")

    if debug:
        click.echo(f"  - Debug Icon:  Auto-enabled")
        click.echo(f"  - Console Capture: Enabled")
        click.echo(f"  - Performance Monitoring: Enabled")

    click.echo(f"\n   Server ready at http://0.0.0.0:{port}")
    click.echo(f"   Open http://localhost:{port} in your browser\n")

    project_dir = Path(".")
    os.chdir(project_dir)

    # Ensure the current directory is in sys.path for module discovery
    if str(project_dir.resolve()) not in sys.path:
        sys.path.insert(0, str(project_dir.resolve()))

    main_module = find_main_module()

    if reload:
        # Enhanced reload configuration with JSX support
        reload_dirs = [
            "pages",
            "components",
            "templates",
            "public",
            "static",
            "styles",
            "scripts",
            ".nextpy_framework",
        ]

        # Filter to only existing directories
        existing_reload_dirs = []
        for reload_dir in reload_dirs:
            dir_path = project_dir / reload_dir
            if dir_path.exists():
                existing_reload_dirs.append(reload_dir)
                if debug:
                    click.echo(click.style(f"  Watching: {reload_dir}/"))

        # Enhanced reload patterns for JSX files
        reload_includes = [
            "*.py",
            "*.psx",
            "*.py.jsx",
            "*.jsx",
            "*.html",
            "*.htm",
            "*.css",
            "*.scss",
            "*.sass",
            "*.less",
            "*.js",
            "*.ts",
            "*.json",
            "*.yaml",
            "*.yml",
            "*.env",
            "requirements.txt",
            "package.json",
            "tailwind.config.js",
            "postcss.config.js",
        ]

        uvicorn.run(
            main_module,
            host=host,
            port=port,
            reload=True,
            reload_dirs=existing_reload_dirs,
            reload_includes=reload_includes,
            log_level="info",
        )
    else:
        uvicorn.run(
            main_module,
            host=host,
            port=port,
            log_level="info",
        )


@cli.command()
@click.option("--out", "-o", default="out", help="Output directory for static files")
@click.option("--clean/--no-clean", default=True, help="Clean output directory first")
def build(out: str, clean: bool):
    """Build the project for production with enhanced feedback"""
    click.echo(click.style("\n  🔨 NextPy Static Build", fg="green", bold=True))
    click.echo(click.style("  ===================\n", fg="green"))

    try:
        from nextpy.core.builder import Builder

        click.echo(f"Output directory: {out}/")
        if clean:
            click.echo(f"Cleaning output directory...")

        click.echo(f"Initializing builder...")
        builder = Builder(out_dir=out)

        click.echo(f"Building static files...")

        async def run_build():
            manifest = await builder.build(clean=clean)
            return manifest

        manifest = asyncio.run(run_build())

        pages_count = len(manifest.get("pages", {}))
        assets_count = len(manifest.get("assets", []))
        total_size = manifest.get("total_size", 0)

        click.echo()
        click.echo(
            click.style(f"Build completed successfully!", fg="green", bold=True)
        )
        click.echo(f"Pages built: {pages_count}")
        click.echo(f"Assets processed: {assets_count}")
        click.echo(f"Total size: {_format_size(total_size)}")
        click.echo(f"Output: {out}/")
        click.echo()
        click.echo(click.style(f"Ready for deployment!", fg="cyan", bold=True))
        click.echo(f"Serve with: nextpy start --port 5000")
        click.echo()

    except Exception as e:
        click.echo(click.style(f"Build failed: {str(e)}", fg="red"))
        if "Builder" not in str(e):
            click.echo(
                click.style(
                    f"Make sure you're in a NextPy project directory", fg="yellow"
                )
            )


@cli.command()
@click.option("--port", "-p", default=5000, help="Port to run the server on")
@click.option("--host", "-h", default="0.0.0.0", help="Host to bind to")
def start(port: int, host: str):
    """Start the production server with enhanced feedback"""
    click.echo(click.style("\n🚀 NextPy Production Server", fg="green", bold=True))
    click.echo(click.style("========================\n", fg="green"))

    click.echo(f"Mode:     Production")
    click.echo(f"Host:     {host} (accessible at http://localhost:{port})")
    click.echo(f"Port:     {port}")
    click.echo(f"Workers:   4 (multi-process)")
    click.echo(f"Logging:  Warning level only")

    click.echo(f"\n Production server ready at http://0.0.0.0:{port}")
    click.echo(f"Open http://localhost:{port} in your browser\n")
    click.echo(click.style(f"Press Ctrl+C to stop the server", fg="yellow"))
    click.echo()

    try:
        os.chdir(Path.cwd())

        uvicorn.run(
            "main:app",
            host=host,
            port=port,
            workers=4,
            log_level="warning",
        )

    except KeyboardInterrupt:
        click.echo(click.style("\nServer stopped gracefully", fg="cyan"))
    except Exception as e:
        click.echo(click.style(f"\nServer error: {str(e)}", fg="red"))
        click.echo(
            click.style(
                f"Make sure you have a main.py file with an app instance",
                fg="yellow",
            )
        )


@cli.command()
@click.argument("name")
@click.option("--psx/--no-psx", default=True, help="Create with PSX (True JSX) support")
@click.option("--template", default="default", help="Project template to use")
def create(name: str, psx: bool, template: str):
    """Create a new NextPy project with True PSX support"""
    click.echo(
        click.style(f"\n🚀 Creating NextPy project: {name}", fg="cyan", bold=True)
    )
    click.echo(click.style(" " + "=" * (25 + len(name)) + "\n", fg="cyan"))

    if psx:
        click.echo(
            click.style("  ✨ PSX (True JSX) Support: ENABLED", fg="green", bold=True)
        )
        click.echo(click.style("     • Write exact JSX syntax in Python", fg="green"))
        click.echo(click.style("     • Revolutionary Python logic in JSX", fg="green"))
        click.echo(click.style("     • Optimized Virtual DOM included", fg="green"))

    project_dir = Path(name)

    if project_dir.exists():
        if any(project_dir.iterdir()):
            click.echo(
                click.style(
                    f"Directory '{name}' already exists and is not empty", fg="red"
                )
            )
            return
        else:
            click.echo(
                click.style(
                    f" Directory '{name}' exists but is empty", fg="yellow"
                )
            )

    click.echo(f"Creating project structure...")

    try:
        _create_project_structure(project_dir, psx=psx, template=template)

        click.echo(
            click.style(f"Project successfully created!", fg="green", bold=True)
        )
        click.echo(f"\nLocation: {project_dir.absolute()}")

        # Attempt to install Node and Python dependencies, then build Tailwind for the new project
        try:
            # Ensure project_dir exists and has package.json
            if (project_dir / "package.json").exists():
                if shutil.which("npm") is None:
                    click.echo(
                        click.style(
                            " npm not found; please install Node.js and npm to build Tailwind automatically.",
                            fg="yellow",
                        )
                    )
                else:
                    click.echo(
                        "  ▶ Installing Node dependencies (this may take a while)..."
                    )
                    npm_cmd = (
                        ["npm", "ci"]
                        if (project_dir / "package-lock.json").exists()
                        or (project_dir / "npm-shrinkwrap.json").exists()
                        else ["npm", "install"]
                    )
                    subprocess.run(npm_cmd, cwd=str(project_dir), check=True)

                    click.echo("  ▶ Building Tailwind CSS...")
                    # Prefer the build script if present
                    try:
                        subprocess.run(
                            ["npm", "run", "build:tailwind"],
                            cwd=str(project_dir),
                            check=True,
                        )
                    except subprocess.CalledProcessError:
                        # Fallback to npx invocation
                        if shutil.which("npx"):
                            subprocess.run(
                                [
                                    "npx",
                                    "tailwindcss",
                                    "-i",
                                    "./styles/styles.css",
                                    "-o",
                                    "./public/tailwind.css",
                                    "--minify",
                                ],
                                cwd=str(project_dir),
                                check=True,
                            )
                        else:
                            click.echo(
                                click.style(
                                    "  npx not found; unable to run Tailwind build automatically.",
                                    fg="yellow",
                                )
                            )
            else:
                click.echo(
                    click.style(
                        " package.json not found; skipping Node install/build.",
                        fg="yellow",
                    )
                )

            # Install Python requirements if available
            if (project_dir / "requirements.txt").exists():
                click.echo("  ▶ Installing Python dependencies (requirements.txt)...")
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
                    cwd=str(project_dir),
                    check=True,
                )
            else:
                click.echo(
                    click.style(
                        " requirements.txt not found; skipping Python dependencies installation.",
                        fg="yellow",
                    )
                )

        except subprocess.CalledProcessError as e:
            click.echo(
                click.style(f" Automatic install/build failed: {e}", fg="red")
            )
            click.echo(
                click.style(
                    " You can retry manually: cd {0} && npm install && npm run build:tailwind && {1} -m pip install -r requirements.txt".format(
                        name, sys.executable
                    ),
                    fg="yellow",
                )
            )

        click.echo(f"\nNext steps:")
        click.echo(f"cd {name}")
        click.echo(
            f" npm install  # Install Tailwind CSS dependencies (if not already installed)"
        )
        click.echo(
            f" pip install -r requirements.txt  # Install Python dependencies (if not already installed)"
        )
        click.echo(
            f" npm run css:build  # Build Tailwind CSS (if you prefer manual build)"
        )
        click.echo(f" python3 main.py  # Start development server")
        click.echo(f"  Open http://localhost:5000 in your browser")

        if psx:
            click.echo(f"\nPSX Development:")
            click.echo(f"    • All PSX utilities, hooks & components auto-imported")
            click.echo(f"    • Use: from nextpy import component, useState, useEffect")
            click.echo(f"    • Full auto-completion & IntelliSense support")
            click.echo(f"    • Edit pages/index.py to see PSX in action")
            click.echo(f"    • Use @component decorator for JSX syntax")
            click.echo(f"    • Try: {{for item in items:<div>{{item}}</div>}}")
            click.echo(f"    • PSX devtools copied to .nextpy/devtools/")
            click.echo(f"    • Install VS Code extension: nextpy-psx")
            click.echo(f"    • Language server: .nextpy/devtools/psx-language-server")

        click.echo()

    except Exception as e:
        click.echo(click.style(f" Failed to create project: {str(e)}", fg="red"))
        click.echo(
            click.style(
                f" Check the error message above for more details", fg="yellow"
            )
        )
        # Clean up partial creation
        if project_dir.exists():
            shutil.rmtree(project_dir, ignore_errors=True)

        click.echo(click.style(f" Cleaned up partial files", fg="yellow"))


@cli.command()
def routes():
    """Display all registered routes with detailed information"""
    click.echo(click.style("\n  NextPy Routes Overview", fg="cyan", bold=True))
    click.echo(click.style("  =====================\n", fg="cyan"))

    try:
        from nextpy.core.router import Router

        router = Router()
        router.scan_pages()

        page_routes = [r for r in router.routes if not r.is_api]
        api_routes = router.api_routes

        click.echo(
            click.style(
                f" Page Routes ({len(page_routes)} total)", fg="blue", bold=True
            )
        )
        if page_routes:
            for i, route in enumerate(page_routes, 1):
                dynamic = " 🔀" if route.is_dynamic else " 📄"
                file_info = f"({route.file_path})"
                click.echo(f"    {i:2d}. {dynamic} {route.path:<30} {file_info}")
        else:
            click.echo(f" No page routes found")

        click.echo()
        click.echo(
            click.style(
                f"  API Routes ({len(api_routes)} total)", fg="green", bold=True
            )
        )
        if api_routes:
            for i, route in enumerate(api_routes, 1):
                dynamic = " 🔀" if route.is_dynamic else " 🔌"
                file_info = f"({route.file_path})"
                methods = (
                    "[GET, POST, PUT, DELETE]" if hasattr(route, "handler") else "[GET]"
                )
                click.echo(
                    f"    {i:2d}. {dynamic} {route.path:<30} {methods:<20} {file_info}"
                )
        else:
            click.echo(f"No API routes found")

        click.echo()
        click.echo(click.style(f"Summary:", fg="yellow", bold=True))
        click.echo(f"    Total Routes: {len(page_routes + api_routes)}")
        click.echo(
            f"    Dynamic Routes: {len([r for r in page_routes + api_routes if r.is_dynamic])}"
        )
        click.echo(
            f"    Static Routes: {len([r for r in page_routes + api_routes if not r.is_dynamic])}"
        )
        click.echo()

    except Exception as e:
        click.echo(click.style(f"  ❌ Error scanning routes: {str(e)}", fg="red"))


@cli.command()
@click.option("--out", "-o", default="out", help="Output directory for static files")
def export(out: str):
    """Export static files with enhanced feedback"""
    click.echo(click.style("\nNextPy Export", fg="green", bold=True))
    click.echo(click.style("  =============\n", fg="green"))

    try:
        from nextpy.core.builder import Builder

        click.echo(f"Output directory: {out}/")
        click.echo(f" Initializing exporter...")

        builder = Builder(out_dir=out)

        click.echo(f"Exporting static files...")

        async def run_export():
            manifest = await builder.export_static()
            return manifest

        manifest = asyncio.run(run_export())

        files_count = len(manifest.get("files", []))
        total_size = manifest.get("total_size", 0)

        click.echo()
        click.echo(
            click.style(f"Export completed successfully!", fg="green", bold=True)
        )
        click.echo(f"Files exported: {files_count}")
        click.echo(f"Total size: {_format_size(total_size)}")
        click.echo(f"Output: {out}/")
        click.echo()
        click.echo(click.style(f"Ready for static hosting!", fg="cyan", bold=True))
        click.echo()

    except Exception as e:
        click.echo(click.style(f"Export failed: {str(e)}", fg="red"))
        click.echo(
            click.style(
                f"  💡 Make sure you're in a NextPy project directory", fg="yellow"
            )
        )


@cli.command()
def version():
    """Show version and system information"""
    click.echo(click.style("\nNextPy Framework Info", fg="cyan", bold=True))
    click.echo(click.style("  ===================\n", fg="cyan"))

    click.echo(f"Version: 4.0.0 ")
    click.echo(f"Python: {sys.version.split()[0]}")
    click.echo(f"Framework: NextPy")
    click.echo(f"Architecture: True JSX")
    click.echo(f"Development Server: uvicorn")
    click.echo(f"Hot Reload: Available")
    click.echo(f"Static Files: Available")
    click.echo(f"API Routes: Available")
    click.echo(f"Page Routes: Available")
    click.echo(f"Component Routes: Available")
    click.echo(f"Component Library: Available")
    click.echo(f"Developer: RAHIMSTUDIOS")
    click.echo(f"License: MIT")
    click.echo(f"GitHub: https://github.com/IRAHIMSTUDIOS/nextpy-framework")
    click.echo(f"Documentation: https://nextpy.org/docs")
    click.echo(f"Support: https://github.com/RAHIMSTUDIOS/nextpy-framework/issues")

    click.echo()


@cli.command()
def info():
    """Show comprehensive framework and system information"""
    click.echo(click.style("\n NextPy System Information", fg="cyan", bold=True))
    click.echo(click.style("  ==========================\n", fg="cyan"))

    # Framework info
    click.echo(click.style("Framework Details:", fg="blue", bold=True))
    click.echo(f"    Version: 2.4.4")
    click.echo(f"    Architecture: True JSX")
    click.echo(f"    Python: {sys.version.split()[0]}")

    # Feature status
    click.echo(click.style("\n  ⚡ Feature Status:", fg="green", bold=True))
    watchdog_status = (
        "Available"
        if WATCHDOG_AVAILABLE
        else "❌ Not Available (pip install watchdog)"
    )
    click.echo(f"    Hot Reload: {watchdog_status}")
    click.echo(f"    Static Files:  Available")
    click.echo(f"    API Routes: Available")
    click.echo(f"    Page Routes: Available")
    click.echo(f"    Component Library: Available")

    # Project structure check
    click.echo(click.style("\n Project Structure:", fg="yellow", bold=True))
    required_dirs = ["pages", "components", "templates", "public"]
    for dir_name in required_dirs:
        status = "✅" if Path(dir_name).exists() else "❌"
        click.echo(f"    {dir_name}/: {status}")

    # Available commands
    click.echo(click.style("\n  🛠️  Available Commands:", fg="purple", bold=True))
    commands = [
        ("nextpy dev", "Start development server"),
        ("nextpy build", "Build for production"),
        ("nextpy start", "Start production server"),
        ("nextpy create <name>", "Create new project"),
        ("nextpy generate <type> <name>", "Generate components/pages/APIs"),
        ("nextpy routes", "Show all routes"),
        ("nextpy export", "Export static files"),
        ("nextpy version", "Show version info"),
        ("nextpy info", "Show this information"),
    ]
    for cmd, desc in commands:
        click.echo(f"    {cmd:<25} - {desc}")

    click.echo()


@cli.command()
@click.argument("type", type=click.Choice(["page", "api", "component"]))
@click.argument("name")
def generate(type: str, name: str):
    """Generate new page, API endpoint, or component"""
    click.echo(click.style(f"\n  Generating {type}: {name}", fg="cyan", bold=True))
    click.echo(click.style("  " + "=" * (20 + len(name) + len(type)) + "\n", fg="cyan"))

    if type == "page":
        _generate_page(name)
    elif type == "api":
        _generate_api(name)
    elif type == "component":
        _generate_component(name)

    click.echo(
        click.style(
            f"\n  {type.title()} '{name}' created successfully!\n",
            fg="green",
            bold=True,
        )
    )


@cli.group()
def plugin():
    """Plugin management commands"""
    pass


@plugin.command()
def list():
    """List all available plugins"""
    click.echo(click.style("\n  🔌 NextPy Plugins", fg="cyan", bold=True))
    click.echo(click.style("  ================\n", fg="cyan"))

    try:
        from nextpy.plugins import plugin_manager

        plugin_info = plugin_manager.get_plugin_info()

        click.echo(click.style(f"  📊 Overview:", fg="blue", bold=True))
        click.echo(f"    Total plugins: {plugin_info['total_plugins']}")
        click.echo(f"    Enabled: {plugin_info['enabled_plugins']}")
        click.echo(
            f"    Disabled: {plugin_info['total_plugins'] - plugin_info['enabled_plugins']}"
        )

        click.echo()
        click.echo(click.style(f"  📋 Plugin Details:", fg="green", bold=True))

        for plugin in plugin_info["plugins"]:
            status = "✅" if plugin["enabled"] else "❌"
            priority = plugin["priority"]
            click.echo(
                f"    {status} {plugin['name']:<15} v{plugin['version']:<8} (Priority: {priority})"
            )

            if plugin["dependencies"]:
                click.echo(f"        Dependencies: {', '.join(plugin['dependencies'])}")

        click.echo()

    except ImportError:
        click.echo(click.style("  ❌ Plugin system not available", fg="red"))
        click.echo(
            click.style("  💡 Install with: pip install nextpy[plugins]", fg="yellow")
        )
    except Exception as e:
        click.echo(click.style(f"  ❌ Error: {str(e)}", fg="red"))


@plugin.command()
@click.argument("name")
@click.option("--enable/--disable", default=True, help="Enable or disable the plugin")
def enable(name: str, enable: bool):
    """Enable or disable a plugin"""
    action = "Enabling" if enable else "Disabling"
    click.echo(click.style(f"\n  {action} plugin: {name}", fg="cyan", bold=True))
    click.echo(click.style("  " + "=" * (20 + len(name)) + "\n", fg="cyan"))

    try:
        from nextpy.plugins import plugin_manager

        if enable:
            plugin_manager.enable_plugin(name)
            click.echo(
                click.style(f"  ✅ Plugin '{name}' enabled successfully", fg="green")
            )
        else:
            plugin_manager.disable_plugin(name)
            click.echo(click.style(f"  ❌ Plugin '{name}' disabled", fg="yellow"))

        click.echo()

    except ImportError:
        click.echo(click.style("  ❌ Plugin system not available", fg="red"))
    except Exception as e:
        click.echo(click.style(f"  ❌ Error: {str(e)}", fg="red"))


@plugin.command()
@click.argument("name")
@click.option("--config", help="Plugin configuration as JSON string")
def configure(name: str, config: str):
    """Configure a plugin"""
    click.echo(click.style(f"\n  ⚙️  Configuring plugin: {name}", fg="cyan", bold=True))
    click.echo(click.style("  " + "=" * (20 + len(name)) + "\n", fg="cyan"))

    try:
        from nextpy.plugins import plugin_manager
        import json

        if config:
            try:
                config_dict = json.loads(config)
            except json.JSONDecodeError:
                click.echo(click.style("  ❌ Invalid JSON configuration", fg="red"))
                return
        else:
            config_dict = {}

        plugin_manager.configure_plugin(name, config_dict)
        click.echo(
            click.style(f"  ✅ Plugin '{name}' configured successfully", fg="green")
        )

        if config_dict:
            click.echo(f"  Configuration: {json.dumps(config_dict, indent=2)}")

        click.echo()

    except ImportError:
        click.echo(click.style("  ❌ Plugin system not available", fg="red"))
    except Exception as e:
        click.echo(click.style(f"  ❌ Error: {str(e)}", fg="red"))


@plugin.command()
@click.argument("file_path", type=click.Path(exists=True))
def load(file_path: str):
    """Load a plugin from file"""
    click.echo(
        click.style(f"\n  📦 Loading plugin from: {file_path}", fg="cyan", bold=True)
    )
    click.echo(click.style("  " + "=" * (25 + len(file_path)) + "\n", fg="cyan"))

    try:
        from nextpy.plugins import plugin_manager
        from pathlib import Path

        plugin = plugin_manager.load_plugin_from_file(Path(file_path))
        plugin_manager.register_plugin(plugin)

        click.echo(
            click.style(f"  ✅ Plugin '{plugin.name}' loaded successfully", fg="green")
        )
        click.echo(f"  Version: {plugin.version}")
        click.echo(f"  Priority: {plugin.priority.value}")

        click.echo()

    except ImportError:
        click.echo(click.style("  ❌ Plugin system not available", fg="red"))
    except Exception as e:
        click.echo(click.style(f"  ❌ Error: {str(e)}", fg="red"))


def _generate_page(name: str):
    """Generate a new page"""
    page_path = Path(f"pages/{name}.py")
    page_path.parent.mkdir(parents=True, exist_ok=True)

    content = f'''"""Generated {name} page"""
    
from nextpy.psx import interactive_component as component

@component
def {name.title()}(props = None):
    """{name.title()} page component"""
    props = props or {{}}
    
    title = props.get("title", "{name.title()} Page")
    
    return (
        <div className="max-w-4xl px-4 py-12 mx-auto">
            <h1 className="mb-6 text-4xl font-bold text-gray-900">{{title}}</h1>
            <p className="text-lg text-gray-600">
                This is the {name} page generated by NextPy.
            </p>
        </div>
    )

def getServerSideProps(context):
    return {{
        "props": {{
            "title": "{name.title()} Page"
        }}
    }}

default = {name.title()}
'''

    page_path.write_text(content)
    click.echo(f"  Created: {page_path}")


def _generate_api(name: str):
    """Generate a new API endpoint"""
    api_path = Path(f"pages/api/{name}.py")
    api_path.parent.mkdir(parents=True, exist_ok=True)

    content = f'''"""Generated {name} API endpoint"""

async def get(request):
    """GET /api/{name}"""
    return {{
        "message": "Hello from {name} API!",
        "endpoint": "/api/{name}",
        "method": "GET"
    }}

async def post(request):
    """POST /api/{name}"""
    body = await request.json()
    return {{
        "message": "POST request received",
        "data": body,
        "endpoint": "/api/{name}",
        "method": "POST"
    }}
'''

    api_path.write_text(content)
    click.echo(f"  Created: {api_path}")


def _generate_component(name: str):
    """Generate a new component"""
    component_path = Path(f"components/{name}.py")
    component_path.parent.mkdir(parents=True, exist_ok=True)

    content = f'''"""Generated {name} component"""

def {name.title()}(props = None):
    """{name.title()} component"""
    props = props or {{}}
    
    children = props.get("children", "")
    className = props.get("className", "")
    
    return (
        <div className="{name.lower()}-component " + className>
            {{children}}
        </div>
    )

default = {name.title()}
'''

    component_path.write_text(content)
    click.echo(f"  Created: {component_path}")


def _ensure_project_structure():
    """Ensure the basic project structure exists"""
    dirs = ["pages", "pages/api", "templates", "public", "public/css", "public/js"]

    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)


def _create_project_structure(
    project_dir: Path, psx: bool = True, template: str = "default"
):
    """Create a complete NextPy project structure with PSX support"""
    dirs = [
        "pages",
        "pages/blog",
        "pages/api",
        "pages/api/users",
        "components",
        "components/ui",
        "components/layout",
        "docs",
        "hooks",
        "styles",
        "public",
        "public/images",
        "public/fonts",
        "public/css",
        "public/js",
        "middleware",
        "templates",
        "tests",
        "utils",
        ".nextpy",
        ".nextpy/plugins",
        ".vscode",
        "static",
        "models"
    ]

    for dir_path in dirs:
        (project_dir / dir_path).mkdir(parents=True, exist_ok=True)
        click.echo(f"  Created: {dir_path}/")

    # Create essential templates
    (project_dir / "templates" / "_page.html").write_text("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{{ title or "NextPy App" }}</title>
    <!-- reference compiled Tailwind CSS rather than CDN for better integration -->
    <link href="/public/tailwind.css" rel="stylesheet">
</head>
<body>
    <div id="app">
        {{ content }}
    </div>
</body>
</html>""")
    click.echo("  Created: templates/_page.html")

    (project_dir / "templates" / "_404.html").write_text("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>404 - Page Not Found</title>
    <link href="/public/tailwind.css" rel="stylesheet">
</head>
<body class="flex items-center justify-center min-h-screen bg-gray-100">
    <div class="text-center">
        <h1 class="mb-4 text-6xl font-bold text-gray-900">404</h1>
        <p class="mb-8 text-xl text-gray-600">Page not found</p>
        <a href="/" class="px-6 py-3 text-white bg-blue-600 rounded-lg hover:bg-blue-700">
            Go Home
        </a>
    </div>
</body>
</html>""")
    click.echo("  Created: templates/_404.html")
    
    try:
        from importlib.resources import files, as_file
        import shutil

        images_dir = project_dir / "public" / "images"
        images_dir.mkdir(parents=True, exist_ok=True)

        logo_source = files("nextpy.public").joinpath("logo.png")

        with as_file(logo_source) as logo_path:
            shutil.copy2(
                logo_path,
                images_dir / "logo.png"
            )
        click.echo("  Copied: logo.png to public/images/")
    except Exception as e:
        click.echo(click.style(f"  ⚠️  Failed to copy logo.png: {str(e)}", fg="yellow"))
    
    #create minimal stylesheet
    (project_dir / "public" / "css"/ "styles.css").write_text("""/* NextPy Styles */
body{
    margin: 0;
    padding: 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}
""")
    
    click.echo("  Created: public/css/styles.css")
   


    # Create styles.css with Tailwind directives
    (project_dir / "styles" / "styles.css").write_text("""/* NextPy Styles */
@import "tailwindcss";

@source "../templates/**/*.html";
@source "../pages/**/*.{py,jsx,html}";
@source "../components/**/*.{py,jsx,html}";
@source "../../../templates/**/*.html";
@source "../../../pages/**/*.{py,jsx,html}";
@source "../../../components/**/*.{py,jsx,html}";

.from-blue-100 { --tw-gradient-from: rgb(219 234 254); --tw-gradient-stops: var(--tw-gradient-from), var(--tw-gradient-to, rgb(255 255 255 / 0)); }
.from-blue-200 { --tw-gradient-from: rgb(191 219 254); --tw-gradient-stops: var(--tw-gradient-from), var(--tw-gradient-to, rgb(255 255 255 / 0)); }
.from-blue-300 { --tw-gradient-from: rgb(147 197 253); --tw-gradient-stops: var(--tw-gradient-from), var(--tw-gradient-to, rgb(255 255 255 / 0)); }
.from-blue-400 { --tw-gradient-from: rgb(96 165 250); --tw-gradient-stops: var(--tw-gradient-from), var(--tw-gradient-to, rgb(255 255 255 / 0)); }
.from-blue-500 { --tw-gradient-from: rgb(59 130 246); --tw-gradient-stops: var(--tw-gradient-from), var(--tw-gradient-to, rgb(255 255 255 / 0)); }
.from-blue-600 { --tw-gradient-from: rgb(37 99 235); --tw-gradient-stops: var(--tw-gradient-from), var(--tw-gradient-to, rgb(255 255 255 / 0)); }
.from-blue-700 { --tw-gradient-from: rgb(29 78 216); --tw-gradient-stops: var(--tw-gradient-from), var(--tw-gradient-to, rgb(255 255 255 / 0)); }

.via-indigo-50 { --tw-gradient-via: rgb(248 250 252); --tw-gradient-stops: var(--tw-gradient-from), var(--tw-gradient-via), var(--tw-gradient-to, rgb(255 255 255 / 0)); }
.via-indigo-100 { --tw-gradient-via: rgb(241 245 249); --tw-gradient-stops: var(--tw-gradient-from), var(--tw-gradient-via), var(--tw-gradient-to, rgb(255 255 255 / 0)); }
.via-indigo-200 { --tw-gradient-via: rgb(226 232 240); --tw-gradient-stops: var(--tw-gradient-from), var(--tw-gradient-via), var(--tw-gradient-to, rgb(255 255 255 / 0)); }
.via-indigo-300 { --tw-gradient-via: rgb(203 213 225); --tw-gradient-stops: var(--tw-gradient-from), var(--tw-gradient-via), var(--tw-gradient-to, rgb(255 255 255 / 0)); }
.via-indigo-400 { --tw-gradient-via: rgb(148 163 184); --tw-gradient-stops: var(--tw-gradient-from), var(--tw-gradient-via), var(--tw-gradient-to, rgb(255 255 255 / 0)); }
.via-indigo-500 { --tw-gradient-via: rgb(100 116 139); --tw-gradient-stops: var(--tw-gradient-from), var(--tw-gradient-via), var(--tw-gradient-to, rgb(255 255 255 / 0)); }
.via-indigo-600 { --tw-gradient-via: rgb(71 85 105); --tw-gradient-stops: var(--tw-gradient-from), var(--tw-gradient-via), var(--tw-gradient-to, rgb(255 255 255 / 0)); }
.via-indigo-700 { --tw-gradient-via: rgb(51 65 85); --tw-gradient-stops: var(--tw-gradient-from), var(--tw-gradient-via), var(--tw-gradient-to, rgb(255 255 255 / 0)); }

.to-purple-50 { --tw-gradient-to: rgb(250 245 255); }
.to-purple-100 { --tw-gradient-to: rgb(243 232 255); }
.to-purple-200 { --tw-gradient-to: rgb(233 213 255); }
.to-purple-300 { --tw-gradient-to: rgb(216 180 254); }
.to-purple-400 { --tw-gradient-to: rgb(196 181 253); }
.to-purple-500 { --tw-gradient-to: rgb(168 85 247); }
.to-purple-600 { --tw-gradient-to: rgb(147 51 234); }
.to-purple-700 { --tw-gradient-to: rgb(126 34 206); }
""")
    click.echo("  Created: styles.css")

    # Create tailwind.config.js with PSX support
    (project_dir / "tailwind.config.js").write_text(
        """ /** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    // Framework templates and components
    "./pages/**/*.{py,jsx,html}",
    "./components/**/*.{py,jsx,html}",
    "./templates/**/*.{html,htm}",
    "./public/**/*.html",

    // Also scan from project root (two level up)
    "../../templates/**/*.{html,htm}",
    "../../pages/**/*.{py,jsx,html}",
    "../../components/**/*.{py,jsx,html}",
  ],
  // Force include common Tailwind classes
  safelist: [
    // Background colors
    'bg-blue-50', 'bg-blue-100', 'bg-blue-200', 'bg-blue-300', 'bg-blue-400', 'bg-blue-500', 'bg-blue-600', 'bg-blue-700',
    'bg-red-50', 'bg-red-100', 'bg-red-200', 'bg-red-300', 'bg-red-400', 'bg-red-500', 'bg-red-600', 'bg-red-700',
    'bg-green-50', 'bg-green-100', 'bg-green-200', 'bg-green-300', 'bg-green-400', 'bg-green-500', 'bg-green-600', 'bg-green-700',
    'bg-purple-50', 'bg-purple-100', 'bg-purple-200', 'bg-purple-300', 'bg-purple-400', 'bg-purple-500', 'bg-purple-600', 'bg-purple-700',
    'bg-gray-50', 'bg-gray-100', 'bg-gray-200', 'bg-gray-300', 'bg-gray-400', 'bg-gray-500', 'bg-gray-600', 'bg-gray-700', 'bg-gray-800', 'bg-gray-900',
    'bg-white', 'bg-black',

    // Text colors
    'text-blue-50', 'text-blue-100', 'text-blue-200', 'text-blue-300', 'text-blue-400', 'text-blue-500', 'text-blue-600', 'text-blue-700',
    'text-red-50', 'text-red-100', 'text-red-200', 'text-red-300', 'text-red-400', 'text-red-500', 'text-red-600', 'text-red-700',
    'text-green-50', 'text-green-100', 'text-green-200', 'text-green-300', 'text-green-400', 'text-green-500', 'text-green-600', 'text-green-700',
    'text-purple-50', 'text-purple-100', 'text-purple-200', 'text-purple-300', 'text-purple-400', 'text-purple-500', 'text-purple-600', 'text-purple-700',
    'text-gray-50', 'text-gray-100', 'text-gray-200', 'text-gray-300', 'text-gray-400', 'text-gray-500', 'text-gray-600', 'text-gray-700', 'text-gray-800', 'text-gray-900',
    'text-white', 'text-black',

    // Shadows
    'shadow-sm', 'shadow', 'shadow-md', 'shadow-lg', 'shadow-xl', 'shadow-2xl',

    // Gradients
    'bg-gradient-to-r', 'bg-gradient-to-br', 'bg-gradient-to-b', 'bg-gradient-to-bl', 'bg-gradient-to-l', 'bg-gradient-to-tl', 'bg-gradient-to-t', 'bg-gradient-to-tr',
    'from-blue-50', 'from-blue-100', 'from-blue-200', 'from-blue-300', 'from-blue-400', 'from-blue-500', 'from-blue-600', 'from-blue-700',
    'via-indigo-50', 'via-indigo-100', 'via-indigo-200', 'via-indigo-300', 'via-indigo-400', 'via-indigo-500', 'via-indigo-600', 'via-indigo-700',
    'to-purple-50', 'to-purple-100', 'to-purple-200', 'to-purple-300', 'to-purple-400', 'to-purple-500', 'to-purple-600', 'to-purple-700',

    // Spacing and layout
    'p-4', 'p-6', 'p-8', 'px-4', 'px-6', 'px-8', 'py-2', 'py-4', 'py-6', 'py-8', 'py-12', 'py-16', 'py-20', 'py-24',
    'm-4', 'm-6', 'm-8', 'mx-4', 'mx-6', 'mx-8', 'my-2', 'my-4', 'my-6', 'my-8', 'my-12', 'my-16', 'my-20', 'my-24',
    'mb-2', 'mb-4', 'mb-6', 'mb-8', 'mb-12', 'mb-16', 'mb-20', 'mb-24',
    'mt-2', 'mt-4', 'mt-6', 'mt-8', 'mt-12', 'mt-16', 'mt-20', 'mt-24',

    // Borders and rounded
    'border', 'border-2', 'border-l-4', 'border-t-4', 'rounded', 'rounded-lg', 'rounded-xl', 'rounded-full',

    // Flexbox and grid
    'flex', 'flex-col', 'flex-row', 'items-center', 'justify-center', 'justify-between', 'grid', 'grid-cols-2', 'grid-cols-3', 'grid-cols-4', 'gap-4', 'gap-6', 'gap-8',

    // Width and height
    'w-full', 'w-1/2', 'w-1/3', 'w-1/4', 'h-full', 'h-screen', 'max-w-md', 'max-w-lg', 'max-w-xl', 'max-w-4xl', 'max-w-6xl', 'max-w-7xl',

    // Typography
    'text-xs', 'text-sm', 'text-base', 'text-lg', 'text-xl', 'text-2xl', 'text-3xl', 'text-4xl', 'text-5xl', 'text-6xl', 'text-7xl',
    'font-light', 'font-normal', 'font-medium', 'font-semibold', 'font-bold',
    'leading-tight', 'leading-relaxed', 'leading-loose',
    'text-center', 'text-left', 'text-right',

    // Hover states
    'hover:bg-blue-600', 'hover:bg-blue-700', 'hover:bg-purple-600', 'hover:bg-purple-700', 'hover:bg-green-600', 'hover:bg-green-700',
    'hover:text-white', 'hover:text-blue-600', 'hover:text-purple-600', 'hover:text-green-600',
    'hover:shadow-lg', 'hover:shadow-xl', 'hover:scale-105', 'hover:translate-x-1',

    // Transitions
    'transition', 'transition-all', 'transition-colors', 'transition-transform',

    // Opacity and visibility
    'opacity-0', 'opacity-50', 'opacity-100', 'invisible', 'visible',

    // Z-index
    'z-10', 'z-20', 'z-30', 'z-40', 'z-50',

    // Positioning
    'relative', 'absolute', 'fixed', 'sticky', 'top-0', 'bottom-0', 'left-0', 'right-0'
  ],
  plugins: [],
}; """
    )
    click.echo("  Created: tailwind.config.js")

    # Create package.json with Node.js dependencies
    (project_dir / "package.json").write_text("""{
 "name": "nextpy-framework",
  "version": "1.0.0",
  "description": "A Python web framework. Build modern web applications with file-based routing, server-side rendering (SSR), static site generation (SSG), and more.",
  "main": "index.js",
  "directories": {
    "doc": "docs",
    "test": "tests"
  },
  "scripts": {
    "test": "pytest -q",
    "build:tailwind": "npx tailwindcss -i ./styles/styles.css -o ./public/tailwind.css --minify",
    "ci:tailwind": "npm ci && npm run build:tailwind"
  },
  "keywords": [],
  "author": "",
  "license": "ISC",
  "devDependencies": {
    "@tailwindcss/cli": "^4.2.1",
    "autoprefixer": "^10.4.22",
    "postcss": "^8.5.6",
    "tailwindcss": "^4.2.1"
  },
  "dependencies": {
    "@tailwindcss/postcss": "^4.2.1",
    "postcss-cli": "^11.0.1"
  }
}
""")
    click.echo("  Created: package.json")

    # Create PSX homepage if enabled
    if psx:
        _create_psx_homepage(project_dir)
        _create_psx_about_page(project_dir)
        _create_psx_examples(project_dir)
        _create_vscode_settings(project_dir)
    else:
        _create_traditional_homepage(project_dir)

    (project_dir / "pages" / "layout.psx").write_text('''
from nextpy.psx import component
"""App Layout"""
@component
def Layout(children, **props):
    return (
        <html>
            <head>
                <title>{{props.get('title', 'My App')</title>
                
                <link href="/tailwind.css" rel="stylesheet">
            </head>
            <body>
                {children}  
            </body>
        </html>
    )

    ''')
    click.echo("  Created: pages/layout.psx ")

    (project_dir / "pages" / "index.psx").write_text('''
"""Interactive Homepage """

from nextpy.psx import interactive_component as component


@component
def Home(props=None):
    props = props or {}
    title = props.get("title", "Welcome to NextPy!")
    message = props.get("message", "Build amazing web apps with Python and True JSX")

    return (
        <div class="flex flex-col items-center justify-between min-h-screen p-8 font-sans antialiased text-black bg-white selection:bg-gray-200">
            <head>
            {/* optionally load a stylesheet from public/css <link rel="stylesheet" href="static/css/styles.css" /> */}
            </head>
            {/* Top spacer to perfectly center the main content vertically */}
            <div class=""></div>

            {/* Main Centered Content */}
            <div class="flex flex-col items-center max-w-xl gap-8 text-center">
                {/* Logo Section */}
                <h1 class="text-[56px] font-extrabold tracking-tighter leading-none select-none font-mono flex items-baseline">
                    <img src="static/images/logo.png" alt="NextPy Logo" class="w-auto h-16" />

                </h1>

                {/* Step-by-Step Instructions */}
                <ol class="list-decimal list-inside text-left text-[16px] font-mono text-gray-800 space-y-2.5">
                    <li>
                        Get started by editing
                        <code class="bg-black/[0.05] px-1.5 py-0.5 rounded font-bold text-black text-[13px]">
                            pages/index.py
                        </code>
                        .
                    </li>
                    <li>Save and see your changes instantly.</li>
                </ol>

                {/* Call To Action Buttons */}
                <div class="flex flex-col items-center gap-4 mt-2 sm:flex-row">
                
                    <a
                        href="https://nextpy-framework.onrender.com/deploy"
                        class="flex items-center gap-2 bg-black text-white px-6 py-3 rounded-full text-[14px] font-medium transition-colors hover:bg-[#2c2c2c] shadow-sm"
                        
                    >
                        <svg
                            class="w-6 h-6"
                            fill="none"
                            stroke="currentColor"
                            stroke-width="2"
                            viewBox="0 0 24 24"
                        >
                            <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                d="M7 18a4 4 0 010-8 5 5 0 019.7-1.2A3.5 3.5 0 0117.5 18H7z"
                            />
                            <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                d="M12 14V8m0 0l-3 3m3-3l3 3"
                            />
                        </svg>
                        
                        Deploy now
                    </a>
                    
                    <a
                        href="https://nextpy-framework.onrender.com/"
                        class="flex items-center justify-center border border-black/[0.08] bg-white text-black px-6 py-3 rounded-full text-[14px] font-medium transition-colors hover:bg-gray-50 hover:border-black/[0.15] min-w-[140px]"
                        
                    >
                        Read our docs
                    </a>
                </div>
                
                <div class="flex flex-wrap items-center justify-center gap-x-8 text-[14px] font-medium text-gray-600 w-full max-w-2xl py-4 border-t border-gray-100 sm:border-none">
                    <a
                    href="https://nextpy-framework.onrender.com/learn"
                    class="flex items-center gap-2 transition-colors hover:underline hover:text-black"
                    
                >
                    {/* Document Icon */}
                    <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                    </svg>
                    Learn
                </a>

                <a
                    href="https://nextpy-framework.onrender.com/templates"
                    class="flex items-center gap-2 transition-colors hover:underline hover:text-black"
                    
                >
                    {/* Window Layout Icon */}
                    <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5zm0 7a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H5a1 1 0 01-1-1v-6zm10 0a1 1 0 011-1h4a1 1 0 011 1v6a1 1 0 01-1 1h-4a1 1 0 01-1-1v-6z"/>
                    </svg>
                    Examples
                </a>

                <a
                    href="https://nextpy-framework.onrender.com/"
                    class="flex items-center gap-1.5 hover:underline hover:text-black transition-colors"
                    
                >
                    {/* Globe Icon */}
                    <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9"/>
                    </svg>
                    Go to nextpy.org →
                </a>
                </div>

            </div>
            
            <footer class="flex flex-wrap items-center justify-center text-[14px] font-medium text-gray-600 w-full max-w-2xl py-4 border-t border-gray-100 sm:border-none">
               The Python Web Framework for Everyone
            </footer>
        </div>
    )


def getServerSideProps(context):
    return {
        "props": {
            "title": "Welcome to NextPy!",
            "message": "Build amazing web apps with Python and True JSX"
        }
    }


default = Home


''')
    click.echo("  Created: pages/index.psx ")


    (project_dir / "components" / "ui" / "Button.psx").write_text(
        '''
"""Button component"""
from nextpy.psx import psx



def Button(props = None):
    """Reusable Button component"""
    props = props or {}
    
    variant = props.get("variant", "default")
    children = props.get("children", "Button")
    className = props.get("className", "")
    
    if variant == "primary":
        variant_class = "bg-blue-600 text-white hover:bg-blue-700 transform hover:scale-105 transition-all duration-200"
    elif variant == "secondary":
        variant_class = "bg-gray-200 text-gray-900 hover:bg-gray-300 transform hover:scale-105 transition-all duration-200"
    elif variant == "success":
        variant_class = "bg-green-600 text-white hover:bg-green-700 transform hover:scale-105 transition-all duration-200"
    elif variant == "danger":
        variant_class = "bg-red-600 text-white hover:bg-red-700 transform hover:scale-105 transition-all duration-200"
    else:
        variant_class = "bg-gray-600 text-white hover:bg-gray-700 transform hover:scale-105 transition-all duration-200"
    
    class_attr = f"px-6 py-3 rounded-lg font-medium transition-all duration-200 transform hover:scale-105 {variant_class} {className}"
    
    return psx(f"
        <button class={class_attr} 
                id={props.get("id")}
                disabled={props.get("disabled", False)}
                onclick={props.get("onClick", "")}>
            {children}
        </button>
    ")

default = Button
'''
    )
    click.echo("  Created: components/ui/Button.psx(enhanced interactive)")
    
    # Create comprehensive API examples
    (project_dir / "pages" / "api" / "hello.psx").write_text(
        '''
"""API example - Hello endpoint"""

from fastapi import Request

async def get(request: Request):
    """GET /api/hello"""
    return {"message": "Hello from NextPy API!", "status": "success"}

async def post(request: Request):
    """POST /api/hello"""
    data = await request.json()
    return {"message": "POST request received", "data": data, "status": "success"}
'''
    )
    click.echo("  Created: pages/api/hello.psx")

    (project_dir / "pages" / "api" / "users" / "index.py").write_text(
        '''"""API example - Users index"""

from fastapi import Request

async def get(request: Request):
    """GET /api/users - List all users"""
    users = [
        {"id": 1, "name": "John Doe", "email": "john@example.com"},
        {"id": 2, "name": "Jane Smith", "email": "jane@example.com"},
    ]
    return {"users": users, "total": len(users)}

async def post(request: Request):
    """POST /api/users - Create new user"""
    data = await request.json()
    # In a real app, you'd save to database
    new_user = {
        "id": 3,
        "name": data.get("name"),
        "email": data.get("email")
    }
    return {"user": new_user, "message": "User created successfully"}
'''
    )
    click.echo("  Created: pages/api/users/index.py")

    (project_dir / "pages" / "api" / "users" / "[id].py").write_text(
        '''
"""API example - Dynamic user route"""

from fastapi import Request

async def get(request: Request, id: int):
    """GET /api/users/{id} - Get user by ID"""
    users = {
        1: {"id": 1, "name": "John Doe", "email": "john@example.com"},
        2: {"id": 2, "name": "Jane Smith", "email": "jane@example.com"},
    }
    
    if id in users:
        return {"user": users[id]}
    else:
        return {"error": "User not found"}, 404

async def put(request: Request, id: int):
    """PUT /api/users/{id} - Update user"""
    data = await request.json()
    return {"message": f"User {id} updated", "data": data}

async def delete(request: Request, id: int):
    """DELETE /api/users/{id} - Delete user"""
    return {"message": f"User {id} deleted successfully"}
'''
    )
    click.echo("  Created: pages/api/users/[id].py")

    # Create database models
    (project_dir / "models" / "User.py").write_text('''"""User model example"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}')>"
''')
    click.echo("  Created: models/User.py")

    # Blog listing page
    (project_dir / "pages" / "blog" / "index.py").write_text('''
"""Blog listing page"""

from nextpy.psx import component

@component
def BlogIndex(props=None):
    props = props or {}
    posts = props.get("posts", [])

    return (
        <div class="min-h-screen bg-gradient-to-br from-slate-50 to-indigo-50/30">
            {/* Hero Section */}
            <div class="relative overflow-hidden bg-white shadow-sm">
                <div class="absolute inset-0 bg-gradient-to-r from-indigo-500/10 to-purple-500/10"></div>
                <div class="relative max-w-6xl px-4 py-16 mx-auto text-center sm:py-24 sm:px-6 lg:px-8">
                    <h1 class="text-5xl font-extrabold tracking-tight text-gray-900 sm:text-6xl">
                        <span class="text-transparent bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text">
                            Our Blog
                        </span>
                    </h1>
                    <p class="max-w-2xl mx-auto mt-4 text-xl text-gray-600">
                        Stories, insights, and updates from the team
                    </p>
                </div>
            </div>

            {/* Posts Grid */}
            <div class="max-w-6xl px-4 py-12 mx-auto sm:px-6 lg:px-8">
                <div class="grid gap-8 sm:grid-cols-2 lg:grid-cols-3">
                    {if len(posts) > 0:
                        {for post in posts:
                            <article class="relative flex flex-col overflow-hidden transition-all duration-300 bg-white shadow-md group rounded-2xl hover:shadow-2xl hover:-translate-y-1">
                                {/* Card Image Placeholder */}
                                <div class="relative h-48 overflow-hidden bg-gradient-to-br from-indigo-200 to-purple-200">
                                    <div class="absolute inset-0 flex items-center justify-center text-4xl text-indigo-400/50">
                                        📖
                                    </div>
                                    <div class="absolute bottom-0 left-0 right-0 h-12 bg-gradient-to-t from-white/80 to-transparent"></div>
                                </div>

                                <div class="flex flex-col flex-1 p-6">
                                    <h2 class="text-xl font-bold text-gray-900 line-clamp-2">
                                        <a href="blog/{post['slug']}" class="transition-colors rounded hover:text-indigo-600 focus:outline-none focus:ring-2 focus:ring-indigo-500">
                                            {post["title"]}
                                        </a>
                                    </h2>
                                    <p class="mt-2 text-sm text-gray-600 line-clamp-3">{post["excerpt"]}</p>

                                    <div class="flex items-center justify-between mt-4 text-xs text-gray-500">
                                        <div class="flex items-center space-x-2">
                                            <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800">
                                                Article
                                            </span>
                                            <span>·</span>
                                            <span>{post["date"]}</span>
                                        </div>
                                        <span class="font-medium text-gray-700">{post["author"]}</span>
                                    </div>

                                    <div class="mt-4">
                                        <a href="blog/{post['slug']}" class="inline-flex items-center text-sm font-semibold text-indigo-600 transition-colors hover:text-indigo-800 group-hover:underline">
                                            Read more
                                            <svg class="w-4 h-4 ml-1 transition-transform group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
                                            </svg>
                                        </a>
                                    </div>
                                </div>
                            </article>
                        }
                    {else:
                        <div class="py-20 text-center col-span-full">
                            <div class="mb-4 text-6xl">📭</div>
                            <p class="text-xl text-gray-600">No posts yet. Check back soon!</p>
                            <p class="text-sm text-gray-400">We're cooking up something great.</p>
                        </div>
                    }
                </div>
            </div>
        </div>
    )

def getServerSideProps(context):
    posts = [
        {
            "slug": "hello-world",
            "title": "Hello World",
            "excerpt": "Welcome to our blog built with NextPy! This is a modern way to build web apps with Python.",
            "date": "2025-01-15",
            "author": "Team NextPy",
        },
        {
            "slug": "why-python-web",
            "title": "Why Python for Web Apps",
            "excerpt": "Discover how Python is changing front-end development and why you should care.",
            "date": "2025-02-20",
            "author": "Jane Doe",
        },
    ]
    return {"props": {"posts": posts}}

default = BlogIndex
    ''')
    click.echo("  Created: pages/blog/index.py")

    # Blog post dynamic route
    (project_dir / "pages" / "blog" / "[slug].py").write_text('''
    """Dynamic blog post page – accessed via /blog/{slug}"""

from nextpy.psx import interactive_component

@interactive_component
def BlogPost(props):
    props = props or {}
    post = props.get("post", {})

    if not post:
        return (
            <div class="flex items-center justify-center min-h-screen bg-gray-50">
                <div class="text-center">
                    <h1 class="mb-4 text-4xl font-bold text-gray-900">Post Not Found</h1>
                    <a href="/blog" class="text-blue-600 hover:underline">← Back to blog</a>
                </div>
            </div>
        )

    return (
        <div class="min-h-screen bg-white">
            <article class="max-w-3xl px-4 py-16 mx-auto sm:px-6 lg:px-8">
                <header class="mb-10">
                    <h1 class="text-5xl font-extrabold leading-tight text-gray-900">
                        {post["title"]}
                    </h1>
                    <div class="flex items-center mt-4 text-lg text-gray-500">
                        <span>{post["date"]}</span>
                        <span class="mx-2">·</span>
                        <span>{post["author"]}</span>
                    </div>
                </header>
                <div class="prose prose-lg text-gray-800 max-w-none">
                    {post["content"]}
                </div>
                <div class="pt-8 mt-12 border-t">
                    <a href="/blog" class="font-medium text-blue-600 transition-colors hover:text-blue-800">
                        ← Back to all posts
                    </a>
                </div>
            </article>
        </div>
    )

def getServerSideProps(context):
    slug = context.get("params", {}).get("slug", "")

    posts = {
        "hello-world": {
            "slug": "hello-world",
            "title": "Hello World",
            "date": "2025-01-15",
            "author": "Team NextPy",
            "content": "This is the full content of the Hello World post.",
        },
        "why-python-web": {
            "slug": "why-python-web",
            "title": "Why Python for Web Apps",
            "date": "2025-02-20",
            "author": "Jane Doe",
            "content": "Python has evolved far beyond scripting.",
        },
    }

    post = posts.get(slug, {})
    return {"props": {"post": post}}

default = BlogPost

    ''')
    click.echo("  Created: pages/blog/[slug].py")

    # Create utility functions
    (project_dir / "utils" / "helpers.py").write_text('''"""Utility helper functions"""

import hashlib
import secrets
from datetime import datetime

def generate_secret_key(length: int = 32) -> str:
    """Generate a secure secret key"""
    return secrets.token_urlsafe(length)

def hash_password(password: str) -> str:
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def format_date(date: datetime) -> str:
    """Format datetime for display"""
    return date.strftime("%B %d, %Y at %I:%M %p")

def slugify(text: str) -> str:
    """Convert text to URL-friendly slug"""
    return text.lower().replace(" ", "-").replace("_", "-")
''')
    click.echo("  Created: utils/helpers.py")

    # Create custom hooks
    (project_dir / "hooks" / "use_auth.py").write_text(
        '''"""Authentication hook example"""

def use_auth(request):
    """Example authentication hook"""
    # In a real app, you'd check tokens, sessions, etc.
    auth_header = request.headers.get("authorization")
    
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        # Validate token here
        return {"user": {"id": 1, "name": "Authenticated User"}, "token": token}
    
    return {"user": None, "error": "No authentication provided"}
'''
    )
    click.echo("  Created: hooks/use_auth.py")

    # Create middleware example
    (project_dir / "middleware" / "cors.py").write_text('''"""CORS middleware example"""

from fastapi import Request, Response
from fastapi.middleware.cors import CORSMiddleware

def add_cors_middleware(app):
    """Add CORS middleware to the app"""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app
''')
    click.echo("  Created: middleware/cors.py")

    # Create test files
    (project_dir / "tests" / "test_api.py").write_text('''"""API tests example"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_hello_api():
    """Test the hello API endpoint"""
    response = client.get("/api/hello")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Hello from NextPy API!"
    assert data["status"] == "success"

def test_users_api():
    """Test the users API endpoint"""
    response = client.get("/api/users")
    assert response.status_code == 200
    data = response.json()
    assert "users" in data
    assert "total" in data
    assert len(data["users"]) == data["total"]
''')
    click.echo("  Created: tests/test_api.py")

    # Create documentation
    (project_dir / "docs" / "README.md").write_text("""# Project Documentation

## Overview
This is a NextPy application with True PSX, Tailwind CSS, and comprehensive API support.

## Features
- ✅ True PSX components
- ✅ Tailwind CSS integration
- ✅ File-based routing
- ✅ API routes with FastAPI
- ✅ Database models with SQLAlchemy
- ✅ Authentication hooks
- ✅ CORS middleware
- ✅ Comprehensive testing

## Project Structure
```
|-- pages/           # File-based routing
|   |-- api/        # API routes
|   `-- *.py        # Page components
|-- components/      # Reusable components
|-- templates/       # HTML templates
|-- models/         # Database models
|-- utils/          # Utility functions
|-- hooks/          # Custom hooks
|-- middleware/     # Custom middleware
|-- tests/          # Test files
|-- public/         # Static assets
|-- styles/         # CSS files
`-- docs/           # Documentation
```

## Getting Started
1. Install dependencies: `pip install -r requirements.txt`
2. Install Node.js deps: `npm install`
3. Run development server: `nextpy dev`
4. Open http://localhost:8000

The framework now adds a set of security headers by default (CSP, X-Frame-Options, etc.) for safer deployments.
* You can request automatic Tailwind CSS compilation on startup by setting the
  `NEXTPY_AUTO_BUILD_TAILWIND=true` environment variable. This requires `npm`
  to be installed and will run `npm ci` followed by `npm run build:tailwind`.
* SQLAlchemy imports have been updated to avoid 2.0 deprecation warnings.
  If you see such warnings upgrade your dependencies or pin the versions as
  needed.

## API Endpoints
- `GET /api/hello` - Hello message
- `GET /api/users` - List users
- `POST /api/users` - Create user
- `GET /api/users/{id}` - Get user by ID
- `PUT /api/users/{id}` - Update user
- `DELETE /api/users/{id}` - Delete user
""")
    click.echo("  Created: docs/README.md")

    (project_dir / "requirements.txt").write_text("""fastapi>=0.100.0
nextpy-framework>=2.5.0
uvicorn[standard]>=0.24.0
fastapi>=0.104.0
pydantic>=2.0.0
jinja2>=3.1.0
watchdog>=2.3.0
click>=8.1.0
python-multipart>=0.0.6
aiofiles>=23.0.0

# PSX Language Server Dependencies (optional)
pygls>=0.12.0
lsprotocol>=2023.0.0

# Development Dependencies
pytest>=7.0.0
pytest-asyncio>=0.21.0
black>=23.0.0
""")
    click.echo("  Created: requirements.txt")
    
    # Create favicon
    (project_dir / "public" / "favicon.ico").write_bytes(b'\x00\x00\x01\x00\x01\x00\x10\x10\x00\x00\x01\x00\x08\x00h\x00\x00\x00\x16\x00\x00\x00')
    click.echo("  Created: public/favicon.ico")
    
     # Create .gitignore
    (project_dir / ".gitignore").write_text('''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
env.bak/
venv.bak/

# NextPy
.nextpy/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/
pip-log.txt
pip-delete-this-directory.txt
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/

# Node
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Build outputs
out/
build/
dist/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db
''')
    click.echo("  Created: .gitignore")


    # Create .env file for development
    (project_dir / ".env").write_text("""# NextPy Development Environment
DEVELOPMENT=true
DEBUG=true
NEXTPY_DEBUG=true

# Server Configuration
HOST=0.0.0.0
PORT=8000

# Database (if needed)
DATABASE_URL=sqlite:///./app.db

# Secret Key
SECRET_KEY=your-secret-key-here

# NextPy Settings
NEXTPY_DEBUG_ICON=true
NEXTPY_HOT_RELOAD=true
NEXTPY_LOG_LEVEL=info
""")
    click.echo("  Created: .env")

    # Install Node.js dependencies
    try:
        import subprocess
        import sys

        click.echo(click.style("  📦 Installing Node.js dependencies...", fg="blue"))
        result = subprocess.run(
            ["npm", "install"], cwd=project_dir, capture_output=True, text=True
        )

        if result.returncode == 0:
            click.echo(click.style("  ✅ Node.js dependencies installed", fg="green"))
        else:
            click.echo(click.style("  ⚠️  npm install failed", fg="yellow"))
            click.echo("  💡 Run manually: npm install")

    except FileNotFoundError:
        click.echo(click.style("  ⚠️  npm not found", fg="yellow"))
        click.echo("  💡 Install Node.js: https://nodejs.org/")
    except Exception as e:
        click.echo(
            click.style(f"  ⚠️  Could not install Node.js deps: {e}", fg="yellow")
        )

    # Install Python dependencies
    try:
        click.echo(click.style("  🐍 Installing Python dependencies...", fg="blue"))
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            cwd=project_dir,
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            click.echo(click.style("  ✅ Python dependencies installed", fg="green"))
        else:
            click.echo(click.style("  ⚠️  pip install failed", fg="yellow"))
            click.echo("  💡 Run manually: pip install -r requirements.txt")

    except Exception as e:
        click.echo(
            click.style(f"  ⚠️  Could not install Python deps: {e}", fg="yellow")
        )
    try:
        import sys
        import subprocess
        from pathlib import Path

        # Check if VS Code is available
        result = subprocess.run(
            [sys.executable, "-c", "import vscode"], capture_output=True, text=True
        )

        if result.returncode == 0:
            extension_id = "nextpy.nextpy-vscode"

            # Check if extension is already installed
            check_cmd = ["code", "--list-extensions", "--show-versions", extension_id]
            check_result = subprocess.run(check_cmd, capture_output=True, text=True)

            if extension_id not in check_result.stdout:
                click.echo(
                    click.style(
                        "  🔌 Installing NextPy VS Code extension...", fg="blue"
                    )
                )

                # Try to install from marketplace
                install_cmd = ["code", "--install-extension", extension_id]
                install_result = subprocess.run(
                    install_cmd, capture_output=True, text=True
                )

                if install_result.returncode == 0:
                    click.echo(
                        click.style(
                            "  ✅ NextPy VS Code extension installed!", fg="green"
                        )
                    )
                    click.echo(
                        click.style("  📝 Restart VS Code to activate", fg="yellow")
                    )
                else:
                    click.echo(
                        click.style("  ⚠️  Extension installation failed", fg="yellow")
                    )
                    click.echo(
                        "  💡 Install manually: code --install-extension nextpy.nextpy-vscode"
                    )
            else:
                click.echo(
                    click.style(
                        "  ✅ NextPy VS Code extension already installed", fg="green"
                    )
                )
        else:
            click.echo(click.style("  ⚠️  VS Code not available", fg="yellow"))
    except Exception as e:
        click.echo(
            click.style(f"  ⚠️  Could not install VS Code extension: {e}", fg="yellow")
        )


def _create_psx_homepage(project_dir: Path):
    """Create PSX homepage with True JSX syntax"""
    (project_dir / "pages" / "index.py").write_text('''"""
NextPy PSX Homepage - True JSX in Python
All PSX utilities, hooks, and components are auto-imported
"""

from nextpy import component, psx

@component
def Home(props=None):
    props = props or {}
    title = props.get("title", "Welcome to NextPy")
    message = props.get("message", "Your Python-powered web framework with True JSX")
    
    return (
        <div class="flex items-center justify-center min-h-screen bg-gradient-to-br from-blue-500 to-purple-600">
            <div class="text-center text-white">
                <h1 class="mb-4 text-5xl font-bold">{title}</h1>
                <p class="text-xl">{message}</p>
                <a href="/about" class="inline-block px-6 py-3 mt-8 font-semibold text-blue-600 transition-all duration-300 transform bg-white rounded-lg shadow-lg hover:bg-gray-100 hover:text-blue-700 hover:scale-105">
                    Learn More
                </a>
            </div>
        </div>
    )

def getServerSideProps(context):
    return {
        "props": {
            "title": "Welcome to NextPy",
            "message": "Your Python-powered web framework with True JSX"
        }
    }

default = Home
''')
    click.echo("  Created: pages/index.py (PSX homepage)")

    # Create sample components
    (project_dir / "components" / "Button.py").write_text('''"""
Button Component - Reusable PSX button component
All PSX utilities, hooks, and components are auto-imported
"""

from nextpy import component, clsx

@component
def Button(props=None):
    """Reusable button component with variants"""
    props = props or {}
    variant = props.get("variant", "primary")
    size = props.get("size", "md")
    children = props.get("children", "Button")
    
    # Base classes
    base_classes = "font-semibold rounded-lg transition-colors"
    
    # Size classes
    size_classes = {
        "sm": "px-3 py-1.5 text-sm",
        "md": "px-4 py-2 text-base",
        "lg": "px-6 py-3 text-lg"
    }.get(size, "px-4 py-2 text-base")
    
    # Variant classes
    variant_classes = {
        "primary": "bg-blue-500 hover:bg-blue-600 text-white",
        "secondary": "bg-gray-200 hover:bg-gray-300 text-gray-800",
        "success": "bg-green-500 hover:bg-green-600 text-white",
        "danger": "bg-red-500 hover:bg-red-600 text-white"
    }.get(variant, "bg-blue-500 hover:bg-blue-600 text-white")
    
    return (
        <button class={f"{base_classes} {size_classes} {variant_classes}"}>
            {children}
        </button>
    )
''')
    click.echo("  Created: components/Button.py")

    (project_dir / "components" / "Card.py").write_text('''"""
Card Component - Reusable PSX card component
"""

from nextpy.psx import component

@component
def Card(props=None):
    """Reusable card component"""
    props = props or {}
    title = props.get("title", "Card Title")
    description = props.get("description", "Card description")
    children = props.get("children", None)
    
    return (
        <div class="max-w-md p-6 bg-white rounded-lg shadow-lg">
            <h3 class="mb-2 text-xl font-semibold">{title}</h3>
            <p class="mb-4 text-gray-600">{description}</p>
            {children if children else ""}
        </div>
    )
''')
    click.echo("  Created: components/Card.py")


def _create_psx_about_page(project_dir: Path):
    """Create PSX about page"""
    (project_dir / "pages" / "about.py").write_text('''"""
NextPy PSX About Page - Demonstrating advanced PSX features
All PSX utilities, hooks, and components are auto-imported
"""

from nextpy import component, psx, clsx

@component
def About(props=None):
    """About page with advanced PSX features"""
    props = props or {}
    title = props.get("title", "About NextPy")
    description = props.get("description", "Revolutionary Python web framework")
    
    return (
        <div class="min-h-screen bg-gray-50">
            <div class="container px-4 py-16 mx-auto">
                <div class="max-w-4xl mx-auto">
                    <div class="mb-12 text-center">
                        <h1 class="mb-4 text-4xl font-bold text-gray-900">{title}</h1>
                        <p class="text-xl text-gray-600">{description}</p>
                    </div>
                    
                    <div class="grid gap-8 mb-12 md:grid-cols-2">
                        {for section in [
                            {
                                "title": "True JSX Syntax",
                                "content": "Write exact JSX syntax in Python with no compilation step needed",
                                "code": "@component\\ndef Component():\\n    return (<div>Hello JSX</div>)"
                            },
                            {
                                "title": "Python Logic in JSX",
                                "content": "Use real Python for loops, if conditions, and try-catch in your JSX",
                                "code": "{for item in items:\\n    <div>{item}</div>}"
                            },
                            {
                                "title": "Virtual DOM",
                                "content": "Optimized rendering with diffing and patching for maximum performance",
                                "code": "vnode = create_element('div', {}, children)"
                            },
                            {
                                "title": "Server-Side Rendering",
                                "content": "Full SSR support with getServerSideProps and getStaticProps",
                                "code": "def getServerSideProps(context):\\n    return {\"props\": data}"
                            }
                        ]:
                            <div class="p-6 bg-white rounded-lg shadow-lg">
                                <h3 class="mb-2 text-xl font-semibold">{section["title"]}</h3>
                                <p class="mb-4 text-gray-600">{section["content"]}</p>
                                <pre class="p-3 overflow-x-auto text-sm text-green-400 bg-gray-900 rounded">
                                    {section["code"]}
                                </pre>
                            </div>
                        }
                    </div>
                    
                    <div class="text-center">
                        <a href="/" class="inline-block px-8 py-3 font-semibold text-white transition-colors bg-blue-600 rounded-lg shadow-lg hover:bg-blue-700">
                            Back to Home
                        </a>
                    </div>
                </div>
            </div>
        </div>
    )

def getServerSideProps(context):
    """Server-side props for about page"""
    return {
        "props": {
            "title": "About NextPy",
            "description": "Revolutionary Python web framework with True JSX"
        }
    }

default = About
''')
    click.echo("  Created: pages/about.py (PSX about page)")


def _create_psx_examples(project_dir: Path):
    """Create PSX examples page"""
    (project_dir / "pages" / "examples.py").write_text('''"""
NextPy PSX Examples - Showcasing all PSX features
All PSX utilities, hooks, and components are auto-imported
"""

from nextpy import component, psx, useState, useEffect

@component
def Examples(props=None):
    """Examples page demonstrating PSX features"""
    return (
        <div class="min-h-screen py-8 bg-gray-50">
            <div class="container px-4 mx-auto">
                <div class="max-w-6xl mx-auto">
                    <h1 class="mb-12 text-4xl font-bold text-center">PSX Examples</h1>
                    
                    {/* Python Logic Examples */}
                    <section class="mb-12">
                        <h2 class="mb-6 text-2xl font-semibold">Python Logic in JSX</h2>
                        
                        <div class="grid gap-6 md:grid-cols-2">
                            <div class="p-6 bg-white rounded-lg shadow">
                                <h3 class="mb-3 font-semibold">For Loop</h3>
                                <div class="space-y-2">
                                    {for i in range(3):
                                        <div class="p-3 bg-blue-100 rounded">
                                            Item {i + 1}
                                        </div>
                                    }
                                </div>
                            </div>
                            
                            <div class="p-6 bg-white rounded-lg shadow">
                                <h3 class="mb-3 font-semibold">Conditional Rendering</h3>
                                {True:
                                    <div class="p-3 bg-green-100 rounded">
                                        This is shown when condition is true
                                    </div>
                                }
                            </div>
                        </div>
                    </section>
                    
                    {/* Component Examples */}
                    <section class="mb-12">
                        <h2 class="mb-6 text-2xl font-semibold">Component Examples</h2>
                        
                        <div class="grid gap-6 md:grid-cols-3">
                            {for card in [
                                {"title": "Card 1", "color": "blue"},
                                {"title": "Card 2", "color": "green"},
                                {"title": "Card 3", "color": "purple"}
                            ]:
                                <div class="p-6 transition-shadow bg-white rounded-lg shadow hover:shadow-lg">
                                    <div class={"w-full h-32 bg-" + card["color"] + "-200 rounded mb-4"}></div>
                                    <h3 class="font-semibold">{card["title"]}</h3>
                                </div>
                            }
                        </div>
                    </section>
                    
                    <div class="text-center">
                        <a href="/" class="inline-block px-8 py-3 font-semibold text-white transition-colors bg-blue-600 rounded-lg shadow-lg hover:bg-blue-700">
                            Back to Home
                        </a>
                    </div>
                </div>
            </div>
        </div>
    )

default = Examples
''')
    click.echo("  Created: pages/examples.py (PSX examples)")


def _create_vscode_settings(project_dir: Path):
    """Create VS Code settings for PSX development"""
    (project_dir / ".vscode").mkdir(exist_ok=True)
    (project_dir / ".vscode" / "settings.json").write_text("""{
  "files.associations": {
    "*.psx": "nextpy-psx",
    "*.py": "nextpy-psx"
  },
  "emmet.includeLanguages": {
    "nextpy-psx": "html"
  },
  "emmet.triggerExpansionOnTab": true,
  "editor.quickSuggestions": {
    "strings": true
  },
  "editor.tabSize": 4,
  "editor.insertSpaces": true,
  "python.defaultInterpreterPath": "./venv/bin/python",
  "python.linting.enabled": true,
  "python.formatting.provider": "black",
  "psx.languageServer.enabled": true,
  "psx.languageServer.path": "./.nextpy/devtools/psx-language-server",
  "psx.formatting.enabled": true,
  "psx.validation.enabled": true,
  "psx.autocomplete.enabled": true,
  "psx.autoImport.enabled": true,
  "psx.suggestions.enabled": true,
  "python.analysis.autoImportCompletions": true,
  "python.analysis.autoCompleteBrackets": true,
  "python.analysis.typeCheckingMode": "basic",
  "editor.suggestSelection": "first",
  "editor.wordBasedSuggestions": true,
  "editor.parameterHints.enabled": true,
  "editor.snippetSuggestions": "inline"
}""")
    click.echo("  Created: .vscode/settings.json (PSX support + Language Server)")

    # Create VS Code extensions recommendation
    (project_dir / ".vscode" / "extensions.json").write_text("""{
  "recommendations": [
    "nextpy-framework.nextpy-psx",
    "ms-python.python",
    "ms-python.black-formatter",
    "bradlc.vscode-tailwindcss"
  ]
}""")
    click.echo("  Created: .vscode/extensions.json")

    # Create launch configuration for debugging PSX language server
    (project_dir / ".vscode" / "launch.json").write_text("""{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Debug PSX Language Server",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/.nextpy/devtools/psx-language-server",
      "console": "integratedTerminal",
      "cwd": "${workspaceFolder}",
      "args": ["--stdio"]
    }
  ]
}""")
    click.echo("  Created: .vscode/launch.json (Language Server Debugging)")

    # Create NextPy configuration
    (project_dir / ".nextpy" / "config.js").write_text("""/** NextPy Configuration */
module.exports = {
  // App configuration
  app: {
    name: "NextPy App",
    description: "A modern Python web framework with True JSX",
    version: "1.0.0"
  },
  
  // Build configuration
  build: {
    outputDir: ".nextpy/build",
    staticDir: "public"
  },
  
  // Development configuration
  dev: {
    port: 5000,
    host: "0.0.0.0",
    autoReload: true
  },
  
  // PSX configuration
  psx: {
    enabled: true,
    strictMode: true,
    experimentalFeatures: false
  }
}""")
    click.echo("  Created: .nextpy/config.js")


def _create_traditional_homepage(project_dir: Path):
    """Create traditional Python homepage (non-PSX)"""
    (project_dir / "pages" / "index.py").write_text(
        '''"""Traditional NextPy Homepage (without PSX)"""

def Home(props=None):
    """Traditional Python component"""
    props = props or {}
    title = props.get("title", "Welcome to NextPy")
    message = props.get("message", "Python-powered web framework")
    
    return """
    <div class="flex items-center justify-center min-h-screen bg-gradient-to-br from-blue-500 to-purple-600">
        <div class="text-center text-white">
            <h1 class="mb-4 text-5xl font-bold">{title}</h1>
            <p class="mb-8 text-xl">{message}</p>
            <a href="/about" class="inline-block px-6 py-3 font-semibold text-blue-600 transition-colors bg-white rounded-lg shadow-lg hover:bg-gray-100">
                Learn More
            </a>
        </div>
    </div>
    """.format(title=title, message=message)

def getServerSideProps(context):
    return {
        "props": {
            "title": "Welcome to NextPy",
            "message": "Python-powered web framework"
        }
    }

default = Home
'''
    )
    click.echo("  Created: pages/index.py (traditional homepage)")


def _generate_page(name: str):
    """Generate a new PSX page"""
    page_path = Path(f"pages/{name}.py")

    if page_path.exists():
        click.echo(click.style(f"  ❌ Page '{name}' already exists", fg="red"))
        return

    # Pre-compute the title to avoid f-string conflicts
    component_name = name.title()

    content = f'''"""
{component_name} Page - PSX Component
"""

from nextpy.psx import component

@component
def {component_name}(props=None):
    """{component_name} page component"""
    props = props or {{}}
    
    return (
        <div class="min-h-screen py-8 bg-gray-50">
            <div class="container px-4 mx-auto">
                <h1 class="mb-8 text-4xl font-bold text-center">{component_name}</h1>
                <div class="max-w-4xl mx-auto">
                    <p class="text-lg text-center text-gray-600">
                        This is the {name} page created with NextPy PSX.
                    </p>
                </div>
            </div>
        </div>
    )

def getServerSideProps(context):
    """Server-side props for {name} page"""
    return {{
        "props": {{
            "title": "{component_name} Page"
        }}
    }}

default = {component_name}
'''

    page_path.write_text(content)
    click.echo(f"  Created: {page_path}")


def _generate_component(name: str):
    """Generate a new PSX component"""
    component_path = Path(f"components/{name}.py")

    if component_path.exists():
        click.echo(click.style(f"  ❌ Component '{name}' already exists", fg="red"))
        return

    # Pre-compute the title to avoid f-string conflicts
    component_name = name.title()

    content = f'''"""
{component_name} Component - PSX Component
"""

from nextpy.psx import component

@component
def {component_name}(props=None):
    """{component_name} component"""
    props = props or {{}}
    
    return (
        <div class="p-4 bg-white rounded-lg shadow">
            <h3 class="mb-2 text-lg font-semibold">{component_name}</h3>
            <div class="text-gray-600">
                {{props.get("children", "Default content")}}
            </div>
        </div>
    )

default = {component_name}
'''

    component_path.write_text(content)
    click.echo(f"  Created: {component_path}")


def _generate_api(name: str):
    """Generate a new API route"""
    api_path = Path(f"pages/api/{name}.py")

    if api_path.exists():
        click.echo(click.style(f"  ❌ API '{name}' already exists", fg="red"))
        return

    # Pre-compute the title to avoid f-string conflicts
    component_name = name.title()

    content = f'''"""
{component_name} API Route
"""

def get(request):
    """GET handler for {name} API"""
    return {{
        "message": "Hello from {component_name} API",
        "method": "GET",
        "status": "success"
    }}

def post(request):
    """POST handler for {name} API"""
    return {{
        "message": "Hello from {component_name} API",
        "method": "POST",
        "status": "success"
    }}
'''

    api_path.write_text(content)
    click.echo(f"  Created: {api_path}")


if __name__ == "__main__":
    cli()
