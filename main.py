"""
NextPy Application Entry Point
This is the main file that runs the NextPy server
"""

import sys
from pathlib import Path
import subprocess



# Add framework to path
sys.path.insert(0, str(Path(__file__).parent / ".nextpy_framework"))



# Compile Tailwind CSS before starting the application
proj_root = Path.cwd()
framework_dir = Path(__file__).parent

try:
    print("Compiling Tailwind CSS...")
    # Ensure styles.css exists in project root
    styles_file = proj_root / "styles" / "styles.css"
    if not styles_file.exists():
        print("Warning: styles/styles.css not found, creating a default file.")
        styles_file.parent.mkdir(parents=True, exist_ok=True)
        styles_file.write_text("@import \"tailwindcss\";\n")

    import shutil

    npm_bin = shutil.which("npm")
    if not npm_bin:
        print("Warning: npm not found on PATH. Skipping Tailwind compilation.")
        print("Install Node.js from https://nodejs.org/ to enable Tailwind CSS.")
    else:
        # Check if package.json exists in project root
        package_json = proj_root / "package.json"
        if package_json.exists():
            # Ensure node dependencies are installed
            node_modules = proj_root / "node_modules"
            if not node_modules.exists():
                print("Installing Node.js dependencies...")
                try:
                    lockfile = proj_root / "package-lock.json"
                    if lockfile.exists():
                        subprocess.run([npm_bin, "ci"], cwd=str(proj_root), check=True)
                    else:
                        subprocess.run([npm_bin, "install"], cwd=str(proj_root), check=True)
                except subprocess.CalledProcessError as e:
                    print(f"Warning: npm install failed: {e}")
                    print("You can try running 'npm install' manually.")

            # Run Tailwind CSS build using package.json script (pinned to v4.3.3)
            try:
                subprocess.run([npm_bin, "run", "build:tailwind"], cwd=str(proj_root), check=True)
                print("Tailwind CSS v4.3.3 compiled successfully.")
            except subprocess.CalledProcessError as e:
                print(f"Error compiling Tailwind CSS: {e}")
                print("You can try running 'npm run build:tailwind' manually.")
        else:
            print("Warning: package.json not found in project root. Skipping Tailwind compilation.")
            print("Create a package.json with Tailwind CSS dependencies to enable Tailwind.")

except Exception as e:
    print(f"Warning: Tailwind CSS compilation failed: {e}")
    print("The application will continue without Tailwind CSS.")


import nextpy as nx
from nextpy.admin import AdminSite
from nextpy.db import User, Post, Todo, Job, Application

# Import all server actions (triggers registration)
try:
    from pages.actions import *  # noqa: F401
except ImportError:
    pass  # No server actions yet

from pages.actions.todo_actions import create_todo, toggle_todo, delete_todo, get_todos, get_todo_stats  # noqa: F401
try:
    from pages.jobs.actions import (  # noqa: F401
        register, login, logout, get_me,
        create_job, update_job, delete_job, get_my_jobs, list_jobs,
        apply_to_job, get_my_applications, get_job_applications, update_application_status,
    )
except ImportError:
    pass  # No job actions yet
from pages.jobs.actions import (  # noqa: F401
    register, login, logout, get_me,
    create_job, update_job, delete_job, get_my_jobs, list_jobs,
    apply_to_job, get_my_applications, get_job_applications, update_application_status,
)

# Database must initialize before the app starts
from nextpy.db import init_db
from nextpy.config import settings
import os

# Get database URL from settings
db_url = settings["database_url"]

# Initialize database with error handling
try:
    init_db(db_url)
except Exception as e:
    print(f"⚠️  Database initialization failed: {e}")
    print("🔄 Using fallback database configuration...")
    # Try with a simple SQLite database
    try:
        init_db("sqlite:///./nextpy_fallback.db")
    except Exception as fallback_error:
        print(f"❌ Fallback database also failed: {fallback_error}")
        print("⚠️  Continuing without database - some features may not work")

admin_site = AdminSite()
admin_site.register(User)
admin_site.register(Post)
admin_site.register(Todo)
admin_site.register(Job)
admin_site.register(Application)

app = nx.create_app(
    pages_dir="pages",
    templates_dir="templates",
    public_dir="public",
    out_dir="out",
    debug=settings["debug"],
    admin_site=admin_site,
)




if __name__ == "__main__":
    import uvicorn
    # Serve this exact app instance so Uvicorn cannot import another main.py.
    uvicorn.run(app, host="0.0.0.0", port=5000)
