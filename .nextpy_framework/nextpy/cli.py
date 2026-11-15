"""
NextPy CLI - Command-line interface for NextPy projects
Commands: dev, build, start
"""

import os
import sys
import time
import secrets
import asyncio
import signal
import threading
from pathlib import Path
from typing import Optional

import click
import uvicorn
import subprocess
import shutil

from nextpy import __version__

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
        self._last_tailwind_build = 0.0
        self._tailwind_build_lock = threading.Lock()

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
        self._schedule_tailwind_build(file_path)

    def _schedule_tailwind_build(self, file_path: str = None):
        """Rebuild Tailwind CSS in the background when source files change.

        Tailwind v4 scans .py/.html sources for class candidates, so edits
        to pages/components must regenerate public/tailwind.css — otherwise
        new utilities only appear after a full restart.
        """
        if not file_path:
            return
        if not str(file_path).endswith(('.py', '.html', '.jsx', '.css')):
            return
        now = time.time()
        if now - self._last_tailwind_build < 2.0:
            return
        with self._tailwind_build_lock:
            if now - self._last_tailwind_build < 2.0:
                return
            self._last_tailwind_build = now
        threading.Thread(target=self._run_tailwind_build, daemon=True).start()

    def _run_tailwind_build(self):
        """Run `npm run build:tailwind` without blocking the reload path."""
        try:
            proj_root = Path.cwd()
            if not (proj_root / "package.json").exists():
                return
            npm_bin = shutil.which("npm")
            if not npm_bin:
                return
            subprocess.run(
                [npm_bin, "run", "build:tailwind"],
                cwd=str(proj_root),
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=120,
            )
        except Exception:
            pass  # CSS rebuild is best-effort; server reload still proceeds

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
        """Broadcast an HMR signal to all SSE-connected browsers, then
        invoke the server reload callback (which restarts uvicorn)."""
        # Notify every browser tab listening on /__nextpy/hmr so the browser
        # starts polling for the new server before uvicorn has finished
        # restarting.  The SSE client script reconnects automatically and
        # reloads the page the moment the server is responsive again.
        try:
            from nextpy.server.app import _hmr_signal_all
            _hmr_signal_all()
        except Exception:
            pass  # HMR notification is best-effort

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
    """Return the ASGI target for the project entry point."""
    main_file = Path.cwd() / "main.py"
    if not main_file.exists():
        raise click.ClickException(
            "No main.py found. Run this command from a NextPy project root "
            "or create one with 'nextpy create <name>'."
        )
    return "main:app"


def _prepare_project() -> None:
    """Load the project .env and make the project importable."""
    project_dir = Path.cwd().resolve()
    if str(project_dir) not in sys.path:
        sys.path.insert(0, str(project_dir))
    from nextpy.config import reload_settings

    reload_settings(str(project_dir))


def _init_project_db():
    """Load .env, register project models, initialize SQLAlchemy."""
    _prepare_project()
    try:
        import nextpy.db  # noqa: F401  (registers app tables on nextpy.db.Base)
    except ImportError:
        pass
    from nextpy.config import settings
    from nextpy.db import init_db

    # Ensure database URL is absolute path for consistency
    db_url = settings.get("database_url", "sqlite:///app.db")
    if db_url.startswith("sqlite:///"):
        db_path = db_url.replace("sqlite:///", "")
        if not os.path.isabs(db_path):
            # Resolve relative to the actual project root context
            project_dir = Path.cwd().resolve()
            abs_path = os.path.abspath(project_dir / db_path)
            db_url = f"sqlite:///{abs_path}"
            settings["database_url"] = db_url

    return init_db(db_url)



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
@click.version_option(version=__version__, prog_name="NextPy")
def cli():
    """NextPy - The Python Web Framework"""
    pass


@cli.command()
@click.option("--port", "-p", default=None, type=int, help="Port to run the server on")
@click.option("--host", "-h", default=None, help="Host to bind to")
@click.option("--reload/--no-reload", default=True, help="Enable hot reload")
@click.option("--debug/--no-debug", default=True, help="Enable debug mode")
def dev(port: int, host: str, reload: bool, debug: bool):
    """Start the development server with enhanced hot reload"""
    _prepare_project()
    _ensure_project_structure()

    from nextpy.config import settings
    port = port or int(settings.get("port", 8000))
    host = host or settings.get("host", "0.0.0.0")

    debug_value = "true" if debug else "false"
    os.environ["NEXTPY_DEBUG"] = debug_value
    os.environ["DEBUG"] = debug_value
    os.environ["DEVELOPMENT"] = "true"

    settings["debug"] = debug
    settings["nextpy_debug"] = debug
    settings["development"] = True

    # Initialize database cleanly with explicit path maps before starting server
    from nextpy.db import init_db
    db_url = settings.get("database_url", "sqlite:///app.db")
    if db_url.startswith("sqlite:///"):
        db_path = db_url.replace("sqlite:///", "")
        if not os.path.isabs(db_path):
            project_dir = Path.cwd().resolve()
            abs_path = os.path.abspath(project_dir / db_path)
            db_url = f"sqlite:///{abs_path}"
            settings["database_url"] = db_url
            
    init_db(db_url)

    main_module = find_main_module()
    project_dir = Path.cwd()
    os.chdir(project_dir)

    main_module = find_main_module()
    project_dir = Path.cwd()
    os.chdir(project_dir)
    os.environ["PYTHONPATH"] = os.pathsep.join(
        [str(project_dir), os.environ.get("PYTHONPATH", "")]
    ).rstrip(os.pathsep)

    click.echo(click.style("\n  NextPy Development Server", fg="cyan", bold=True))
    click.echo(click.style("  ========================\n", fg="cyan"))
    click.echo(f"  Local:    http://localhost:{port}")
    click.echo(f"  Network:  http://{host}:{port}")
    click.echo(f"  Entry:    main.py")
    click.echo(f"  Reload:   {'on' if reload else 'off'}")
    click.echo(f"  Debug:    {'on' if debug else 'off'}")
    if reload and not WATCHDOG_AVAILABLE:
        click.echo(click.style("  Watchdog: not installed (using polling reload)", fg="yellow"))
    click.echo(click.style("\n  Starting server...\n", fg="bright_black"))

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
            app_dir=str(project_dir),
            reload_dirs=existing_reload_dirs,
            reload_includes=reload_includes,
            log_level="info",
        )
    else:
        uvicorn.run(
            main_module,
            host=host,
            port=port,
            app_dir=str(project_dir),
            log_level="info",
        )


