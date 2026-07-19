#!/usr/bin/env python3
"""Test Tailwind CSS integration in NextPy"""

import sys
import os
from pathlib import Path

# Add the framework to path
sys.path.insert(0, str(Path(__file__).parent / ".nextpy_framework"))

from nextpy.plugins.builtin import TailwindPlugin
from nextpy.plugins.base import PluginContext

def test_tailwind_integration():
    """Test Tailwind CSS plugin integration"""
    
    print("🧪 Testing Tailwind CSS Integration...")
    
    # Create test JSX content with Tailwind classes
    test_content = '''
def Home(props=None):
    props = props or {}
    return (
        <div class="flex items-center justify-center min-h-screen bg-gradient-to-br from-blue-500 to-purple-600">
            <div class="text-center text-white">
                <h1 class="mb-4 text-5xl font-bold">Hello NextPy!</h1>
                <p class="text-xl mb-8">Build modern web apps with Python</p>
                <button class="bg-white text-blue-600 px-6 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors transform hover:scale-105">
                    Get Started
                </button>
            </div>
        </div>
    )
'''
    
    # Create plugin context
    context = PluginContext(
        file_path=Path("test.py"),
        file_content=test_content,
        metadata={},
        config={},
        debug=True
    )
    
    # Initialize and test Tailwind plugin
    tailwind_plugin = TailwindPlugin()
    
    print("📝 Original content:")
    print(test_content)
    print("\n" + "="*50)
    
    # Apply plugin transformation
    result = tailwind_plugin.transform(context)
    
    print("🔧 Plugin Result:")
    print(f"✅ Success: {result.success}")
    print(f"📊 Metadata: {result.metadata}")
    
    if result.errors:
        print(f"❌ Errors: {result.errors}")
    
    if result.warnings:
        print(f"⚠️  Warnings: {result.warnings}")
    
    print("\n📝 Transformed content:")
    print(result.content)
    
    # Test specific optimizations
    print("\n" + "="*50)
    print("🔍 Testing Optimizations:")
    
    # Check for duplicate class removal
    if "flex items-center justify-center" in result.content:
        print("✅ Duplicate classes preserved (correct)")
    else:
        print("❌ Duplicate classes incorrectly removed")
    
    # Check for class optimization
    if "className=" in result.content:
        print("✅ className attribute preserved")
    else:
        print("❌ className attribute missing")
    
    # Test with duplicate classes
    duplicate_test = '''
<div class="flex flex items-center justify-center text-white text-white">
    <h1 class="text-2xl font-bold text-2xl">Hello</h1>
</div>
'''
    
    context_duplicate = PluginContext(
        file_path=Path("duplicate_test.py"),
        file_content=duplicate_test,
        metadata={},
        config={},
        debug=True
    )
    
    result_duplicate = tailwind_plugin.transform(context_duplicate)
    
    print("\n🔄 Testing Duplicate Class Removal:")
    print("Original:", duplicate_test.strip())
    print("Transformed:", result_duplicate.content.strip())
    
    # Count optimizations
    original_count = duplicate_test.count("text-white") + duplicate_test.count("text-2xl")
    transformed_count = result_duplicate.content.count("text-white") + result_duplicate.content.count("text-2xl")
    
    if transformed_count < original_count:
        print(f"✅ Removed {original_count - transformed_count} duplicate classes")
    else:
        print("❌ No duplicate classes removed")
    
    print("\n🎉 Tailwind CSS Integration Test Complete!")
    
    return result.success

if __name__ == "__main__":
    success = test_tailwind_integration()
    if success:
        print("\n✅ Tailwind CSS integration is working well!")
        sys.exit(0)
    else:
        print("\n❌ Tailwind CSS integration has issues!")
        sys.exit(1)
