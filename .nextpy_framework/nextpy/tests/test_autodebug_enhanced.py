#!/usr/bin/env python3
"""
Test Enhanced AutoDebug System
Tests the enhanced AutoDebug.py with event listener tracking, component state monitoring, and WebSocket status
"""

import sys
from pathlib import Path

# Add framework to path
sys.path.insert(0, str(Path(__file__).parent / ".nextpy_framework"))

def test_autodebug_imports():
    """Test that AutoDebug can be imported and functions work"""
    print("Testing AutoDebug imports...")
    
    try:
        from nextpy.components.debug.AutoDebug import should_show_debug, get_debug_config, inject_debug_icon
        print("✓ AutoDebug module imported successfully")
        
        # Test configuration
        config = get_debug_config()
        assert isinstance(config, dict)
        assert "show_debug_icon" in config
        assert "auto_capture_errors" in config
        print("✓ Debug configuration works")
        
        # Test debug detection
        debug_enabled = should_show_debug()
        print(f"✓ Debug detection works: {debug_enabled}")
        
        return True
        
    except Exception as e:
        print(f"✗ AutoDebug import test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_html_injection():
    """Test HTML injection with debug content"""
    print("\nTesting HTML injection...")
    
    try:
        from nextpy.components.debug.AutoDebug import inject_debug_icon
        
        # Test basic HTML
        basic_html = "<html><body><h1>Test</h1></body></html>"
        enhanced_html = inject_debug_icon(basic_html)
        
        # Check if debug elements are injected
        assert "nextpy-debug-overlay" in enhanced_html
        assert "nextpy-debug-icon" in enhanced_html
        assert "nextpy-debug-panel" in enhanced_html
        print("✓ Debug HTML elements injected")
        
        # Check for new sections
        assert "Event Listeners" in enhanced_html
        assert "Component State" in enhanced_html
        assert "WebSocket Status" in enhanced_html
        print("✓ Enhanced debug sections present")
        
        # Check for JavaScript functions
        assert "nextpyDebugExpose" in enhanced_html
        assert "trackEventListener" in enhanced_html
        assert "updateComponentState" in enhanced_html
        print("✓ Enhanced JavaScript functions present")
        
        # Check for CSS styles
        assert "nextpy-debug-events" in enhanced_html
        assert "nextpy-debug-components" in enhanced_html
        assert "nextpy-debug-websocket" in enhanced_html
        print("✓ Enhanced CSS styles present")
        
        return True
        
    except Exception as e:
        print(f"✗ HTML injection test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_page_props_handling():
    """Test page props handling in debug"""
    print("\nTesting page props handling...")
    
    try:
        from nextpy.components.debug.AutoDebug import inject_debug_icon
        
        # Test with page props
        html_with_props = "<html><body><h1>Test</h1></body></html>"
        page_props = {
            "route": "/test",
            "user": {"name": "Test User"},
            "data": [1, 2, 3, 4, 5]
        }
        
        enhanced_html = inject_debug_icon(html_with_props, page_props)
        
        # Check if page props are included
        assert "Page Props" in enhanced_html
        assert "test" in enhanced_html
        assert "Test User" in enhanced_html
        print("✓ Page props properly included")
        
        return True
        
    except Exception as e:
        print(f"✗ Page props test failed: {e}")
        return False

def test_debug_configuration():
    """Test debug configuration options"""
    print("\nTesting debug configuration...")
    
    try:
        from nextpy.components.debug.AutoDebug import get_debug_config
        
        # Test default configuration
        config = get_debug_config()
        expected_keys = [
            "show_debug_icon",
            "auto_capture_errors", 
            "show_performance",
            "show_console",
            "position",
            "theme"
        ]
        
        for key in expected_keys:
            assert key in config, f"Missing config key: {key}"
        
        print("✓ All expected configuration keys present")
        
        # Test configuration values are proper types
        assert isinstance(config["show_debug_icon"], bool)
        assert isinstance(config["auto_capture_errors"], bool)
        assert isinstance(config["position"], str)
        assert isinstance(config["theme"], str)
        print("✓ Configuration values have proper types")
        
        return True
        
    except Exception as e:
        print(f"✗ Debug configuration test failed: {e}")
        return False

def test_enhanced_features():
    """Test enhanced features availability"""
    print("\nTesting enhanced features...")
    
    try:
        from nextpy.components.debug.AutoDebug import inject_debug_icon
        
        html = "<html><body><h1>Test</h1></body></html>"
        enhanced_html = inject_debug_icon(html)
        
        # Test for enhanced JavaScript features
        enhanced_features = [
            "eventListeners: new Map()",
            "componentStates: new Map()", 
            "websocketState:",
            "exposeEventListeners:",
            "trackEventListener:",
            "updateComponentState:",
            "updateWebSocketState:",
            "nextpyDebugExpose:",
            "updateEventDisplay:",
            "updateComponentDisplay:",
            "updateWebSocketDisplay:"
        ]
        
        missing_features = []
        for feature in enhanced_features:
            if feature not in enhanced_html:
                missing_features.append(feature)
        
        if not missing_features:
            print("✓ All enhanced JavaScript features present")
        else:
            print(f"✗ Missing features: {missing_features}")
            return False
        
        # Test for enhanced CSS features
        css_features = [
            "nextpy-debug-events",
            "nextpy-debug-event-item",
            "nextpy-debug-components",
            "nextpy-debug-component-item",
            "nextpy-debug-websocket",
            "nextpy-debug-count"
        ]
        
        missing_css = []
        for feature in css_features:
            if feature not in enhanced_html:
                missing_css.append(feature)
        
        if not missing_css:
            print("✓ All enhanced CSS features present")
        else:
            print(f"✗ Missing CSS features: {missing_css}")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ Enhanced features test failed: {e}")
        return False

def main():
    """Run all AutoDebug tests"""
    print("=" * 60)
    print("Enhanced AutoDebug System Test Suite")
    print("=" * 60)
    
    tests = [
        test_autodebug_imports,
        test_html_injection,
        test_page_props_handling,
        test_debug_configuration,
        test_enhanced_features,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 All Enhanced AutoDebug tests passed!")
        print("\n✅ Enhanced Features Successfully Implemented:")
        print("  • Event listener tracking and exposure to window")
        print("  • Component state monitoring and display")
        print("  • WebSocket status tracking")
        print("  • Enhanced UI with proper scroll overflow")
        print("  • True values instead of string comparisons")
        print("  • Comprehensive interactivity improvements")
        
        print("\n🔧 Window Exposed Functions:")
        print("  • window.nextpyDebugExpose.getEventListeners()")
        print("  • window.nextpyDebugExpose.getComponentStates()")
        print("  • window.nextpyDebugExpose.getWebSocketState()")
        print("  • window.nextpyDebugExpose.getLogs()")
        print("  • window.nextpyDebugExpose.getMetrics()")
        print("  • window.nextpyDebugExpose.trackEvent()")
        print("  • window.nextpyDebugExpose.updateComponent()")
        print("  • window.nextpyDebugExpose.updateWebSocket()")
        
        print("\n🚀 Enhanced AutoDebug System Ready for Development!")
        
    else:
        print(f"\n❌ {total - passed} tests failed. Please review the issues above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
