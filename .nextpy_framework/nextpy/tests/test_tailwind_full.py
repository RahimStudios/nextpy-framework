#!/usr/bin/env python3
"""Test full Tailwind CSS integration including CSS processing"""

import sys
import os
import subprocess
from pathlib import Path

# Add the framework to path
sys.path.insert(0, str(Path(__file__).parent / ".nextpy_framework"))

def test_tailwind_css_processing():
    """Test Tailwind CSS compilation and processing"""
    
    print("🧪 Testing Full Tailwind CSS Integration...")
    
    # Check if Tailwind CSS is installed
    try:
        result = subprocess.run(['npm', 'list', 'tailwindcss'], 
                          capture_output=True, text=True, cwd=Path(__file__).parent)
        if result.returncode == 0:
            print("✅ Tailwind CSS is installed via npm")
        else:
            print("❌ Tailwind CSS not found via npm")
    except FileNotFoundError:
        print("⚠️  npm not found, checking for local CSS files...")
    
    # Check for Tailwind CSS files
    tailwind_files = [
        "node_modules/tailwindcss/index.css",
        "styles.css",
        "tailwind.config.js",
        "postcss.config.js"
    ]
    
    print("\n📁 Checking Tailwind CSS files:")
    for file_path in tailwind_files:
        full_path = Path(file_path)
        if full_path.exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
    
    # Test CSS content
    styles_css = Path("styles.css")
    if styles_css.exists():
        print("\n📝 styles.css content:")
        with open(styles_css, 'r') as f:
            content = f.read()
            print(content)
        
        # Check for Tailwind directives
        if "@tailwind" in content:
            print("✅ Tailwind directives found")
        else:
            print("❌ Tailwind directives missing")
    
    # Test Tailwind config
    tailwind_config = Path("tailwind.config.js")
    if tailwind_config.exists():
        print("\n📝 tailwind.config.js content:")
        with open(tailwind_config, 'r') as f:
            content = f.read()
            print(content)
        
        # Check for Python file patterns
        if ".py" in content:
            print("✅ Python files included in Tailwind config")
        else:
            print("⚠️  Python files might not be included")
    
    # Test PostCSS config
    postcss_config = Path("postcss.config.js")
    if postcss_config.exists():
        print("\n📝 postcss.config.js content:")
        with open(postcss_config, 'r') as f:
            content = f.read()
            print(content)
        
        # Check for Tailwind plugin
        if "tailwindcss" in content:
            print("✅ Tailwind CSS plugin configured in PostCSS")
        else:
            print("❌ Tailwind CSS plugin missing from PostCSS")
    
    # Test CSS compilation
    print("\n🔧 Testing CSS compilation...")
    try:
        # Try to compile CSS using PostCSS
        result = subprocess.run([
            'npx', 'postcss', 'styles.css', '-o', 'output.css'
        ], capture_output=True, text=True, cwd=Path(__file__).parent)
        
        if result.returncode == 0:
            print("✅ CSS compilation successful")
            
            # Check output file
            output_css = Path("output.css")
            if output_css.exists():
                with open(output_css, 'r') as f:
                    compiled_content = f.read()
                
                # Check for Tailwind utility classes
                utility_classes = [
                    '.flex', '.items-center', '.justify-center',
                    '.text-center', '.text-white', '.bg-blue-500',
                    '.px-6', '.py-3', '.rounded-lg'
                ]
                
                found_classes = []
                for cls in utility_classes:
                    if cls in compiled_content:
                        found_classes.append(cls)
                
                print(f"✅ Found {len(found_classes)} Tailwind utility classes")
                if len(found_classes) >= 5:
                    print("✅ Tailwind CSS is properly compiled")
                else:
                    print("⚠️  Some Tailwind classes missing")
                
                # Cleanup
                output_css.unlink()
            else:
                print("❌ Output CSS file not created")
        else:
            print(f"❌ CSS compilation failed: {result.stderr}")
    except FileNotFoundError:
        print("⚠️  PostCSS not available for testing")
    
    # Test plugin integration
    print("\n🔌 Testing Plugin Integration...")
    try:
        from nextpy.plugins.builtin import TailwindPlugin
        from nextpy.plugins.base import PluginContext
        
        # Create test content with various Tailwind classes
        test_jsx = '''
def HomePage(props=None):
    return (
        <div class="flex min-h-screen bg-gray-100">
            <div class="container mx-auto px-4 py-8">
                <h1 class="text-3xl font-bold text-gray-900 mb-4">
                    Tailwind CSS Test
                </h1>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div class="bg-white p-6 rounded-lg shadow-md">
                        <h2 class="text-xl font-semibold mb-2">Card 1</h2>
                        <p class="text-gray-600">Testing responsive design</p>
                    </div>
                    <div class="bg-white p-6 rounded-lg shadow-md">
                        <h2 class="text-xl font-semibold mb-2">Card 2</h2>
                        <p class="text-gray-600">Testing grid layout</p>
                    </div>
                </div>
            </div>
        </div>
    )
'''
        
        context = PluginContext(
            file_path=Path("test.py"),
            file_content=test_jsx,
            metadata={},
            config={},
            debug=True
        )
        
        tailwind_plugin = TailwindPlugin()
        result = tailwind_plugin.transform(context)
        
        if result.success:
            print("✅ Tailwind plugin integration working")
            print(f"📊 Metadata: {result.metadata}")
        else:
            print("❌ Tailwind plugin integration failed")
            print(f"Errors: {result.errors}")
            
    except Exception as e:
        print(f"❌ Plugin integration test failed: {e}")
    
    print("\n🎉 Full Tailwind CSS Integration Test Complete!")
    
    return True

if __name__ == "__main__":
    test_tailwind_css_processing()
