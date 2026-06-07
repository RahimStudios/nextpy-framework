"""NextPy ASGI Application Entry Point"""

import os
import sys
import subprocess
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / ".nextpy_framework"))
try:
    print("Info: Compiling Tailwind CSS...")
    proj_root = Path.cwd()
    framework_dir = Path(__file__).parent
    # If the project root doesn't have a styles.css yet, warn the user and create a minimal one.
    styles_file = proj_root / "styles" / "styles.css"
    if not styles_file.exists():
        print("Warning: styles.css not found, creating a minimal file.")
        styles_file.write_text("@tailwind base;\n"
                            "@tailwind components;\n"
                            "@tailwind utilities;\n"
                            "/* Add your custom styles here */\n")

    import shutil
    npm_bin = shutil.which("npm")
    if not npm_bin:
        raise FileNotFoundError("npm not found on PATH")

    lockfile = proj_root / "package-lock.json"
    node_modules = proj_root / "node_modules"
    if not node_modules.exists():
        if lockfile.exists():
            subprocess.run([npm_bin, "ci"], cwd=str(proj_root), check=True)
        else:
            subprocess.run([npm_bin, "install"], cwd=str(proj_root), check=True)

    subprocess.run([npm_bin, "run", "build:tailwind"], cwd=str(proj_root), check=True)
    print("Tailwind CSS compiled successfully.")
except subprocess.CalledProcessError as e:
    print(f"Error compiling Tailwind CSS: {e}")
    print("You can also run `cd .nextpy_framework/nextpy && npm ci && npm run build:tailwind` manually.")
except FileNotFoundError:
    print("Error: npm not found. Make sure Node.js is installed and available on PATH.")
    print("See https://nodejs.org/ for installation instructions.")

# Import NextPy modules (works when installed via pip)
from nextpy.server.app import create_app
from nextpy.db import init_db
from nextpy.config import settings

# Initialize database
try:
    init_db(settings["database_url"])
    print("Database initialized successfully.")
except Exception as e:
    print(f"Warning: Database initialization failed: {e}")

# Create NextPy app with file-based routing
app = create_app(
    pages_dir="pages",
    templates_dir="templates", 
    public_dir="public",
    out_dir="out",
    debug=settings["debug"],
)

# Note: Routes are automatically loaded from pages/ directory
# - / -> pages/index.py
# - /about -> pages/about.py  
# - /api/* -> pages/api/*.py

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

