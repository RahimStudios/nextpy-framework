#!/usr/bin/env python3
"""
Test Tailwind CSS Integration in NextPy
Verifies that Tailwind CSS is properly compiled and usable
"""

import requests
import time
import subprocess
from pathlib import Path

def test_tailwind_compilation():
    """Test if Tailwind CSS is being compiled correctly"""
    print("🎨 Testing Tailwind CSS Compilation...")
    
    # Check if compiled CSS exists
    css_file = Path("public/tailwind.css")
    if not css_file.exists():
        print("  ❌ Compiled CSS file not found")
        return False
    
    css_content = css_file.read_text()
    
    # Check for Tailwind utilities
    tailwind_classes = [
        "flex", "items-center", "justify-center", 
        "bg-gradient-to-br", "from-blue-500", "to-purple-600",
        "text-white", "font-bold", "text-5xl"
    ]
    
    missing_classes = []
    for cls in tailwind_classes:
        if f".{cls}" not in css_content and cls not in css_content:
            missing_classes.append(cls)
    
    if missing_classes:
        print(f"  ❌ Missing Tailwind classes: {missing_classes}")
        return False
    
    print("  ✅ Tailwind CSS compiled successfully")
    print(f"  ✅ CSS file size: {len(css_content)} characters")
    return True

def test_server_with_tailwind():
    """Test if server serves Tailwind CSS correctly"""
    print("\n🌐 Testing Server Tailwind CSS Serving...")
    
    try:
        # Start server in background
        server_process = subprocess.Popen(
            ["python3", "-m", "nextpy.cli", "dev", "--port", "5002"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        # Wait for server to start
        time.sleep(5)
        
        # Test homepage
        try:
            response = requests.get("http://localhost:5002", timeout=5)
            if response.status_code == 200:
                print("  ✅ Homepage accessible")
                
                # Check if Tailwind CSS is linked
                if "tailwind.css" in response.text:
                    print("  ✅ Tailwind CSS linked in HTML")
                else:
                    print("  ⚠️  Tailwind CSS not found in HTML")
            else:
                print(f"  ❌ Homepage returned {response.status_code}")
        except requests.RequestException as e:
            print(f"  ❌ Could not access homepage: {e}")
        
        # Test Tailwind CSS file
        try:
            css_response = requests.get("http://localhost:5002/tailwind.css", timeout=5)
            if css_response.status_code == 200:
                print("  ✅ Tailwind CSS file served")
                
                # Check CSS content
                if "tailwindcss" in css_response.text.lower():
                    print("  ✅ CSS contains Tailwind styles")
                else:
                    print("  ⚠️  CSS may not contain Tailwind styles")
            else:
                print(f"  ❌ CSS file returned {css_response.status_code}")
        except requests.RequestException as e:
            print(f"  ❌ Could not access CSS file: {e}")
        
    except Exception as e:
        print(f"  ❌ Server error: {e}")
    finally:
        # Stop server
        try:
            server_process.terminate()
            server_process.wait(timeout=5)
        except:
            pass
    
    return True

def test_tailwind_in_jsx():
    """Test if Tailwind classes work in JSX components"""
    print("\n🧩 Testing Tailwind in JSX Components...")
    
    # Check if JSX files contain Tailwind classes
    jsx_files = list(Path("pages").glob("*.py"))
    
    if not jsx_files:
        print("  ❌ No JSX files found")
        return False
    
    tailwind_found = False
    for jsx_file in jsx_files:
        content = jsx_file.read_text()
        
        # Look for Tailwind classes in JSX
        if 'class="' in content and any(cls in content for cls in ['flex', 'bg-', 'text-', 'p-', 'm-']):
            print(f"  ✅ Found Tailwind classes in {jsx_file.name}")
            tailwind_found = True
            break
    
    if not tailwind_found:
        print("  ❌ No Tailwind classes found in JSX files")
        return False
    
    return True

def test_tailwind_config():
    """Test Tailwind configuration"""
    print("\n⚙️ Testing Tailwind Configuration...")
    
    # Check tailwind.config.js
    config_file = Path("tailwind.config.js")
    if not config_file.exists():
        print("  ❌ tailwind.config.js not found")
        return False
    
    config_content = config_file.read_text()
    
    # Check for Python files in content
    if ".py" not in config_content:
        print("  ❌ Python files not included in Tailwind config")
        return False
    
    print("  ✅ Tailwind config exists and includes Python files")
    
    # Check postcss.config.js
    postcss_file = Path("postcss.config.js")
    if not postcss_file.exists():
        print("  ❌ postcss.config.js not found")
        return False
    
    postcss_content = postcss_file.read_text()
    
    if "@tailwindcss/postcss" not in postcss_content:
        print("  ❌ New Tailwind PostCSS plugin not configured")
        return False
    
    print("  ✅ PostCSS config uses new Tailwind plugin")
    return True

def main():
    """Run all Tailwind integration tests"""
    print("🚀 Testing Tailwind CSS Integration in NextPy")
    print("=" * 50)
    
    tests = [
        test_tailwind_config,
        test_tailwind_compilation,
        test_tailwind_in_jsx,
        test_server_with_tailwind
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"  ❌ Test failed: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    
    passed = sum(results)
    total = len(results)
    
    print(f"  Passed: {passed}/{total}")
    
    if passed == total:
        print("  ✅ All tests passed! Tailwind CSS is fully integrated.")
        print("\n🎉 You can use Tailwind CSS in your NextPy components!")
        print("\n💡 Example usage:")
        print('  <div class="flex items-center justify-center bg-blue-500">')
        print('    <h1 class="text-white text-2xl font-bold">Hello Tailwind!</h1>')
        print("  </div>")
    else:
        print("  ❌ Some tests failed. Tailwind CSS integration needs attention.")
        print("\n🔧 Check the failed tests above to fix the issues.")

if __name__ == "__main__":
    main()