@cli.command()
@click.option("--out", "-o", default="out", help="Output directory for static files")
@click.option("--clean/--no-clean", default=True, help="Clean output directory first")
@click.option("--optimize/--no-optimize", default=True, help="Enable build optimization")
@click.option("--minify/--no-minify", default=True, help="Minify JS/CSS assets")
@click.option("--tree-shake/--no-tree-shake", default=True, help="Enable tree shaking")
@click.option("--code-split/--no-code-split", default=True, help="Enable code splitting")
def build(out: str, clean: bool, optimize: bool, minify: bool, tree_shake: bool, code_split: bool):
    """Build the project for production with enhanced feedback"""
    click.echo(click.style("\n  🔨 NextPy Static Build", fg="green", bold=True))
    click.echo(click.style("  ===================\n", fg="green"))

    try:
        _prepare_project()
        from nextpy.core.builder import Builder

        click.echo(f"Output directory: {out}/")
        if clean:
            click.echo(f"Cleaning output directory...")

        if optimize:
            click.echo(f"Optimization enabled: minify={minify}, tree_shake={tree_shake}, code_split={code_split}")

        click.echo(f"Initializing builder...")
        builder = Builder(
            out_dir=out,
            optimize=optimize,
            minify=minify,
            tree_shaking=tree_shake,
            code_splitting=code_split,
        )

        click.echo(f"Building static files...")

        async def run_build():
            manifest = await builder.build(clean=clean)
            return manifest

        manifest = asyncio.run(run_build())

        pages_count = len(manifest.get("pages", {}))
        assets_count = len(manifest.get("assets", []))
        total_size = manifest.get("total_size", 0)
        optimization = manifest.get("optimization", {})

        click.echo()
        click.echo(
            click.style(f"Build completed successfully!", fg="green", bold=True)
        )
        click.echo(f"Pages built: {pages_count}")
        click.echo(f"Assets processed: {assets_count}")
        click.echo(f"Total size: {_format_size(total_size)}")
        if optimization:
            ts = optimization.get("tree_shaking", {})
            cs = optimization.get("code_splitting", {})
            mn = optimization.get("minification", {})
            click.echo(f"Tree shaking: {ts.get('unused_count', 0)} unused modules flagged (report only)")
            click.echo(f"Code splitting: {cs.get('chunk_count', 0)} chunks")
            click.echo(f"Minification: {mn.get('bytes_saved', 0)} bytes saved")
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
@click.option("--port", "-p", default=None, type=int, help="Port to run the server on")
@click.option("--host", "-h", default=None, help="Host to bind to")
def start(port: int, host: str):
    """Start the production server with enhanced feedback"""
    _prepare_project()
    from nextpy.config import settings
    port = port or int(settings.get("port", 5000))
    host = host or settings.get("host", "0.0.0.0")
    main_module = find_main_module()
    project_dir = Path.cwd()
    os.chdir(project_dir)
    os.environ["PYTHONPATH"] = os.pathsep.join(
        [str(project_dir), os.environ.get("PYTHONPATH", "")]
    ).rstrip(os.pathsep)
    os.environ["DEBUG"] = "false"
    os.environ["NEXTPY_DEBUG"] = "false"
    os.environ["DEVELOPMENT"] = "false"

    settings["debug"] = False
    settings["nextpy_debug"] = False
    settings["development"] = False

    # In-process singletons (websocket connections, StateManager, admin
    # sessions, rate-limit buckets) do not span workers. Default to a single
    # worker so realtime/state-sync features work; override with
    # NEXTPY_WORKERS if you don't use them (or add sticky sessions + a shared
    # backplane first).
    workers = int(os.environ.get("NEXTPY_WORKERS", "1"))
    if workers > 1:
        click.echo(click.style(
            f"  Warning: running {workers} workers — WebSocket channels, "
            "StateManager, and rate limiting are per-process and will not "
            "be consistent across workers.",
            fg="yellow"))

    click.echo(click.style("\n  NextPy Production Server", fg="green", bold=True))
    click.echo(click.style("  ========================\n", fg="green"))
    click.echo(f"  Local:    http://localhost:{port}")
    click.echo(f"  Network:  http://{host}:{port}")
    click.echo(f"  Entry:    main.py")
    click.echo(f"  Workers:  {workers}")
    click.echo(click.style("\n  Starting server...\n", fg="bright_black"))

    try:
        uvicorn.run(
            main_module,
            host=host,
            port=port,
            workers=workers,
            app_dir=str(project_dir),
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
@click.option("--username", prompt="Username", help="Superuser username")
@click.option("--email", prompt="Email", help="Superuser email")
@click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True, help="Superuser password")
def createsuperuser(username: str, email: str, password: str):
    """Create or update an admin superuser in the project database."""
    username = username.strip()
    email = email.strip().lower()
    if not username or not email or not password:
        raise click.ClickException("Username, email, and password are required.")

    try:
        db = _init_project_db()
        from nextpy.auth import hash_password
        from nextpy.db import User, get_session
        from sqlalchemy import or_

        session = get_session()
        try:
            user = (
                session.query(User)
                .filter(or_(User.username == username, User.email == email))
                .first()
            )
            if user:
                user.username = username
                user.email = email
                user.role = "superuser"
                user.is_active = True
                user.hashed_password = hash_password(password)
                action = "Updated"
            else:
                user = User(
                    username=username,
                    email=email,
                    full_name=username,
                    role="superuser",
                    is_active=True,
                    hashed_password=hash_password(password),
                )
                session.add(user)
                action = "Created"
            session.commit()
        finally:
            session.close()
    except Exception as exc:
        raise click.ClickException(f"Could not create superuser: {exc}") from exc

    click.echo(click.style(f"\n  {action} superuser '{username}'", fg="green", bold=True))
    click.echo(f"  Sign in at /admin with these credentials.")


