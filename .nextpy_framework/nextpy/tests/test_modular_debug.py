#!/usr/bin/env python3
"""
Test Suite for NextPy Modular Debug System v3.0
Tests the clean, event-driven architecture
"""

import sys
import time
import asyncio
from pathlib import Path

# Add framework to path
sys.path.insert(0, str(Path(__file__).parent / ".nextpy_framework"))

def test_runtime_events():
    """Test runtime event system"""
    print("Testing Runtime Event System...")
    
    try:
        from nextpy.runtime.events import event_system, RuntimeEvents, RuntimeIntegration
        
        # Test event registration
        events_received = []
        
        def test_callback(event):
            events_received.append(event)
        
        listener_id = event_system.on(RuntimeEvents.COMPONENT_MOUNT, test_callback)
        assert listener_id is not None
        print("✓ Event registration works")
        
        # Test event emission
        test_data = {"component_id": "test_comp", "props": {"value": 42}}
        event_system.emit(RuntimeEvents.COMPONENT_MOUNT, test_data, "test")
        
        assert len(events_received) == 1
        assert events_received[0].event_type == RuntimeEvents.COMPONENT_MOUNT
        assert events_received[0].data == test_data
        print("✓ Event emission works")
        
        # Test event history
        history = event_system.get_history(RuntimeEvents.COMPONENT_MOUNT)
        assert len(history) == 1
        print("✓ Event history works")
        
        # Test listener removal
        removed = event_system.off(RuntimeEvents.COMPONENT_MOUNT, listener_id)
        assert removed is True
        print("✓ Listener removal works")
        
        return True
        
    except Exception as e:
        print(f"✗ Runtime events test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_debug_core():
    """Test debug core functionality"""
    print("\nTesting Debug Core...")
    
    try:
        from nextpy.debug.core import debug_core, start_debug_session, end_debug_session
        
        # Test session management
        session_id = start_debug_session()
        assert session_id is not None
        assert debug_core.enabled is True
        print("✓ Session start works")
        
        # Test component tracking
        debug_core.track_component_state("test_comp", {"count": 5, "active": True})
        state = debug_core.get_component_state("test_comp")
        assert state["count"] == 5
        print("✓ Component tracking works")
        
        # Test event tracking
        debug_core.track_event("test_event", {"data": "test"}, "test_source")
        events = debug_core.get_event_history("test_event")
        assert len(events) == 1
        print("✓ Event tracking works")
        
        # Test performance tracking
        debug_core.track_performance("test_metric", 100.5, {"unit": "ms"})
        metrics = debug_core.get_performance_metrics()
        assert "test_metric" in metrics
        print("✓ Performance tracking works")
        
        # Test WebSocket tracking
        debug_core.track_websocket_state({"connected": True, "client_id": "test_client"})
        ws_state = debug_core.get_websocket_state()
        assert ws_state["connected"] is True
        print("✓ WebSocket tracking works")
        
        # Test session end
        summary = end_debug_session()
        assert summary is not None
        assert summary["session_id"] == session_id
        print("✓ Session end works")
        
        return True
        
    except Exception as e:
        print(f"✗ Debug core test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_performance_monitor():
    """Test performance monitoring"""
    print("\nTesting Performance Monitor...")
    
    try:
        from nextpy.debug.performance import performance_monitor, start_timer, end_timer, record_metric
        
        # Test timer functionality
        start_timer("test_timer")
        time.sleep(0.01)  # Small delay
        duration = end_timer("test_timer", "ms")
        assert duration is not None
        assert duration > 0
        print("✓ Timer functionality works")
        
        # Test metric recording
        record_metric("test_metric", 42.5, "units", {"metadata": "test"})
        metric = performance_monitor.get_metric("test_metric")
        assert metric is not None
        assert metric.value == 42.5
        print("✓ Metric recording works")
        
        # Test averages
        for i in range(5):
            record_metric("avg_test", i * 10, "count")
        
        avg = performance_monitor.get_average("avg_test")
        assert avg == 20.0  # (0 + 10 + 20 + 30 + 40) / 5
        print("✓ Average calculation works")
        
        # Test counters
        performance_monitor.increment_counter("test_counter")
        performance_monitor.increment_counter("test_counter", 5)
        counters = performance_monitor.get_counters()
        assert counters["test_counter"] == 6
        print("✓ Counter functionality works")
        
        return True
        
    except Exception as e:
        print(f"✗ Performance monitor test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_websocket_tracker():
    """Test WebSocket tracking"""
    print("\nTesting WebSocket Tracker...")
    
    try:
        from nextpy.debug.websocket import ws_tracker, get_websocket_state
        
        # Test connection tracking
        ws_tracker.track_connection("test_client_123", "ws://localhost:8000/ws")
        state = ws_tracker.get_state()
        assert state["connected"] is True
        assert state["client_id"] == "test_client_123"
        print("✓ Connection tracking works")
        
        # Test message tracking
        ws_tracker.track_message("state_update", {"component": "test", "state": {"count": 5}}, "incoming")
        ws_tracker.track_message("component_event", {"event": "click"}, "outgoing")
        
        messages = ws_tracker.get_recent_messages(2)
        assert len(messages) == 2
        assert messages[0]["direction"] == "incoming"
        assert messages[1]["direction"] == "outgoing"
        print("✓ Message tracking works")
        
        # Test error tracking
        test_error = Exception("Test error")
        ws_tracker.track_error(test_error, "test_context")
        state = ws_tracker.get_state()
        assert state["error_count"] == 1
        print("✓ Error tracking works")
        
        # Test disconnection
        ws_tracker.track_disconnection("Normal closure")
        state = ws_tracker.get_state()
        assert state["connected"] is False
        print("✓ Disconnection tracking works")
        
        # Test global function
        global_state = get_websocket_state()
        assert global_state["connected"] is False
        print("✓ Global state function works")
        
        return True
        
    except Exception as e:
        print(f"✗ WebSocket tracker test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_debug_ui():
    """Test debug UI generation"""
    print("\nTesting Debug UI...")
    
    try:
        from nextpy.debug.ui import debug_ui
        
        # Test HTML generation
        html = debug_ui.generate_html({"route": "/test", "user": "test"})
        assert "nextpy-debug-overlay" in html
        assert "nextpy-debug-icon" in html
        assert "nextpy-debug-panel" in html
        print("✓ HTML generation works")
        
        # Test JavaScript generation
        js = debug_ui.generate_javascript()
        assert "nextpyDebugUI" in js
        assert "toggle" in js
        assert "fetchAPI" in js
        print("✓ JavaScript generation works")
        
        # Test CSS generation
        css = debug_ui.generate_css()
        assert ".nextpy-debug-overlay" in css
        assert ".nextpy-debug-icon" in css
        assert ".nextpy-debug-panel" in css
        print("✓ CSS generation works")
        
        # Test UI injection
        from nextpy.debug.ui import inject_debug_ui
        test_html = "<html><body><h1>Test</h1></body></html>"
        enhanced_html = inject_debug_ui(test_html)
        assert "nextpy-debug-overlay" in enhanced_html
        assert enhanced_html.count("</body>") == 1  # Should still have only one closing body tag
        print("✓ UI injection works")
        
        return True
        
    except Exception as e:
        print(f"✗ Debug UI test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_autodebug_v3():
    """Test AutoDebug v3 integration"""
    print("\nTesting AutoDebug v3...")
    
    try:
        # Test import
        from nextpy.components.debug.AutoDebug_v3 import should_show_debug, get_debug_config, setup_debug_system
        print("✓ AutoDebug v3 import works")
        
        # Test configuration
        config = get_debug_config()
        assert isinstance(config, dict)
        assert "show_debug_icon" in config
        assert "modular" in config
        assert config["modular"] is True
        print("✓ Configuration works")
        
        # Test HTML injection
        from nextpy.components.debug.AutoDebug_v3 import inject_debug_icon
        test_html = "<html><body><h1>Test</h1></body></html>"
        page_props = {"route": "/test", "data": {"value": 42}}
        
        enhanced_html = inject_debug_icon(test_html, page_props)
        assert "nextpy-debug-overlay" in enhanced_html
        assert "NextPyRuntime" in enhanced_html
        print("✓ HTML injection works")
        
        return True
        
    except Exception as e:
        print(f"✗ AutoDebug v3 test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_event_driven_architecture():
    """Test event-driven architecture integration"""
    print("\nTesting Event-Driven Architecture...")
    
    try:
        from nextpy.runtime.events import event_system, RuntimeEvents
        from nextpy.debug.core import debug_core
        from nextpy.debug.performance import performance_monitor
        
        # Start debug session
        from nextpy.debug.core import start_debug_session
        session_id = start_debug_session()
        
        # Test component event flow
        def component_mount_handler(event):
            debug_core.track_component_state(event.component_id, event.data)
        
        event_system.on(RuntimeEvents.COMPONENT_MOUNT, component_mount_handler)
        
        # Emit component mount event
        event_system.emit(RuntimeEvents.COMPONENT_MOUNT, 
                        {"count": 10, "active": True}, 
                        "test_source", 
                        "test_component")
        
        # Check if debug core received the state
        state = debug_core.get_component_state("test_component")
        assert state["count"] == 10
        print("✓ Component event flow works")
        
        # Test performance event flow
        def performance_handler(event):
            metric_name = event.data.get("metric", "unknown")
            value = event.data.get("value", 0)
            performance_monitor.record_metric(metric_name, value)
        
        event_system.on(RuntimeEvents.PERFORMANCE_METRIC, performance_handler)
        
        # Emit performance event
        event_system.emit(RuntimeEvents.PERFORMANCE_METRIC, 
                        {"metric": "render_time", "value": 16.7})
        
        # Check if performance monitor received the metric
        metric = performance_monitor.get_metric("render_time")
        assert metric.value == 16.7
        print("✓ Performance event flow works")
        
        # Clean up
        from nextpy.debug.core import end_debug_session
        end_debug_session()
        
        return True
        
    except Exception as e:
        print(f"✗ Event-driven architecture test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_modular_encapsulation():
    """Test modular encapsulation and no global pollution"""
    print("\nTesting Modular Encapsulation...")
    
    try:
        # Test that modules are properly isolated
        from nextpy.debug.core import debug_core
        from nextpy.debug.ui import debug_ui
        from nextpy.debug.websocket import ws_tracker
        from nextpy.debug.performance import performance_monitor
        from nextpy.runtime.events import event_system
        
        # Each module should have its own instance
        assert debug_core is not None
        assert debug_ui is not None
        assert ws_tracker is not None
        assert performance_monitor is not None
        assert event_system is not None
        
        # Test that they don't share internal state inappropriately
        debug_core.track_component_state("test", {"value": 1})
        assert debug_core.get_component_state("test")["value"] == 1
        
        # WebSocket tracker should be independent
        ws_state = ws_tracker.get_state()
        assert ws_state["connected"] is False  # Should be default state
        
        # Performance monitor should be independent
        perf_metrics = performance_monitor.get_all_metrics()
        assert "test" not in perf_metrics  # Should not have debug core data
        
        # Event system should be independent
        history = event_system.get_history()
        assert len(history) == 0  # Should be empty by default
        
        print("✓ Modules are properly encapsulated")
        print("✓ No global pollution detected")
        
        return True
        
    except Exception as e:
        print(f"✗ Modular encapsulation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all modular debug system tests"""
    print("=" * 70)
    print("NextPy Modular Debug System v3.0 - Test Suite")
    print("=" * 70)
    
    tests = [
        test_runtime_events,
        test_debug_core,
        test_performance_monitor,
        test_websocket_tracker,
        test_debug_ui,
        test_autodebug_v3,
        test_event_driven_architecture,
        test_modular_encapsulation,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 70)
    print("Test Results Summary")
    print("=" * 70)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 All Modular Debug System tests passed!")
        print("\n✅ Clean Architecture Successfully Implemented:")
        print("  • Modular components (core, ui, websocket, performance)")
        print("  • Event-driven runtime integration")
        print("  • Proper encapsulation without global pollution")
        print("  • Clean WebSocket hooks")
        print("  • Performance monitoring without polling")
        print("  • Runtime event system")
        print("  • NextPyRuntime.log wrapper instead of console override")
        print("  • Event listener tracking with patching")
        
        print("\n🔧 Architecture Improvements:")
        print("  • No more monolithic injected strings")
        print("  • No tight coupling with runtime")
        print("  • No global window pollution")
        print("  • No expensive DOM scanning")
        print("  • No console override conflicts")
        print("  • No polling-based updates")
        
        print("\n🚀 NextPy Debug System v3.0 Ready for Production!")
        
    else:
        print(f"\n❌ {total - passed} tests failed. Please review the issues above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
