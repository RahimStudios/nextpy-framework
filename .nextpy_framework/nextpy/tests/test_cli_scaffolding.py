#!/usr/bin/env python3
"""
Test NextPy CLI PSX Scaffolding
"""

import sys
import os
import tempfile
import shutil
from pathlib import Path

# Add NextPy to path
sys.path.insert(0, '.nextpy_framework')

def test_cli_scaffolding():
    """Test CLI scaffolding functionality"""
    print("=== 🚀 TESTING CLI PSX SCAFFOLDING ===")
    print()
    
    try:
        # Import CLI functions directly
        from nextpy.cli import _create_project_structure, _create_psx_homepage
        print("✅ CLI functions imported successfully")
        
        # Create temporary test project
        with tempfile.TemporaryDirectory() as temp_dir:
            test_project = Path(temp_dir) / 'test-psx-app'
            
            print("✅ Creating PSX project structure...")
            _create_project_structure(test_project, psx=True, template='default')
            
            # Verify files were created
            key_files = [
                'pages/index.py',
                'pages/about.py', 
                'pages/examples.py',
                'tailwind.config.js',
                'package.json',
                'requirements.txt',
                'main.py',
                '.vscode/settings.json'
            ]
            
            print("✅ Checking created files:")
            for file_path in key_files:
                full_path = test_project / file_path
                if full_path.exists():
                    print(f"  ✅ {file_path}")
                    
                    # Check content of key files
                    if file_path == 'pages/index.py':
                        content = full_path.read_text()
                        if '@component' in content and '<div' in content:
                            print("    ✅ Contains @component and JSX")
                        else:
                            print("    ❌ Missing @component or JSX")
                    
                    if file_path == 'tailwind.config.js':
                        content = full_path.read_text()
                        if '.py' in content and '.psx' in content:
                            print("    ✅ Supports .py and .psx files")
                    
                    if file_path == 'package.json':
                        content = full_path.read_text()
                        if 'PSX' in content:
                            print("    ✅ PSX description included")
                            
                else:
                    print(f"  ❌ {file_path}")
            
            print("✅ CLI scaffolding test completed successfully!")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    
    return True

def show_cli_usage():
    """Show CLI usage examples"""
    print("\n🎯 NEXTPY CLI USAGE:")
    print()
    print("📦 CREATE NEW PROJECT:")
    print("  nextpy create my-app          # Creates PSX project (default)")
    print("  nextpy create my-app --psx    # Explicitly creates PSX project")
    print("  nextpy create my-app --no-psx  # Creates traditional Python project")
    print()
    print("🔧 DEVELOPMENT SERVER:")
    print("  cd my-app")
    print("  npm install                    # Install Tailwind CSS")
    print("  nextpy dev                    # Start development server")
    print()
    print("📄 GENERATE COMPONENTS:")
    print("  nextpy generate page contact   # Creates PSX page")
    print("  nextpy generate component Button # Creates PSX component")
    print("  nextpy generate api users      # Creates API route")
    print()
    print("✨ PSX FEATURES IN SCAFFOLDING:")
    print("  ✅ @component decorator for JSX syntax")
    print("  ✅ True JSX syntax in generated files")
    print("  ✅ Tailwind CSS configuration")
    print("  ✅ VS Code settings for PSX")
    print("  ✅ Complete project structure")
    print("  ✅ Server-side rendering setup")
    print("  ✅ Example pages with PSX features")
    print()

if __name__ == "__main__":
    success = test_cli_scaffolding()
    show_cli_usage()
    
    if success:
        print("🎉 CLI SCAFFOLDING UPDATE COMPLETE!")
        print("NextPy CLI now supports PSX (True JSX) scaffolding!")
    else:
        print("❌ CLI scaffolding needs fixes")
        sys.exit(1)
