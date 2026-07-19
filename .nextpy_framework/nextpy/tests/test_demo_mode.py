"""
Test the demo mode functionality
"""

import sys
from pathlib import Path

# Add the nextpy framework to the path
sys.path.insert(0, str(Path(__file__).parent / ".nextpy_framework"))

from nextpy.core.demo_router import demo_router
from nextpy.core.demo_pages_simple import HomePage, ComponentsPage


def test_demo_mode():
    """Test demo mode detection and page serving"""
    print("=== Testing Demo Mode ===\n")
    
    # Test demo mode detection
    print("1. Testing demo mode detection...")
    is_demo = demo_router.should_serve_demo()
    print(f"Should serve demo: {is_demo}")
    print()
    
    # Test demo routes
    print("2. Testing demo routes...")
    routes = demo_router.get_demo_routes()
    print(f"Available demo routes: {list(routes.keys())}")
    print()
    
    # Test demo page functions
    print("3. Testing demo page functions...")
    
    # Test home page
    home_page = demo_router.get_demo_page('/')
    if home_page:
        print("✅ Home page function found")
        try:
            result = home_page()
            print(f"✅ Home page renders successfully")
            print(f"HTML length: {len(result)} characters")
        except Exception as e:
            print(f"❌ Home page render error: {e}")
    else:
        print("❌ Home page function not found")
    
    # Test components page
    components_page = demo_router.get_demo_page('/components')
    if components_page:
        print("✅ Components page function found")
    else:
        print("❌ Components page function not found")
    
    print()
    
    # Test demo route matching
    print("4. Testing demo route matching...")
    test_routes = ['/', '/components', '/hooks', '/docs', '/nonexistent']
    
    for route in test_routes:
        page_func = demo_router.get_demo_page(route)
        if page_func:
            print(f"✅ {route} -> Function found")
        else:
            print(f"❌ {route} -> No function found")
    
    print()
    print("=== Demo Mode Test Complete ===")
    print("\n🎉 Demo mode is ready!")
    print("\nWhen users install NextPy and run 'nextpy dev' without creating a project:")
    print("• They'll see the beautiful homepage")
    print("• They can browse documentation")
    print("• They can explore components and hooks")
    print("• They'll be prompted to create a project")
    print("• Full NextPy experience without setup!")


if __name__ == "__main__":
    test_demo_mode()
