"""
NextPy Application Entry Point
This is the main file that runs the NextPy server
"""

import sys
from pathlib import Path
import subprocess



# Add framework to path
sys.path.insert(0, str(Path(__file__).parent / ".nextpy_framework"))



# Compile Tailwind CSS using framework's npm script; this keeps paths consistent regardless
# of where the user runs the server from.
proj_root = Path.cwd()
framework_dir = Path(__file__).parent

try:
    print("Compiling Tailwind CSS...")
    # If the project root doesn't have a styles.css yet, warn the user and create a minimal one.
    styles_file = proj_root / "styles.css"
    if not styles_file.exists():
        print("Warning: styles.css not found in project root, creating a default file.")
        styles_file.write_text("@tailwind base;\n@tailwind components;\n@tailwind utilities;\n")

    import shutil

    npm_bin = shutil.which("npm")
    if not npm_bin:
        raise FileNotFoundError("npm not found on PATH")

    # Ensure node deps are present. Prefer `npm ci` when a lockfile exists.
    lockfile = framework_dir / "package-lock.json"
    node_modules = framework_dir / "node_modules"
    try:
        if not node_modules.exists():
            if lockfile.exists():
                subprocess.run([npm_bin, "ci"], cwd=str(framework_dir), check=True)
            else:
                subprocess.run([npm_bin, "install"], cwd=str(framework_dir), check=True)

        # Run the build script defined in the vendored framework's package.json
        subprocess.run([npm_bin, "run", "build:tailwind"], cwd=str(framework_dir), check=True)
        print("Tailwind CSS compiled successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error compiling Tailwind CSS: {e}")
        print("You can try running `cd .nextpy_framework/nextpy && npm ci && npm run build:tailwind` manually.")
except subprocess.CalledProcessError as e:
    print(f"Error compiling Tailwind CSS: {e}")
    print("You can try running `cd .nextpy_framework/nextpy && npm ci && npm run build:tailwind` manually.")
except FileNotFoundError:
    print("Error: npm not found. Make sure Node.js is installed and available on PATH.")
    print("See https://nodejs.org/ for installation instructions.")


from nextpy.server.app import create_app
from nextpy.db import init_db
from nextpy.config import settings

# Initialize database
try:
    init_db(settings["database_url"])
except Exception as e:
    print(f"Warning: Database initialization failed: {e}")

app = create_app(
    pages_dir="pages",
    templates_dir="templates",
    public_dir="public",
    out_dir="out",
    
)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app', host="0.0.0.0", port=8000)
