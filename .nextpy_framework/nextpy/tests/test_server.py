#!/usr/bin/env python3
"""Test the server routing with links"""

import sys
import os
from pathlib import Path

# Add the framework to path
sys.path.insert(0, str(Path(__file__).parent / ".nextpy_framework"))

from nextpy.server.app import NextPyApp

def test_server():
    """Test the server with links"""
    
    # Create a temporary pages directory
    pages_dir = Path("test_server_pages")
    pages_dir.mkdir(exist_ok=True)
    
    # Create index page with link
    (pages_dir / "index.py").write_text('''
def handler():
    return (
        <div>
            <h1>Home Page</h1>
            <p><a href="/about">Go to About Page</a></p>
            <p><a href="/contact">Go to Contact Page</a></p>
        </div>
    )
''')
    
    # Create about page
    (pages_dir / "about.py").write_text('''
def handler():
    return (
        <div>
            <h1>About Page</h1>
            <p>This is the about page.</p>
            <p><a href="/">Back to Home</a></p>
        </div>
    )
''')
    
    # Create contact page
    (pages_dir / "contact.py").write_text('''
def handler():
    return (
        <div>
            <h1>Contact Page</h1>
            <p>This is the contact page.</p>
            <p><a href="/">Back to Home</a></p>
        </div>
    )
''')
    
    print("🚀 Starting NextPy server...")
    print("📁 Pages directory:", pages_dir)
    print("🔗 Test these URLs:")
    print("   http://localhost:8000/")
    print("   http://localhost:8000/about") 
    print("   http://localhost:8000/contact")
    print()
    
    # Create and run the app
    app = NextPyApp(pages_dir=str(pages_dir), debug=True)
    
    try:
        import uvicorn
        uvicorn.run(app.app, host="0.0.0.0", port=8000, log_level="info")
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
    finally:
        # Cleanup
        import shutil
        shutil.rmtree(pages_dir)

if __name__ == "__main__":
    test_server()
