#!/usr/bin/env python3
"""Complete NextPy Project Setup - Ensure all files and configurations are correct"""

import os
import sys
import subprocess
from pathlib import Path

def setup_complete_project():
    """Setup a complete NextPy project with all required files and configurations"""
    
    print("🚀 Setting up Complete NextPy Project...")
    
    project_root = Path.cwd()
    
    # 1. Ensure all directories exist
    print("\n📁 Creating project structure...")
    directories = [
        "pages",
        "pages/api", 
        "components",
        "components/ui",
        "components/layout",
        "templates",
        "public",
        "public/css",
        "public/js",
        "public/images",
        "styles",
        ".vscode"
    ]
    
    for dir_name in directories:
        dir_path = project_root / dir_name
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"  ✅ {dir_name}/")
    
    # 2. Create updated main.py with correct Tailwind compilation
    print("\n📄 Creating main.py...")
    main_py_content = '''"""
NextPy Application Entry Point
Complete NextPy application with True JSX and Tailwind CSS
"""

import sys
from pathlib import Path
import subprocess

print(f"DEBUG: Current working directory: {Path.cwd()}")
print(f"DEBUG: sys.path before modification: {sys.path}")

# Add framework to path
sys.path.insert(0, str(Path(__file__).parent / ".nextpy_framework"))

print(f"DEBUG: sys.path after modification: {sys.path}")

# Compile Tailwind CSS using PostCSS
try:
    print("Compiling Tailwind CSS...")
    # Use PostCSS with the new Tailwind plugin
    result = subprocess.run(
        ["./node_modules/.bin/postcss", "styles.css", "-o", "public/tailwind.css"], 
        capture_output=True, 
        text=True,
        check=True
    )
    print("Tailwind CSS compiled successfully.")
    if result.stdout:
        print(f"CSS Output: {result.stdout[:200]}...")
except subprocess.CalledProcessError as e:
    print(f"Error compiling Tailwind CSS: {e}")
    if e.stderr:
        print(f"CSS Error: {e.stderr}")
except FileNotFoundError:
    print("Error: PostCSS not found. Make sure Node.js and Tailwind CSS are installed.")
    print("Install with: npm install postcss-cli @tailwindcss/postcss")

from nextpy.server.app import create_app
from nextpy.db import init_db
from nextpy.config import settings

# Initialize database
try:
    init_db(settings.database_url)
    print("Database initialized successfully.")
except Exception as e:
    print(f"Warning: Database initialization failed: {e}")

# Create NextPy app
app = create_app(
    pages_dir="pages",
    templates_dir="templates", 
    public_dir="public",
    out_dir="out",
    debug=settings.debug,
)

# Add health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "framework": "NextPy"}

# Root endpoint
@app.get("/")
async def root():
    return {"message": "NextPy is running!", "docs": "/docs"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
'''
    
    (project_root / "main.py").write_text(main_py_content)
    print("  ✅ main.py (updated with PostCSS)")
    
    # 3. Ensure styles.css exists
    print("\n🎨 Creating styles.css...")
    styles_css_content = '''/* NextPy Styles */
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Custom styles */
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
}

.debug-icon {
    position: fixed;
    bottom: 20px;
    right: 20px;
    background: #3b82f6;
    color: white;
    padding: 8px 12px;
    border-radius: 8px;
    font-size: 12px;
    font-weight: bold;
    z-index: 9999;
    cursor: pointer;
    transition: all 0.3s ease;
}

.debug-icon:hover {
    background: #2563eb;
    transform: scale(1.05);
}
'''
    
    (project_root / "styles.css").write_text(styles_css_content)
    print("  ✅ styles.css")
    
    # 4. Create comprehensive requirements.txt
    print("\n📦 Creating requirements.txt...")
    requirements_content = '''# NextPy Framework Requirements
fastapi>=0.100.0
uvicorn>=0.23.0
jinja2>=3.1.0
pydantic>=2.0.0
pydantic-settings>=2.0.0
click>=8.1.0
watchdog>=3.0.0
python-multipart>=0.0.6
pillow>=10.0.0
aiofiles>=23.0.0
httpx>=0.24.0
sqlalchemy>=2.0.0
python-dotenv>=1.0.0
pyjwt>=2.8.0
markdown>=3.0.0
'''
    
    (project_root / "requirements.txt").write_text(requirements_content)
    print("  ✅ requirements.txt")
    
    # 5. Create .env file
    print("\n🔧 Creating .env...")
    env_content = '''# NextPy Development Environment
DEVELOPMENT=true
DEBUG=true
NEXTPY_DEBUG=true

# Server Configuration
HOST=0.0.0.0
PORT=5000

# Database (if needed)
DATABASE_URL=sqlite:///./app.db

# Secret Key
SECRET_KEY=your-secret-key-here

# NextPy Settings
NEXTPY_DEBUG_ICON=true
NEXTPY_HOT_RELOAD=true
NEXTPY_LOG_LEVEL=info
'''
    
    (project_root / ".env").write_text(env_content)
    print("  ✅ .env")
    
    # 6. Create sample pages
    print("\n📄 Creating sample pages...")
    
    # Index page
    index_page = '''"""Homepage with True JSX and Tailwind CSS"""

def Home(props=None):
    """Homepage component"""
    props = props or {}
    title = props.get("title", "Welcome to NextPy")
    message = props.get("message", "Your Python-powered web framework with True JSX")
    
    return (
        <div class="flex items-center justify-center min-h-screen bg-gradient-to-br from-blue-500 to-purple-600">
            <div class="text-center text-white">
                <h1 class="mb-4 text-5xl font-bold">{title}</h1>
                <p class="text-xl mb-8">{message}</p>
                <div class="space-x-4">
                    <a href="/about" class="inline-block px-6 py-3 font-semibold text-blue-600 transition-all duration-300 transform bg-white rounded-lg shadow-lg hover:bg-gray-100 hover:text-blue-700 hover:scale-105">
                        Learn More
                    </a>
                    <a href="/tailwind_test" class="inline-block px-6 py-3 ml-4 font-semibold text-green-600 transition-all duration-300 transform bg-white rounded-lg shadow-lg hover:bg-gray-100 hover:text-green-700 hover:scale-105">
                        Tailwind Test
                    </a>
                </div>
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
'''
    
    (project_root / "pages" / "index.py").write_text(index_page)
    print("  ✅ pages/index.py")
    
    # About page
    about_page = '''"""About page with True JSX"""

def About(props=None):
    """About page component"""
    props = props or {}
    
    title = props.get("title", "About NextPy")
    description = props.get("description", "Learn about NextPy framework")
    
    return (
        <div class="max-w-4xl px-4 py-12 mx-auto">
            <h1 class="mb-6 text-4xl font-bold text-gray-900">{title}</h1>
            <p class="mb-4 text-lg text-gray-600">{description}</p>
            <div class="bg-white p-6 rounded-lg shadow-lg">
                <h2 class="mb-4 text-2xl font-semibold text-blue-600">Features</h2>
                <ul class="space-y-2 text-gray-700">
                    <li class="flex items-center"><span class="mr-2">✅</span> True JSX in Python</li>
                    <li class="flex items-center"><span class="mr-2">✅</span> File-based routing</li>
                    <li class="flex items-center"><span class="mr-2">✅</span> Server-side rendering</li>
                    <li class="flex items-center"><span class="mr-2">✅</span> Tailwind CSS integration</li>
                    <li class="flex items-center"><span class="mr-2">✅</span> Hot reload development</li>
                    <li class="flex items-center"><span class="mr-2">✅</span> Plugin system</li>
                </ul>
            </div>
            <div class="mt-8 text-center">
                <a href="/" class="text-blue-600 hover:text-blue-800 font-medium">
                    ← Back to Home
                </a>
            </div>
        </div>
    )

def getServerSideProps(context):
    return {
        "props": {
            "title": "About NextPy",
            "description": "Learn about NextPy framework"
        }
    }

default = About
'''
    
    (project_root / "pages" / "about.py").write_text(about_page)
    print("  ✅ pages/about.py")
    
    # 7. Install missing dependencies
    print("\n📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "--break-system-packages", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print("  ✅ Dependencies installed")
    except subprocess.CalledProcessError as e:
        print(f"  ⚠️  Some dependencies may have failed: {e}")
    
    # 8. Install Node.js dependencies if needed
    print("\n📦 Checking Node.js dependencies...")
    if not (project_root / "node_modules").exists():
        try:
            subprocess.run(["npm", "install"], check=True, capture_output=True)
            print("  ✅ Node.js dependencies installed")
        except subprocess.CalledProcessError:
            print("  ⚠️  npm install failed - run manually")
    else:
        print("  ✅ Node.js dependencies already installed")
    
    print("\n🎉 NextPy project setup complete!")
    print("\n🚀 Next steps:")
    print("  1️⃣  Run: nextpy dev")
    print("  2️⃣  Open: http://localhost:5000")
    print("  3️⃣  Start building with True JSX + Tailwind CSS!")
    
    print("\n✨ Your NextPy app is ready for development!")

if __name__ == "__main__":
    setup_complete_project()