@cli.command("flushdb")
@click.option("--username", prompt="Superuser username", help="Admin username or email")
@click.option("--password", prompt=True, hide_input=True, help="Admin password")
@click.option("--yes", is_flag=True, help="Skip the confirmation prompt")
def flushdb(username: str, password: str, yes: bool):
    """Drop and recreate every table after superuser verification."""
    try:
        db = _init_project_db()
        from nextpy.auth import verify_password
        from nextpy.db import User, get_session
        from sqlalchemy import or_

        session = get_session()
        try:
            user = (
                session.query(User)
                .filter(or_(User.username == username, User.email == username))
                .first()
            )
            authorized = bool(
                user
                and getattr(user, "is_active", True)
                and (user.role or "").lower() in {"superuser", "admin", "staff"}
                and user.hashed_password
                and verify_password(password, user.hashed_password)
            )
        finally:
            session.close()

        if not authorized:
            raise click.ClickException("Invalid superuser credentials. Database was not changed.")

        if not yes:
            click.confirm(
                "This deletes all tables and data in the project database. Continue?",
                abort=True,
            )

        db.drop_tables()
        db.create_tables()
    except click.ClickException:
        raise
    except Exception as exc:
        raise click.ClickException(f"Database flush failed: {exc}") from exc

    click.echo(click.style("\n  Database flushed and tables recreated.", fg="green", bold=True))


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
            f" npm run build:tailwind  # Build Tailwind CSS (if you prefer manual build)"
        )
        click.echo(f" nextpy dev  # Start development server")
        click.echo(f"  Open http://localhost:8000 in your browser")

        if psx:
            click.echo(f"\nPSX Development:")
            click.echo(f"    • All PSX utilities, hooks & components auto-imported")
            click.echo(f"    • Use: from nextpy import component, useState, useEffect")
            click.echo(f"    • Full auto-completion & IntelliSense support")
            click.echo(f"    • Edit pages/index.psx to see PSX in action")
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
        _prepare_project()
        from nextpy.core.builder import Builder

        click.echo(f"Output directory: {out}/")
        click.echo(f" Initializing exporter...")

        builder = Builder(out_dir=out)

        click.echo(f"Exporting static files...")

        async def run_export():
            manifest = await builder.build(clean=True)
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

    click.echo(f"Version: {__version__}")
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
    click.echo(f"    Version: {__version__}")
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
    click.echo(click.style("\n  🛠️  Available Commands:", fg="magenta", bold=True))
    commands = [
        ("nextpy dev", "Start development server"),
        ("nextpy build", "Build for production"),
        ("nextpy start", "Start production server"),
        ("nextpy create <name>", "Create new project"),
        ("nextpy generate <type> <name>", "Generate components/pages/APIs"),
        ("nextpy createsuperuser", "Create an admin superuser"),
        ("nextpy flushdb", "Reset the project database (superuser only)"),
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
        "pages/actions",
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
    <link href="/tailwind.css" rel="stylesheet">
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
    <link href="/tailwind.css" rel="stylesheet">
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
        _create_framework_showcase(project_dir)
        _create_additional_pages(project_dir)
        _create_vscode_settings(project_dir)
    else:
        _create_traditional_homepage(project_dir)


    (project_dir / "components" / "ui" / "Button.psx").write_text(
        '''
"""Reusable button component."""

from nextpy.psx import component


@component
def Button(props=None):
    props = props or {}
    variant = props.get("variant", "primary")
    children = props.get("children", "Button")
    class_name = props.get("className", "")

    variants = {
        "primary": "bg-blue-600 text-white hover:bg-blue-700",
        "secondary": "bg-gray-200 text-gray-900 hover:bg-gray-300",
        "success": "bg-green-600 text-white hover:bg-green-700",
        "danger": "bg-red-600 text-white hover:bg-red-700",
    }
    variant_class = variants.get(variant, variants["primary"])
    class_attr = (
        "px-6 py-3 rounded-lg font-medium transition-all duration-200 "
        f"transform hover:scale-105 {variant_class} {class_name}"
    )

    return (
        <button
            class={class_attr}
            id={props.get("id")}
            disabled={props.get("disabled", False)}
            onclick={props.get("onClick", "")}
        >
            {children}
        </button>
    )


default = Button
'''
    )
    click.echo("  Created: components/ui/Button.psx(enhanced interactive)")
    
    # Create comprehensive API examples
    (project_dir / "pages" / "api" / "hello.py").write_text(
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
    click.echo("  Created: pages/api/hello.py")

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

    # Create database models.  Every model must import the framework Base so
    # init_db() sees it when creating tables.
    (project_dir / "models" / "User.py").write_text('''"""User model example."""

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from nextpy.db import Base


class AppUser(Base):
    # The framework already owns the "users" table, so app models need a
    # distinct table name and class name to avoid SQLAlchemy registry
    # collisions with nextpy.db.User.
    __tablename__ = "app_users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f"<AppUser(id={self.id}, name='{self.name}', email='{self.email}')>"


User = AppUser
''')
    click.echo("  Created: models/User.py")

    (project_dir / "models" / "__init__.py").write_text('''"""Import every model here so init_db() can create its table."""

from models.User import AppUser, User

__all__ = ["AppUser", "User"]
''')
    click.echo("  Created: models/__init__.py")

    # Create the application entry point.  init_db() is called here, after all
    # models have been imported, so SQLAlchemy knows every table.
    (project_dir / "main.py").write_text('''

"""NextPy application entry point."""

import sys
import os
from pathlib import Path

# Support running from a source checkout that vendors the framework.
_framework_dir = Path(__file__).parent / ".nextpy_framework"
if _framework_dir.exists():
    sys.path.insert(0, str(_framework_dir))

import nextpy as nx
from nextpy.admin import AdminSite
from nextpy.config import settings
from nextpy.db import User, init_db

# Importing models registers them on nextpy.db.Base.
import models  # noqa: F401

# Import server actions to register them
try:
    from pages.actions import *  # noqa: F401
except ImportError:
    pass  # No server actions yet

admin_site = AdminSite()
admin_site.register(User)

# Define the app instance cleanly so Uvicorn can import it
app = nx.create_app(
    pages_dir="pages",
    templates_dir="templates",
    public_dir="public",
    out_dir="out",
    debug=settings["debug"],
    admin_site=admin_site,
)

# Initialize the database at import time so it also runs inside uvicorn's
# reload worker (which imports ``main:app`` rather than executing __main__).
db_url = settings["database_url"]
if db_url.startswith("sqlite://"):
    # Normalize SQLite URL format
    parts = db_url.split("://", 1)
    if len(parts) == 2:
        scheme, path = parts
        if path.startswith("/"):
            # Absolute path - ensure three slashes
            path = path.lstrip("/")
            db_url = f"{scheme}:///{path}"
        else:
            # Relative path - use sqlite:///./path format
            db_url = f"{scheme}:///./{path}"

init_db(db_url)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings["host"],
        port=settings["port"],
        reload=settings["development"],
    )

''')
    click.echo("  Created: main.py")

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

from nextpy.psx import component

@component
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

    post = posts.get(slug)
    if post is None:
        return {"not_found": True}
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

    (project_dir / "pages/actions" / "__init__.py").write_text('''
"""Server actions for this NextPy app.

Server actions let client-side components call Python functions without
writing API routes.  Every function decorated with ``@server_action`` is
registered automatically when ``main.py`` runs
``from pages.actions import *``.  Call them from PSX components with::

    callServerAction("greet", {"name": "World"})

The result lands in the ``_server_result`` state variable (loading in
``_server_loading``, errors in ``_server_error``).
"""

import time

import nextpy as nx
from nextpy.server_actions import server_action, ServerActionError, ValidationError
from nextpy.websocket import manager as ws_manager

# In-memory demo stores — swap for nextpy.db models in a real app.
_notes = []
_task_log = []


@server_action()
def greet(name: str = "world"):
    """Simple action: returns a greeting."""
    name = (name or "").strip() or "world"
    return {"op": "greet", "message": f"Hello, {name}!"}


@server_action()
def add_note(content: str = ""):
    """Add a note to the in-memory store."""
    content = (content or "").strip()
    if not content:
        raise ValidationError("content", "Note cannot be empty")
    note = {"id": len(_notes) + 1, "content": content, "created_at": time.time()}
    _notes.append(note)
    return {"op": "add_note", "note": note}


@server_action()
def list_notes():
    """Return all stored notes."""
    return {"op": "list_notes", "notes": list(_notes)}


@server_action()
def clear_notes():
    """Delete all notes."""
    _notes.clear()
    return {"op": "clear_notes"}


@server_action()
async def broadcast_demo(message: str = "Hello from NextPy!"):
    """Publish an event to every client subscribed to the 'demo' channel.

    Pairs with ``pages/live.py`` — open two browser tabs to see
    real-time fan-out through the framework WebSocket endpoint.
    """
    await ws_manager.publish("demo", {
        "type": "DEMO_EVENT",
        "payload": {"message": message, "timestamp": time.time()},
    })
    return {"op": "broadcast", "published": True, "channel": "demo"}


def _background_work(item: str) -> str:
    """Runs on the background queue — never blocks the HTTP request."""
    time.sleep(1)
    result = f"processed:{item}"
    _task_log.append({"item": item, "result": result, "at": time.time()})
    return result


@server_action()
def run_background_demo(item: str = "demo"):
    """Enqueue work on the background task queue and return immediately."""
    from nextpy import enqueue
    enqueue(_background_work, item)
    return {"op": "bg", "queued": True, "item": item}


@server_action()
def get_task_log():
    """Return completed background-task results."""
    tasks = [f"{t['item']} -> {t['result']}" for t in _task_log]
    return {"op": "task_log", "tasks": tasks}


# Auth actions (register / login / logout / get_me) — cookie sessions.
try:
    from . import auth_actions  # noqa: F401,E402
except ImportError:
    pass  # Auth actions not available
''')
    click.echo("  Created: pages/actions/__init__.py (server actions)")

    
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
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import app
from fastapi.testclient import TestClient

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

    (project_dir / "requirements.txt").write_text("""fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.0.0
pydantic-settings>=2.0.0
email-validator>=2.0.0
SQLAlchemy>=2.0.0
PyJWT>=2.8.0
jinja2>=3.1.0
watchdog>=2.3.0
click>=8.1.0
python-multipart>=0.0.6
aiofiles>=23.0.0
python-dotenv>=1.0.0
httpx>=0.28.1
websockets>=12.0
pillow>=10.0.0
markdown>=3.5.0

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

# Environment files
.env
.env.local
.env.*.local
!.env.example

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


    # create .env file with generated secrets
    _secret_key = secrets.token_urlsafe(48)
    _jwt_secret = secrets.token_urlsafe(48)
    _session_secret = secrets.token_urlsafe(48)

    # Create .env.example file (without secrets)
    (project_dir / ".env.example").write_text("""# NextPy Development Environment
DEVELOPMENT=true
DEBUG=true
NEXTPY_DEBUG=true

# Server Configuration
HOST=0.0.0.0
PORT=8000

# Database Configuration
DATABASE_URL=sqlite:///nextpy.db

# Secrets (generate your own - see .env for example)
SECRET_KEY=your-secret-key-here
JWT_SECRET=your-jwt-secret-here
SESSION_SECRET=your-session-secret-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# Security
CSRF_PROTECTION=true
RATE_LIMIT_ENABLED=true
CORS_ORIGINS=

# NextPy Settings
NEXTPY_DEBUG_ICON=true
NEXTPY_HOT_RELOAD=true
NEXTPY_HMR=true
NEXTPY_LOG_LEVEL=info
""")

    # Create .env file with generated secrets (gitignored)
    (project_dir / ".env").write_text(f"""# NextPy Development Environment
DEVELOPMENT=true
DEBUG=true
NEXTPY_DEBUG=true

# Server Configuration
HOST=0.0.0.0
PORT=8000

# Database Configuration
DATABASE_URL=sqlite:///nextpy.db

# Secrets (generated for this project)
SECRET_KEY={_secret_key}
JWT_SECRET={_jwt_secret}
SESSION_SECRET={_session_secret}
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# Security
CSRF_PROTECTION=true
RATE_LIMIT_ENABLED=true
CORS_ORIGINS=

# NextPy Settings
NEXTPY_DEBUG_ICON=true
NEXTPY_HOT_RELOAD=true
NEXTPY_HMR=true
NEXTPY_LOG_LEVEL=info
""")

    click.echo("  Created: .env.example")
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
    """Create PSX sample components (the homepage is written as index.psx)."""

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

    # Create PSX homepage
    (project_dir / "pages" / "index.py").write_text('''"""Interactive Homepage with PSX"""

from nextpy.psx import component, useState

@component
def Home(props=None):
    props = props or {}
    title = props.get("title", "Welcome to NextPy!")
    message = props.get("message", "Build amazing web apps with Python and True JSX")
    [count, setCount] = useState(0)

    return (
        <div class="flex flex-col items-center justify-between min-h-screen p-8 font-sans antialiased text-black bg-white selection:bg-gray-200">
            <div class=""></div>

            <div class="flex flex-col items-center max-w-xl gap-8 text-center">
                <h1 class="text-[56px] font-extrabold tracking-tighter leading-none select-none font-mono flex items-baseline">
                    <img src="/static/images/logo.png" alt="NextPy Logo" class="w-auto h-16" />
                </h1>

                <h2 class="text-4xl font-bold">{title}</h2>
                <p class="text-xl text-gray-600">{message}</p>

                <div class="flex items-center gap-4">
                    <button onclick={lambda e: setCount(count + 1)} class="px-6 py-3 font-semibold text-white bg-blue-600 rounded-lg hover:bg-blue-700">
                        Count: {count}
                    </button>
                    <a href="/features" class="px-6 py-3 font-semibold text-blue-600 bg-white border border-blue-600 rounded-lg hover:bg-blue-50">
                        Features
                    </a>
                </div>

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
    click.echo("  Created: pages/index.py (PSX homepage)")


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
                                "code": "Use @component on a Python function and return JSX."
                            },
                            {
                                "title": "Python Logic in JSX",
                                "content": "Use real Python for loops, if conditions, and try-catch in your JSX",
                                "code": "Use a Python for loop directly inside JSX braces."
                            },
                            {
                                "title": "Virtual DOM",
                                "content": "Optimized rendering with diffing and patching for maximum performance",
                                "code": "The renderer builds and diffs virtual nodes for you."
                            },
                            {
                                "title": "Server-Side Rendering",
                                "content": "Full SSR support with getServerSideProps and getStaticProps",
                                "code": "Return props from getServerSideProps(context)."
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
                                {if True:
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


def _create_framework_showcase(project_dir: Path):
    """Generate demo pages covering every major framework capability.

    These are working examples, not stubs — a freshly created app can
    exercise server actions, cookie auth, SSG/ISR, WebSockets, background
    tasks, and PSX animations out of the box.
    """
    click.echo("  Creating framework showcase pages...")

    (project_dir / "pages" / "actions" / "auth_actions.py").write_text('''"""Authentication server actions — register, login, logout, get_me.

All use cookie-based sessions backed by ``nextpy.db.User``.  The ``request``
and ``response`` parameters are injected automatically by the action runtime.
"""

from fastapi import Request, Response
from nextpy.db import get_session, User
from nextpy.auth import (
    hash_password, verify_password,
    set_session_cookie, get_user_id_from_request,
    clear_session_cookie, delete_session, COOKIE_NAME,
)
from nextpy.server_actions import server_action


def _user_dict(user) -> dict:
    return {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "full_name": user.full_name or "",
        "role": user.role or "user",
    }


def _rotate_session(request: Request, response: Response, user_id: int) -> None:
    """Replace any existing session with a fresh one on login/register."""
    old_session_id = request.cookies.get(COOKIE_NAME)
    if old_session_id:
        delete_session(old_session_id)
    set_session_cookie(response, user_id, secure=request.url.scheme == "https")


@server_action()
async def register(
    request: Request,
    response: Response,
    email: str = "",
    username: str = "",
    full_name: str = "",
    password: str = "",
):
    """Register a new user account."""
    email = (email or "").strip().lower()
    username = (username or "").strip()
    full_name = (full_name or "").strip()
    password = password or ""

    if not email or not username or not password:
        return {"success": False, "error": "Email, username and password are required"}
    if len(password) < 6:
        return {"success": False, "error": "Password must be at least 6 characters"}

    db = get_session()
    try:
        if db.query(User).filter(User.email == email).first():
            return {"success": False, "error": "Email already registered"}
        if db.query(User).filter(User.username == username).first():
            return {"success": False, "error": "Username already taken"}

        user = User(
            email=email,
            username=username,
            full_name=full_name,
            hashed_password=hash_password(password),
            role="user",
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        _rotate_session(request, response, user.id)
        return {"success": True, "user": _user_dict(user), "message": "Account created"}
    except Exception as e:
        db.rollback()
        return {"success": False, "error": str(e)}
    finally:
        db.close()


@server_action()
async def login(
    request: Request,
    response: Response,
    email: str = "",
    password: str = "",
):
    """Log in an existing user."""
    email = (email or "").strip().lower()
    password = password or ""

    if not email or not password:
        return {"success": False, "error": "Email and password are required"}

    db = get_session()
    try:
        user = db.query(User).filter(User.email == email).first()
        if user is None or not verify_password(password, user.hashed_password):
            return {"success": False, "error": "Invalid email or password"}

        _rotate_session(request, response, user.id)
        return {"success": True, "user": _user_dict(user), "message": "Logged in"}
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        db.close()


@server_action()
async def logout(request: Request, response: Response):
    """Log out the current user by clearing the session cookie."""
    session_id = request.cookies.get(COOKIE_NAME, "")
    if session_id:
        clear_session_cookie(response, session_id, secure=request.url.scheme == "https")
    else:
        response.delete_cookie(COOKIE_NAME, path="/")
    return {"success": True, "message": "Logged out"}


@server_action()
async def get_me(request: Request):
    """Get the currently authenticated user, or null."""
    user_id = get_user_id_from_request(request)
    if user_id is None:
        return {"user": None}

    db = get_session()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        return {"user": _user_dict(user) if user else None}
    finally:
        db.close()
''')
    click.echo("  Created: pages/actions/auth_actions.py")

    (project_dir / "pages" / "login.py").write_text('''"""Login page — cookie-session auth via the ``login`` server action."""

from nextpy.psx import component, interactive_component, useState, useEffect, callServerAction, Motion


@interactive_component
def LoginPage(props=None):
    [email, setEmail] = useState("")
    [password, setPassword] = useState("")
    [error, setError] = useState("")
    [_server_result, _setServerResult] = useState(None)
    [_server_loading, _setServerLoading] = useState(False)

    def handle_login(e):
        setError("")
        callServerAction("login", {"email": email, "password": password})

    def handle_result():
        if _server_result:
            if _server_result.get("success"):
                window.nextpyHardNavigate("/account")
            else:
                setError(_server_result.get("error", "Login failed"))

    useEffect(handle_result, [_server_result])

    input_cls = "w-full rounded-xl border border-gray-300 bg-gray-50/50 px-4 py-3 text-gray-900 placeholder-gray-400 transition focus:border-indigo-500 focus:bg-white focus:outline-none focus:ring-4 focus:ring-indigo-500/10"

    return (
        <div class="flex min-h-[70vh] items-center justify-center px-4 py-12">
            <Motion
                initial={{"opacity": 0, "transform": "translateY(24px)"}}
                animate={{"opacity": 1, "transform": "translateY(0px)"}}
                transition={{"duration": 0.5, "easing": "ease-out"}}
                className="w-full max-w-md"
            >
                <div class="mb-8 text-center">
                    <h1 class="text-3xl font-bold tracking-tight text-gray-900">Welcome back</h1>
                    <p class="mt-2 text-gray-500">Log in to your account</p>
                </div>

                <div class="rounded-2xl border border-gray-200 bg-white p-8 shadow-xl shadow-gray-900/5">
                    <div data-state-error data-state-toggle style="display: none" class="mb-5 p-3 text-sm text-red-700 rounded-lg bg-red-50"></div>

                    <form onsubmit={handle_login} class="space-y-5">
                        <div>
                            <label class="mb-1.5 block text-sm font-semibold text-gray-700">Email</label>
                            <input type="email" value={email} oninput={lambda e: setEmail(e.target.value)}
                                required placeholder="you@example.com" autocomplete="email" class={input_cls} />
                        </div>
                        <div>
                            <label class="mb-1.5 block text-sm font-semibold text-gray-700">Password</label>
                            <input type="password" value={password} oninput={lambda e: setPassword(e.target.value)}
                                required placeholder="Your password" autocomplete="current-password" class={input_cls} />
                        </div>
                        <button type="submit" disabled={_server_loading}
                            class="w-full rounded-xl bg-indigo-600 px-4 py-3.5 font-semibold text-white shadow-lg shadow-indigo-600/25 transition-all hover:bg-indigo-700 active:scale-[0.98] disabled:cursor-not-allowed disabled:opacity-60">
                            {"Signing in..." if _server_loading else "Sign in"}
                        </button>
                    </form>

                    <p class="mt-6 text-center text-sm text-gray-500">
                        No account?{" "}
                        <a href="/register" class="font-semibold text-indigo-600 transition hover:text-indigo-500">Sign up</a>
                    </p>
                </div>
            </Motion>
        </div>
    )


default = LoginPage
''')
    click.echo("  Created: pages/login.py")

    (project_dir / "pages" / "register.py").write_text('''"""Registration page — creates an account via the ``register`` server action."""

from nextpy.psx import component, interactive_component, useState, useEffect, callServerAction, Motion


@interactive_component
def RegisterPage(props=None):
    [email, setEmail] = useState("")
    [username, setUsername] = useState("")
    [fullName, setFullName] = useState("")
    [password, setPassword] = useState("")
    [error, setError] = useState("")
    [_server_result, _setServerResult] = useState(None)
    [_server_loading, _setServerLoading] = useState(False)

    def handle_register(e):
        setError("")
        callServerAction("register", {
            "email": email,
            "username": username,
            "full_name": fullName,
            "password": password,
        })

    def handle_result():
        if _server_result:
            if _server_result.get("success"):
                window.nextpyHardNavigate("/account")
            else:
                setError(_server_result.get("error", "Registration failed"))

    useEffect(handle_result, [_server_result])

    input_cls = "w-full rounded-xl border border-gray-300 bg-gray-50/50 px-4 py-3 text-gray-900 placeholder-gray-400 transition focus:border-indigo-500 focus:bg-white focus:outline-none focus:ring-4 focus:ring-indigo-500/10"

    return (
        <div class="flex min-h-[70vh] items-center justify-center px-4 py-12">
            <Motion
                initial={{"opacity": 0, "transform": "translateY(24px)"}}
                animate={{"opacity": 1, "transform": "translateY(0px)"}}
                transition={{"duration": 0.5, "easing": "ease-out"}}
                className="w-full max-w-md"
            >
                <div class="mb-8 text-center">
                    <h1 class="text-3xl font-bold tracking-tight text-gray-900">Create account</h1>
                    <p class="mt-2 text-gray-500">Get started with NextPy</p>
                </div>

                <div class="rounded-2xl border border-gray-200 bg-white p-8 shadow-xl shadow-gray-900/5">
                    <div data-state-error data-state-toggle style="display: none" class="mb-5 p-3 text-sm text-red-700 rounded-lg bg-red-50"></div>

                    <form onsubmit={handle_register} class="space-y-4">
                        <input type="text" value={fullName} oninput={lambda e: setFullName(e.target.value)}
                            placeholder="Full name" class={input_cls} />
                        <input type="text" value={username} oninput={lambda e: setUsername(e.target.value)}
                            required placeholder="Username" autocomplete="username" class={input_cls} />
                        <input type="email" value={email} oninput={lambda e: setEmail(e.target.value)}
                            required placeholder="you@example.com" autocomplete="email" class={input_cls} />
                        <input type="password" value={password} oninput={lambda e: setPassword(e.target.value)}
                            required placeholder="Password (min 6 chars)" autocomplete="new-password" class={input_cls} />
                        <button type="submit" disabled={_server_loading}
                            class="w-full rounded-xl bg-indigo-600 px-4 py-3.5 font-semibold text-white shadow-lg shadow-indigo-600/25 transition-all hover:bg-indigo-700 active:scale-[0.98] disabled:cursor-not-allowed disabled:opacity-60">
                            {"Creating account..." if _server_loading else "Sign up"}
                        </button>
                    </form>

                    <p class="mt-6 text-center text-sm text-gray-500">
                        Already have an account?{" "}
                        <a href="/login" class="font-semibold text-indigo-600 transition hover:text-indigo-500">Log in</a>
                    </p>
                </div>
            </Motion>
        </div>
    )


default = RegisterPage
''')
    click.echo("  Created: pages/register.py")

    (project_dir / "pages" / "account.py").write_text('''"""Protected account page — SSR auth guard + logout server action."""

from nextpy.psx import component, interactive_component, useState, useEffect, callServerAction, Motion


@interactive_component
def AccountPage(props=None):
    user = props.get("user") if props else None
    [_server_result, _setServerResult] = useState(None)

    def handle_logout():
        callServerAction("logout", {})

    def handle_result():
        if _server_result and _server_result.get("success"):
            window.nextpyHardNavigate("/login")

    useEffect(handle_result, [_server_result])

    if not user:
        return (
            <div class="flex min-h-[60vh] items-center justify-center px-4">
                <div class="text-center">
                    <h1 class="text-2xl font-bold text-gray-900">Not signed in</h1>
                    <a href="/login" class="mt-4 inline-block rounded-xl bg-indigo-600 px-6 py-3 font-semibold text-white hover:bg-indigo-700">
                        Go to login
                    </a>
                </div>
            </div>
        )

    return (
        <div class="mx-auto max-w-2xl px-4 py-16">
            <Motion
                initial={{"opacity": 0, "transform": "translateY(20px)"}}
                animate={{"opacity": 1, "transform": "translateY(0px)"}}
                transition={{"duration": 0.5, "easing": "ease-out"}}
            >
                <div class="rounded-2xl border border-gray-200 bg-white p-8 shadow-xl">
                    <h1 class="text-3xl font-bold text-gray-900">Account</h1>
                    <dl class="mt-6 space-y-3 text-gray-700">
                        <div class="flex justify-between border-b border-gray-100 pb-3">
                            <dt class="font-medium text-gray-500">Name</dt>
                            <dd>{user.get("full_name") or user.get("username")}</dd>
                        </div>
                        <div class="flex justify-between border-b border-gray-100 pb-3">
                            <dt class="font-medium text-gray-500">Username</dt>
                            <dd>{user.get("username")}</dd>
                        </div>
                        <div class="flex justify-between border-b border-gray-100 pb-3">
                            <dt class="font-medium text-gray-500">Email</dt>
                            <dd>{user.get("email")}</dd>
                        </div>
                        <div class="flex justify-between">
                            <dt class="font-medium text-gray-500">Role</dt>
                            <dd>{user.get("role")}</dd>
                        </div>
                    </dl>
                    <button onclick={handle_logout}
                        class="mt-8 w-full rounded-xl border border-red-200 px-4 py-3 font-semibold text-red-600 transition hover:bg-red-50">
                        Log out
                    </button>
                </div>
            </Motion>
        </div>
    )


def getServerSideProps(context):
    """SSR auth guard: resolve the session cookie on every request."""
    from nextpy.auth import get_user_id_from_request
    from nextpy.db import get_session, User

    request = context.get("request") or context.get("req")
    user_id = get_user_id_from_request(request) if request else None
    if user_id is None:
        return {"redirect": {"destination": "/login", "permanent": False}}

    db = get_session()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            return {"redirect": {"destination": "/login", "permanent": False}}
        return {
            "props": {
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "username": user.username,
                    "full_name": user.full_name or "",
                    "role": user.role or "user",
                }
            }
        }
    finally:
        db.close()


default = AccountPage
''')
    click.echo("  Created: pages/account.py (protected)")

    (project_dir / "pages" / "showcase.py").write_text('''"""Framework showcase — server actions, notes CRUD, animations, refs.

Demonstrates the interactive PSX stack: useState, callServerAction,
Motion entrance animations, AnimatePresence exits, and data-psx-ref.
"""

from nextpy.psx import component, interactive_component, useState, useEffect, callServerAction, Motion, AnimatePresence


@interactive_component
def Showcase(props=None):
    [count, setCount] = useState(0)
    [name, setName] = useState("World")
    [noteText, setNoteText] = useState("")
    [notes, setNotes] = useState([])
    [taskLog, setTaskLog] = useState([])
    [panelOpen, setPanelOpen] = useState(True)
    [greeting, setGreeting] = useState("")
    [refStatus, setRefStatus] = useState("not checked")
    [_server_result, _setServerResult] = useState(None)
    [_server_loading, _setServerLoading] = useState(False)

    def handle_result():
        if not _server_result:
            return
        op = _server_result.get("op")
        if op == "greet":
            setGreeting(_server_result.get("message", ""))
        elif op == "add_note":
            setNoteText("")
            callServerAction("list_notes", {})
        elif op == "list_notes":
            setNotes(list(_server_result.get("notes", [])))
        elif op == "clear_notes":
            setNotes([])
        elif op == "bg":
            callServerAction("get_task_log", {})
        elif op == "task_log":
            setTaskLog(list(_server_result.get("tasks", [])))

    useEffect(handle_result, [_server_result])

    def check_ref():
        el = window.nextpy.getRef(window.nextpy._componentId, "showcase_card")
        setRefStatus("found" if el else "missing")

    input_cls = "w-full rounded-xl border border-gray-300 bg-gray-50/50 px-4 py-3 text-gray-900 placeholder-gray-400 transition focus:border-indigo-500 focus:bg-white focus:outline-none focus:ring-4 focus:ring-indigo-500/10"
    btn_cls = "rounded-xl bg-indigo-600 px-5 py-2.5 font-semibold text-white transition hover:bg-indigo-700 active:scale-[0.98] disabled:opacity-60"

    return (
        <div class="mx-auto max-w-4xl px-4 py-16">
            <h1 class="mb-2 text-4xl font-extrabold tracking-tight text-gray-900">Framework Showcase</h1>
            <p class="mb-12 text-lg text-gray-500">Every major NextPy capability, working.</p>

            {/* Server actions */}
            <section class="mb-10 rounded-2xl border border-gray-200 bg-white p-8 shadow-sm">
                <h2 class="mb-4 text-xl font-bold text-gray-900">Server Actions</h2>
                <div class="flex flex-wrap items-center gap-4">
                    <input value={name} oninput={lambda e: setName(e.target.value)} placeholder="Your name"
                        class={input_cls + " max-w-xs"} />
                    <button onclick={lambda e: callServerAction("greet", {"name": name})} class={btn_cls}>
                        {"Working..." if _server_loading else "Greet me"}
                    </button>
                    <button onclick={lambda e: callServerAction("list_notes", {})} class={btn_cls + " bg-gray-700 hover:bg-gray-800"}>
                        Refresh notes
                    </button>
                </div>
                {if greeting:
                    <p class="mt-4 rounded-lg bg-indigo-50 px-4 py-3 font-medium text-indigo-700">{greeting}</p>
                }

                <div class="mt-6 flex gap-3">
                    <input value={noteText} oninput={lambda e: setNoteText(e.target.value)} placeholder="Write a note..."
                        class={input_cls} />
                    <button onclick={lambda e: callServerAction("add_note", {"content": noteText})} class={btn_cls}>
                        Add note
                    </button>
                    <button onclick={lambda e: callServerAction("clear_notes", {})} class={btn_cls + " bg-red-600 hover:bg-red-700"}>
                        Clear
                    </button>
                </div>
                <ul class="mt-4 space-y-2">
                    {for note in notes:
                        <li class="flex items-center justify-between rounded-lg border border-gray-100 bg-gray-50 px-4 py-2 text-sm text-gray-700">
                            <span>{note["content"]}</span>
                            <span class="text-xs text-gray-400">#{note["id"]}</span>
                        </li>
                    }
                </ul>
            </section>

            {/* Background tasks */}
            <section class="mb-10 rounded-2xl border border-gray-200 bg-white p-8 shadow-sm">
                <h2 class="mb-4 text-xl font-bold text-gray-900">Background Tasks</h2>
                <p class="mb-4 text-sm text-gray-500">Enqueued via <code class="rounded bg-gray-100 px-1.5 py-0.5 font-mono text-xs">nextpy.enqueue</code> — the request returns instantly.</p>
                <button onclick={lambda e: callServerAction("run_background_demo", {"item": "report-" + str(count)})} class={btn_cls}>
                    Run background task
                </button>
                <ul class="mt-4 space-y-2">
                    {for line in taskLog:
                        <li class="rounded-lg border border-gray-100 bg-gray-50 px-4 py-2 font-mono text-xs text-gray-600">{line}</li>
                    }
                </ul>
            </section>

            {/* Local state + animations */}
            <section class="mb-10 rounded-2xl border border-gray-200 bg-white p-8 shadow-sm">
                <h2 class="mb-4 text-xl font-bold text-gray-900">State & Animations</h2>
                <div class="flex items-center gap-6">
                    <button onclick={lambda e: setCount(count + 1)} class={btn_cls}>
                        Count: {count}
                    </button>
                    <button onclick={lambda e: setPanelOpen(not panelOpen)} class={btn_cls + " bg-gray-700 hover:bg-gray-800"}>
                        {"Close panel" if panelOpen else "Open panel"}
                    </button>
                </div>
                <Motion
                    initial={{"opacity": 0, "transform": "translateY(20px) scale(0.95)"}}
                    animate={{"opacity": 1, "transform": "translateY(0px) scale(1)"}}
                    transition={{"duration": 0.4, "easing": "ease-out"}}
                    className="mt-6 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 p-6 text-white"
                >
                    <p class="font-semibold">This card animated in with the Web Animations API.</p>
                </Motion>
                <AnimatePresence>
                    {if panelOpen:
                        <Motion
                            initial={{"opacity": 0, "transform": "scale(0.9)"}}
                            animate={{"opacity": 1, "transform": "scale(1)"}}
                            exit={{"opacity": 0, "transform": "scale(0.9) translateY(-8px)"}}
                            transition={{"duration": 0.3}}
                            className="mt-4 rounded-xl border border-emerald-200 bg-emerald-50 p-6 text-emerald-800"
                        >
                            <p class="font-semibold">AnimatePresence exit animation</p>
                            <p class="mt-1 text-sm">Closing the panel plays the exit animation before removal.</p>
                        </Motion>
                    }
                </AnimatePresence>
            </section>

            {/* Refs */}
            <section class="rounded-2xl border border-gray-200 bg-white p-8 shadow-sm">
                <h2 class="mb-4 text-xl font-bold text-gray-900">Refs</h2>
                <div ref="showcase_card" class="mb-4 rounded-xl border-2 border-dashed border-indigo-300 p-6 text-center text-indigo-500">
                    <code class="font-mono text-sm">ref="showcase_card"</code>
                </div>
                <button onclick={check_ref} class={btn_cls}>Check ref ({refStatus})</button>
            </section>
        </div>
    )


default = Showcase
''')
    click.echo("  Created: pages/showcase.py")

    (project_dir / "pages" / "catalog.py").write_text('''"""Static catalog page — getStaticProps / ISR revalidation demo."""

from nextpy import get_static_props
from nextpy.core.data_fetching import PropsResult
from nextpy.psx import component

ITEMS = [
    {"id": "astro", "name": "Astro Lamp", "price": 49.0},
    {"id": "nova", "name": "Nova Chair", "price": 199.0},
    {"id": "comet", "name": "Comet Desk", "price": 349.0},
]


@component
def Catalog(props=None):
    props = props or {}
    items = props.get("items", [])

    return (
        <div class="mx-auto max-w-4xl px-4 py-16">
            <h1 class="mb-2 text-4xl font-extrabold text-gray-900">Catalog</h1>
            <p class="mb-10 text-gray-500">Rendered at build time with <code class="rounded bg-gray-100 px-1.5 py-0.5 font-mono text-sm">getStaticProps</code> + ISR.</p>
            <div class="grid gap-6 sm:grid-cols-3">
                {for item in items:
                    <a href="/catalog/{item['id']}" class="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm transition hover:shadow-lg">
                        <h2 class="text-lg font-bold text-gray-900">{item["name"]}</h2>
                        <p class="mt-2 text-indigo-600 font-semibold">${item["price"]}</p>
                    </a>
                }
            </div>
        </div>
    )


@get_static_props
async def getStaticProps(context):
    # Revalidate every 60s — stale pages are served while a fresh copy
    # is generated in the background (Incremental Static Regeneration).
    return PropsResult(props={"items": ITEMS}, revalidate=60)


default = Catalog
''')
    click.echo("  Created: pages/catalog.py")

    (project_dir / "pages" / "catalog").mkdir(exist_ok=True)
    (project_dir / "pages" / "catalog" / "[item].py").write_text('''"""Dynamic SSG page — getStaticPaths + getStaticProps demo.

Every item in ITEMS is pre-rendered at build time; unknown ids 404.
"""

from nextpy import get_static_paths, get_static_props
from nextpy.core.data_fetching import PropsResult, StaticPathsResult
from nextpy.psx import component

ITEMS = {
    "astro": {"id": "astro", "name": "Astro Lamp", "price": 49.0, "description": "A warm lamp for late-night stargazing sessions."},
    "nova": {"id": "nova", "name": "Nova Chair", "price": 199.0, "description": "Sculptural seating with a galaxy-grade finish."},
    "comet": {"id": "comet", "name": "Comet Desk", "price": 349.0, "description": "A floating desk that tracks your orbit."},
}


@component
def CatalogItem(props=None):
    props = props or {}
    item = props.get("item")

    if not item:
        return (
            <div class="flex min-h-[50vh] items-center justify-center">
                <div class="text-center">
                    <h1 class="text-3xl font-bold text-gray-900">Item not found</h1>
                    <a href="/catalog" class="mt-4 inline-block text-indigo-600 hover:underline">Back to catalog</a>
                </div>
            </div>
        )

    return (
        <div class="mx-auto max-w-2xl px-4 py-16">
            <a href="/catalog" class="text-sm font-medium text-indigo-600 hover:underline">&larr; All items</a>
            <h1 class="mt-4 text-4xl font-extrabold text-gray-900">{item["name"]}</h1>
            <p class="mt-2 text-2xl font-semibold text-indigo-600">${item["price"]}</p>
            <p class="mt-6 text-lg text-gray-600">{item["description"]}</p>
            <div class="mt-8 rounded-xl bg-gray-50 p-4 font-mono text-xs text-gray-500">
                Pre-rendered by getStaticPaths + getStaticProps at build time
            </div>
        </div>
    )


@get_static_paths
async def getStaticPaths():
    return StaticPathsResult(
        paths=[{"params": {"item": item_id}} for item_id in ITEMS.keys()],
        fallback=False,
    )


@get_static_props
async def getStaticProps(context):
    item_id = context.get("params", {}).get("item", "")
    item = ITEMS.get(item_id)
    if item is None:
        return PropsResult(not_found=True)
    return PropsResult(props={"item": item})


default = CatalogItem
''')
    click.echo("  Created: pages/catalog/[item].py")

    (project_dir / "pages" / "live.py").write_text('''"""Real-time demo — WebSocket pub/sub through ``nextpy.websocket.manager``.

The page subscribes to the ``demo`` channel; the "Broadcast" button runs
the ``broadcast_demo`` server action which publishes to every connected
client.  Open this page in two tabs to see live fan-out.  The socket
client lives in ``public/js/live-feed.js``.
"""

from nextpy.psx import component, interactive_component, useState, callServerAction


@interactive_component
def LivePage(props=None):
    [_server_result, _setServerResult] = useState(None)
    [_server_loading, _setServerLoading] = useState(False)

    def broadcast():
        callServerAction("broadcast_demo", {"message": "Live update from NextPy!"})

    return (
        <div class="mx-auto max-w-2xl px-4 py-16">
            <h1 class="mb-2 text-4xl font-extrabold text-gray-900">Live Feed</h1>
            <p class="mb-8 text-gray-500">
                Server actions publish to the <code class="rounded bg-gray-100 px-1.5 py-0.5 font-mono text-sm">demo</code> channel;
                this page subscribes over the <code class="rounded bg-gray-100 px-1.5 py-0.5 font-mono text-sm">/ws</code> WebSocket.
            </p>

            <button onclick={broadcast} disabled={_server_loading}
                class="mb-8 rounded-xl bg-indigo-600 px-6 py-3 font-semibold text-white transition hover:bg-indigo-700 disabled:opacity-60">
                {"Broadcasting..." if _server_loading else "Broadcast to all clients"}
            </button>

            <div id="live-feed" class="space-y-2">
                <div class="rounded-lg border border-dashed border-gray-300 p-4 text-center text-sm text-gray-400">
                    Waiting for events...
                </div>
            </div>

            <script src="/js/live-feed.js"></script>
        </div>
    )


default = LivePage
''')
    click.echo("  Created: pages/live.py")

    (project_dir / "public" / "js").mkdir(parents=True, exist_ok=True)
    (project_dir / "public" / "js" / "live-feed.js").write_text('''/* NextPy live-feed client — subscribes to the "demo" WebSocket channel
   and appends DEMO_EVENT payloads to #live-feed. Plain browser JS so it
   works without any framework hydration. */
(function () {
    var feed = document.getElementById('live-feed');
    if (!feed) return;

    var protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    var socket;
    var retryDelay = 1000;

    function addEvent(ev) {
        var first = feed.querySelector('.border-dashed');
        if (first) first.remove();
        var row = document.createElement('div');
        row.className = 'rounded-lg border border-indigo-100 bg-indigo-50 px-4 py-3 text-sm text-indigo-900';
        var msg = (ev && ev.payload && ev.payload.message) || JSON.stringify(ev);
        var ts = ev && ev.payload && ev.payload.timestamp
            ? new Date(ev.payload.timestamp * 1000).toLocaleTimeString()
            : '';
        row.innerHTML = '<span class="font-medium">' + msg + '</span>' +
            (ts ? ' <span class="ml-2 text-xs text-indigo-400">' + ts + '</span>' : '');
        feed.prepend(row);
        while (feed.children.length > 50) feed.removeChild(feed.lastChild);
    }

    function connect() {
        socket = new WebSocket(protocol + '//' + window.location.host + '/ws');
        socket.addEventListener('open', function () {
            retryDelay = 1000;
            socket.send(JSON.stringify({ type: 'subscribe', channel: 'demo' }));
        });
        socket.addEventListener('close', function () {
            setTimeout(connect, retryDelay);
            retryDelay = Math.min(retryDelay * 2, 30000);
        });
        socket.addEventListener('message', function (event) {
            try {
                var msg = JSON.parse(event.data);
                if (msg && msg.type === 'DEMO_EVENT') addEvent(msg);
            } catch (e) { /* ignore malformed frames */ }
        });
    }

    connect();
})();
''')
    click.echo("  Created: public/js/live-feed.js")


def _create_additional_pages(project_dir: Path):
    """Create additional pages: features, contact, sitemap, robots.txt, layout"""
    click.echo("  Creating additional pages...")

    # Create layout file
    (project_dir / "pages" / "layout.psx").write_text('''from nextpy.psx import component
"""App Layout"""

@component
def Layout(children, **props):
    return (
        <html>
            <head>
                <title>{props.get('title', 'My App')}</title>
                <link href="/tailwind.css" rel="stylesheet">
            </head>
            <body class="bg-gray-50">
                <nav class="bg-white shadow-sm">
                    <div class="container px-4 py-4 mx-auto">
                        <div class="flex items-center justify-between">
                            <a href="/" class="text-2xl font-bold text-gray-900">NextPy</a>
                            <div class="space-x-4">
                                <a href="/" class="text-gray-600 hover:text-gray-900">Home</a>
                                <a href="/features" class="text-gray-600 hover:text-gray-900">Features</a>
                                <a href="/examples" class="text-gray-600 hover:text-gray-900">Examples</a>
                                <a href="/about" class="text-gray-600 hover:text-gray-900">About</a>
                                <a href="/contact" class="text-gray-600 hover:text-gray-900">Contact</a>
                            </div>
                        </div>
                    </div>
                </nav>
                <main class="min-h-screen">
                    {children}
                </main>
                <footer class="py-8 mt-16 bg-white border-t">
                    <div class="container px-4 mx-auto text-center text-gray-600">
                        <p>&copy; 2024 NextPy. Built with Python.</p>
                    </div>
                </footer>
            </body>
        </html>
    )
''')
    click.echo("  Created: pages/layout.psx")

    # Features page
    (project_dir / "pages" / "features.py").write_text('''"""Features showcase page"""

from nextpy.psx import component

@component
def Features(props=None):
    props = props or {}
    features = [
        {
            "icon": "page",
            "title": "File-Based Routing",
            "description": "Create pages by adding Python files to pages/",
            "link": "/documentation"
        },
        {
            "icon": "rocket",
            "title": "Server-Side Rendering",
            "description": "Render pages on the server with get_server_side_props",
            "link": "/documentation"
        },
        {
            "icon": "lightning",
            "title": "Static Generation",
            "description": "Pre-render pages at build time with get_static_props",
            "link": "/documentation"
        },
        {
            "icon": "database",
            "title": "Database Integration",
            "description": "SQLAlchemy ORM with SQLite, PostgreSQL, MySQL",
            "link": "/db_example"
        },
        {
            "icon": "wrench",
            "title": "API Routes",
            "description": "Create REST APIs with FastAPI in pages/api/",
            "link": "/api/hello"
        },
        {
            "icon": "palette",
            "title": "Components",
            "description": "20+ pre-built UI components",
            "link": "/examples"
        },
        {
            "icon": "fire",
            "title": "Live Reload",
            "description": "Instant updates during development",
            "link": "/documentation"
        },
        {
            "icon": "shield",
            "title": "Authentication",
            "description": "Built-in auth with cookie sessions",
            "link": "/login"
        }
    ]

    return (
        <div class="min-h-screen py-8 bg-gray-50">
            <div class="container px-4 mx-auto">
                <div class="max-w-6xl mx-auto">
                    <h1 class="mb-12 text-4xl font-bold text-center">Features</h1>
                    <div class="grid gap-8 sm:grid-cols-2 lg:grid-cols-3">
                        {for feature in features:
                            <a href={feature["link"]} class="block p-6 bg-white rounded-lg shadow-lg transition-shadow hover:shadow-xl">
                                <div class="flex items-center mb-4">
                                    <span class="text-2xl">{feature["icon"]}</span>
                                    <h3 class="ml-3 text-xl font-semibold">{feature["title"]}</h3>
                                </div>
                                <p class="text-gray-600">{feature["description"]}</p>
                            </a>
                        }
                    </div>
                </div>
            </div>
        </div>
    )

def getServerSideProps(context):
    return {"props": {"title": "Features"}}

default = Features
''')
    click.echo("  Created: pages/features.py")

    # Contact page
    (project_dir / "pages" / "contact.py").write_text('''"""Contact page with form"""

from nextpy.psx import component

@component
def Contact(props=None):
    props = props or {}
    title = props.get("title", "Contact Us")
    description = props.get("description", "Get in touch with NextPy team")

    return (
        <div class="min-h-screen py-8 bg-gray-50">
            <div class="container px-4 mx-auto">
                <div class="max-w-2xl mx-auto text-center">
                    <h1 class="mb-4 text-4xl font-bold">{title}</h1>
                    <p class="mb-8 text-xl text-gray-600">{description}</p>
                    <form class="space-y-6">
                        <div>
                            <label class="block mb-2 text-sm font-medium text-gray-700">Name</label>
                            <input type="text" name="name" class="w-full px-4 py-2 border rounded-lg" required />
                        </div>
                        <div>
                            <label class="block mb-2 text-sm font-medium text-gray-700">Email</label>
                            <input type="email" name="email" class="w-full px-4 py-2 border rounded-lg" required />
                        </div>
                        <div>
                            <label class="block mb-2 text-sm font-medium text-gray-700">Message</label>
                            <textarea name="message" rows="4" class="w-full px-4 py-2 border rounded-lg" required></textarea>
                        </div>
                        <button type="submit" class="w-full px-6 py-3 font-semibold text-white bg-blue-600 rounded-lg hover:bg-blue-700">
                            Send Message
                        </button>
                    </form>
                </div>
            </div>
        </div>
    )

def getServerSideProps(context):
    return {
        "props": {
            "title": "Contact Us",
            "description": "Get in touch with NextPy team"
        }
    }

default = Contact
''')
    click.echo("  Created: pages/contact.py")

    # Sitemap XML page
    (project_dir / "pages" / "sitemap.xml.py").write_text('''"""Sitemap page for SEO"""

def get_template():
    return "sitemap.xml"

async def get_server_side_props(context):
    """Generate sitemap with all important pages"""
    import os
    from datetime import datetime
    from fastapi.responses import Response

    base_url = os.getenv("FRONTEND_URL", "http://localhost:8000")

    pages = [
        {"loc": f"{base_url}/", "lastmod": datetime.now().strftime("%Y-%m-%d"), "changefreq": "daily", "priority": "1.0"},
        {"loc": f"{base_url}/documentation", "lastmod": datetime.now().strftime("%Y-%m-%d"), "changefreq": "weekly", "priority": "0.9"},
        {"loc": f"{base_url}/examples", "lastmod": datetime.now().strftime("%Y-%m-%d"), "changefreq": "weekly", "priority": "0.8"},
        {"loc": f"{base_url}/features", "lastmod": datetime.now().strftime("%Y-%m-%d"), "changefreq": "weekly", "priority": "0.8"},
        {"loc": f"{base_url}/about", "lastmod": datetime.now().strftime("%Y-%m-%d"), "changefreq": "monthly", "priority": "0.7"},
        {"loc": f"{base_url}/blog", "lastmod": datetime.now().strftime("%Y-%m-%d"), "changefreq": "weekly", "priority": "0.7"},
        {"loc": f"{base_url}/contact", "lastmod": datetime.now().strftime("%Y-%m-%d"), "changefreq": "monthly", "priority": "0.6"},
    ]

    xml = '<?xml version="1.0" encoding="UTF-8"?>\\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\\n'

    for page in pages:
        xml += f"""  <url>
    <loc>{page['loc']}</loc>
    <lastmod>{page['lastmod']}</lastmod>
    <changefreq>{page['changefreq']}</changefreq>
    <priority>{page['priority']}</priority>
  </url>
"""

    xml += '\\n</urlset>'

    return Response(content=xml, media_type="application/xml")
''')
    click.echo("  Created: pages/sitemap.xml.py")

    # Robots.txt page
    (project_dir / "pages" / "robots.txt.py").write_text('''"""Robots.txt page for SEO"""

def get_template():
    return "robots.txt"

async def get_server_side_props(context):
    """Generate robots.txt"""
    import os
    from fastapi.responses import Response

    base_url = os.getenv("FRONTEND_URL", "http://localhost:8000")

    robots_content = f"""User-agent: *
Allow: /

# Block common non-content or sensitive paths
Disallow: /api/
Disallow: /_nextpy_debug/
Disallow: /static/
Disallow: *.py$
Disallow: *.html$

# Sitemap location
Sitemap: {base_url}/sitemap.xml
"""

    return Response(content=robots_content, media_type="text/plain")
''')
    click.echo("  Created: pages/robots.txt.py")


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
