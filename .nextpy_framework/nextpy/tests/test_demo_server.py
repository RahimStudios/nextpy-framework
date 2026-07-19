"""
Test the demo server functionality
Simulates running nextpy dev without a project
"""

import sys
from pathlib import Path

# Add the nextpy framework to the path
sys.path.insert(0, str(Path(__file__).parent / ".nextpy_framework"))

from nextpy.core.demo_router import demo_router
from nextpy.core.demo_pages_simple import HomePage


def test_demo_server_simulation():
    """Simulate running nextpy dev without a project"""
    print("=== Simulating 'nextpy dev' without project ===\n")
    
    # Check if we're in a NextPy project
    print("1. Checking current directory...")
    is_project = demo_router.is_nextpy_project()
    print(f"Is NextPy project: {is_project}")
    
    if not is_project:
        print("✅ No project detected - Demo mode would be activated")
        print("\n🎉 NextPy Demo Mode - No project detected")
        print("📚 Showing built-in documentation and examples")
        print("💡 Create a project with: nextpy create my-app")
        print()
        
        # Show what pages would be available
        print("2. Available demo pages:")
        routes = demo_router.get_demo_routes()
        for route in routes:
            print(f"   http://localhost:5000{route}")
        
        print()
        print("3. Sample homepage content:")
        home_page = demo_router.get_demo_page('/')
        if home_page:
            html_content = home_page()
            # Show first few lines of the homepage
            lines = html_content.split('\n')[:10]
            for line in lines:
                print(f"   {line}")
            print("   ...")
        
        print()
        print("4. What users would see:")
        print("   • Beautiful landing page with NextPy branding")
        print("   • Links to documentation and examples")
        print("   • Clear instructions to create a project")
        print("   • Full demonstration of NextPy capabilities")
        
        print()
        print("5. User flow:")
        print("   1. User installs: pip install nextpy-framework")
        print("   2. User runs: nextpy dev")
        print("   3. NextPy detects no project → Demo mode")
        print("   4. User sees homepage at http://localhost:5000")
        print("   5. User can explore docs, components, hooks")
        print("   6. User clicks 'Create Project' or runs command")
        print("   7. User creates real project and starts building!")
        
    else:
        print("❌ Project detected - Normal mode would be used")
    
    print()
    print("=== Demo Server Simulation Complete ===")


if __name__ == "__main__":
    test_demo_server_simulation()
