"""
NextPy AutoDebug System v3.0
Clean, modular, event-driven debugging architecture
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional

# Import modular debug components
AUTO_DEBUG_AVAILABLE = True
debug_core = None
debug_ui = None
event_system = None

try:
    from ..debug.core import debug_core
    from ..debug.core import start_debug_session
    from ..debug.core import end_debug_session
except ImportError:
    debug_core = None
    start_debug_session = None
    end_debug_session = None
    try:
        # Fallback basic implementation
        class MockDebugCore:
            def set_verbose(self, enabled): pass
            def set_capture_console(self, enabled): pass
            def set_capture_performance(self, enabled): pass
        debug_core = MockDebugCore()
        
        def start_debug_session():
            return "mock_session"
        
        def end_debug_session():
            return {"mock": "summary"}
    except:
        AUTO_DEBUG_AVAILABLE = False

try:
    from ...debug.ui import debug_ui as real_debug_ui
    from ...debug.ui import inject_debug_ui as real_inject_debug_ui
    # Use the real implementations
    debug_ui = real_debug_ui
    inject_debug_ui = real_inject_debug_ui
except ImportError as e:
    print(f"Warning: Debug UI import failed: {e}")
    debug_ui = None
    inject_debug_ui = None
    # Don't create fallback UI here - let the system handle it gracefully

try:
    from ..runtime.events import event_system, RuntimeEvents
except ImportError:
    event_system = None
    try:
        # Fallback basic implementation
        class MockEventSystem:
            def on(self, event_type, callback): return 'mock_id'
            def emit(self, event_type, data, source='runtime'): pass
        event_system = MockEventSystem()
    except:
        pass


def should_show_debug() -> bool:
    """Check if debug system should be shown based on environment"""
    return (
        os.getenv("NEXTPY_DEBUG") == "true" or 
        os.getenv("DEBUG") == "true" or
        os.getenv("DEVELOPMENT") == "true" or
        "--debug" in sys.argv or
        not os.getenv("PRODUCTION")  # Default to debug in non-production
    )


def get_debug_config() -> Dict[str, Any]:
    """Get debug configuration from environment"""
    return {
        "show_debug_icon": should_show_debug(),
        "auto_capture_errors": os.getenv("NEXTPY_DEBUG_CAPTURE_ERRORS", "true").lower() == "true",
        "show_performance": os.getenv("NEXTPY_DEBUG_PERFORMANCE", "true").lower() == "true",
        "show_console": os.getenv("NEXTPY_DEBUG_CONSOLE", "true").lower() == "true",
        "position": os.getenv("NEXTPY_DEBUG_POSITION", "bottom-right"),
        "theme": os.getenv("NEXTPY_DEBUG_THEME", "dark"),
        "verbose": os.getenv("NEXTPY_DEBUG_VERBOSE", "false").lower() == "true",
        "modular": True  # New modular architecture
    }


def inject_debug_icon(html_content: str, page_props: Dict[str, Any] = None) -> str:
    """
    Inject modular debug system into HTML content
    
    Args:
        html_content: HTML content to inject into
        page_props: Page props for debugging
        
    Returns:
        Enhanced HTML content with debug system
    """
    # Always inject if called, regardless of AUTO_DEBUG_AVAILABLE
    config = get_debug_config()
    
    if not config["show_debug_icon"]:
        return html_content
    
    # Start debug session if needed
    if config.get("auto_start", True) and start_debug_session:
        start_debug_session()
    
    # Configure debug core
    if debug_core:
        debug_core.set_verbose(config.get("verbose", False))
        debug_core.set_capture_console(config["show_console"])
        debug_core.set_capture_performance(config["show_performance"])
    
    # Install WebSocket hooks
    if config.get("websocket_hooks", True):
        try:
            from ..debug.websocket import install_websocket_debugging
            install_websocket_debugging()
        except ImportError:
            pass
    
    # Setup event listeners
    setup_event_listeners()
    
    # Inject modular UI
    if debug_ui and hasattr(debug_ui, 'generate_html'):
        # Use full modular UI
        html_content = inject_debug_ui(html_content, page_props)
    elif inject_debug_ui:
        # Fallback UI (should show full features if available)
        html_content = inject_debug_ui(html_content, page_props)
    
    # Add runtime integration script
    html_content = inject_runtime_integration(html_content)
    
    return html_content


def setup_event_listeners():
    """Setup event listeners for runtime integration"""
    if not event_system or not debug_core:
        return
    
    try:
        # Component events
        event_system.on(RuntimeEvents.COMPONENT_MOUNT, lambda e: debug_core.track_component_state(e.component_id, e.data))
        event_system.on(RuntimeEvents.COMPONENT_UPDATE, lambda e: debug_core.track_component_state(e.component_id, e.data))
        
        # WebSocket events
        event_system.on(RuntimeEvents.WS_CONNECTED, lambda e: debug_core.track_websocket_state({'connected': True, **e.data}))
        event_system.on(RuntimeEvents.WS_DISCONNECTED, lambda e: debug_core.track_websocket_state({'connected': False, **e.data}))
        event_system.on(RuntimeEvents.WS_MESSAGE, lambda e: debug_core.track_event('ws_message', e.data, 'websocket'))
        
        # Performance events
        event_system.on(RuntimeEvents.PERFORMANCE_METRIC, lambda e: debug_core.track_performance(e.data.get('metric', 'unknown'), e.data.get('value', 0), e.data))
        event_system.on(RuntimeEvents.RENDER_START, lambda e: debug_core.track_event('render_start', e.data, 'performance'))
        event_system.on(RuntimeEvents.RENDER_END, lambda e: debug_core.track_event('render_end', e.data, 'performance'))
        
        # Debug events
        event_system.on(RuntimeEvents.DEBUG_LOG, lambda e: debug_core.track_event('debug_log', e.data, 'debug'))
        event_system.on(RuntimeEvents.DEBUG_ERROR, lambda e: debug_core.track_event('debug_error', e.data, 'debug'))
    except Exception:
        # Silently handle event setup errors
        pass


def inject_runtime_integration(html_content: str) -> str:
    """Inject runtime integration script"""
    integration_script = """
    <script>
        // NextPy Runtime Integration - Clean Architecture
        (function() {
            'use strict';
            
            // Runtime event emitter
            window.NextPyRuntime = window.NextPyRuntime || {
                events: {},
                
                on: function(eventType, callback) {
                    if (!this.events[eventType]) {
                        this.events[eventType] = [];
                    }
                    this.events[eventType].push(callback);
                },
                
                emit: function(eventType, data) {
                    if (this.events[eventType]) {
                        this.events[eventType].forEach(callback => {
                            try {
                                callback({ type: eventType, data: data, timestamp: Date.now() });
                            } catch (e) {
                                console.error('Runtime event error:', e);
                            }
                        });
                    }
                },
                
                log: function(level, message, data) {
                    this.emit('debug:log', { level: level, message: message, data: data });
                    
                    // Still log to console for backward compatibility
                    const originalLog = level === 'ERROR' ? console.error : 
                                      level === 'WARN' ? console.warn : console.log;
                    originalLog.call(console, '[NextPy][' + level + '] ' + message, data || '');
                },
                
                // Component management functions
                createComponent: function(componentId, props) {
                    this.emit('component:create', { componentId: componentId, props: props });
                    
                    // Store component state
                    if (!this.components) {
                        this.components = {};
                    }
                    this.components[componentId] = {
                        id: componentId,
                        props: props,
                        state: {},
                        mounted: false,
                        created: Date.now()
                    };
                    
                    // Find the component element
                    const element = document.getElementById(componentId);
                    if (element) {
                        element.setAttribute('data-component', componentId);
                        this.emit('component:mount', { componentId: componentId, element: element, props: props });
                        this.components[componentId].mounted = true;
                    }
                    
                    return this.components[componentId];
                },
                
                updateComponent: function(componentId, state) {
                    this.emit('component:update', { componentId: componentId, state: state });
                    
                    if (this.components && this.components[componentId]) {
                        this.components[componentId].state = Object.assign({}, this.components[componentId].state, state);
                        this.components[componentId].updated = Date.now();
                    }
                    
                    return this.components ? this.components[componentId] : null;
                },
                
                getComponent: function(componentId) {
                    return this.components ? this.components[componentId] : null;
                },
                
                getAllComponents: function() {
                    return this.components || {};
                }
            };
            
            // Component lifecycle tracking
            const originalCreateElement = document.createElement;
            document.createElement = function(tagName) {
                const element = originalCreateElement.call(this, tagName);
                
                // Track component creation if it has data-component attribute
                if (element.setAttribute) {
                    const originalSetAttribute = element.setAttribute;
                    element.setAttribute = function(name, value) {
                        if (name === 'data-component') {
                            NextPyRuntime.emit('component:mount', { componentId: value, element: element });
                        }
                        return originalSetAttribute.call(this, name, value);
                    };
                }
                
                return element;
            };
            
            // Event listener tracking (clean approach)
            const originalAddEventListener = EventTarget.prototype.addEventListener;
            EventTarget.prototype.addEventListener = function(type, listener, options) {
                // Track event listeners for debugging
                NextPyRuntime.emit('debug:event_listener', {
                    target: this.constructor.name,
                    type: type,
                    listenerCount: (this._nextpyListeners || 0) + 1
                });
                
                // Store listener reference for cleanup
                if (!this._nextpyListeners) {
                    this._nextpyListeners = [];
                }
                this._nextpyListeners.push({ type, listener });
                
                return originalAddEventListener.call(this, type, listener, options);
            };
            
            // Performance monitoring
            if ('performance' in window && 'observer' in window.Performance) {
                const perfObserver = new PerformanceObserver((list) => {
                    list.getEntries().forEach(entry => {
                        NextPyRuntime.emit('performance:metric', {
                            metric: entry.name,
                            value: entry.duration || entry.startTime,
                            entryType: entry.entryType
                        });
                    });
                });
                
                perfObserver.observe({ entryTypes: ['measure', 'navigation', 'resource'] });
            }
            
            // Error handling
            window.addEventListener('error', function(event) {
                NextPyRuntime.emit('debug:error', {
                    message: event.message,
                    filename: event.filename,
                    lineno: event.lineno,
                    colno: event.colno,
                    error: event.error
                });
            });
            
            window.addEventListener('unhandledrejection', function(event) {
                NextPyRuntime.emit('debug:error', {
                    message: 'Unhandled promise rejection',
                    reason: event.reason
                });
            });
            
            // WebSocket integration (with graceful error handling)
            if (window.WebSocket) {
                const OriginalWebSocket = window.WebSocket;
                
                window.WebSocket = function(url, protocols) {
                    // Only intercept NextPy WebSocket connections
                    if (url.includes('/ws') || url.includes('websocket')) {
                        try {
                            const ws = new OriginalWebSocket(url, protocols);
                            
                            ws.addEventListener('open', function() {
                                NextPyRuntime.emit('ws:connected', { url: url, protocols: protocols });
                                NextPyRuntime.log('INFO', 'WebSocket connected', { url: url });
                            });
                            
                            ws.addEventListener('message', function(event) {
                                try {
                                    const data = JSON.parse(event.data);
                                    NextPyRuntime.emit('ws:message', data);
                                } catch {
                                    NextPyRuntime.emit('ws:message', { raw: event.data });
                                }
                            });
                            
                            ws.addEventListener('close', function(event) {
                                NextPyRuntime.emit('ws:disconnected', { 
                                    code: event.code, 
                                    reason: event.reason 
                                });
                                NextPyRuntime.log('INFO', 'WebSocket disconnected', { 
                                    code: event.code, 
                                    reason: event.reason 
                                });
                            });
                            
                            ws.addEventListener('error', function(event) {
                                NextPyRuntime.emit('ws:error', { error: event });
                                NextPyRuntime.log('WARN', 'WebSocket connection failed', { 
                                    url: url,
                                    error: event.error ? event.error.message : 'Unknown error'
                                });
                            });
                            
                            return ws;
                        } catch (error) {
                            // Graceful fallback if WebSocket fails
                            NextPyRuntime.log('WARN', 'WebSocket not available, using fallback mode', { 
                                url: url,
                                error: error.message
                            });
                            
                            // Return a mock WebSocket that doesn't break the app
                            return {
                                addEventListener: function(type, listener) {
                                    if (type === 'error') {
                                        // Simulate connection error after a short delay
                                        setTimeout(() => {
                                            listener({ error: new Error('WebSocket not available') });
                                        }, 100);
                                    }
                                },
                                send: function(data) {
                                    NextPyRuntime.log('DEBUG', 'WebSocket send (mock)', { data: data });
                                },
                                close: function() {
                                    NextPyRuntime.log('DEBUG', 'WebSocket close (mock)');
                                },
                                readyState: 3, // CLOSED
                                CONNECTING: 0,
                                OPEN: 1,
                                CLOSING: 2,
                                CLOSED: 3
                            };
                        }
                    } else {
                        // For non-NextPy WebSockets, use original implementation
                        return new OriginalWebSocket(url, protocols);
                    }
                };
                
                // Copy static properties
                Object.setPrototypeOf(window.WebSocket, OriginalWebSocket);
                Object.setPrototypeOf(window.WebSocket.prototype, OriginalWebSocket.prototype);
            }
            
            // Initialize runtime
            NextPyRuntime.emit('runtime:ready', { timestamp: Date.now() });
            
            console.log('[NextPy] Runtime integration loaded');
            
            // Debug icon visibility check
            setTimeout(() => {
                const debugIcon = document.getElementById('nextpy-debug-icon');
                if (debugIcon) {
                    console.log('[NextPy] Debug icon is visible and ready');
                    // Ensure the icon is visible
                    debugIcon.style.display = 'flex';
                    debugIcon.style.visibility = 'visible';
                    debugIcon.style.opacity = '1';
                } else {
                    console.warn('[NextPy] Debug icon not found in DOM');
                }
            }, 200);
        })();
    </script>
    """
    
    # Insert before closing body tag
    if "</body>" in html_content:
        parts = html_content.split("</body>")
        html_content = parts[0] + integration_script + "</body>" + parts[1] if len(parts) > 1 else parts[0] + integration_script + "</body>"
    else:
        html_content += integration_script
    
    return html_content


# API endpoints for debug UI
def create_debug_api_routes(app):
    """Create API routes for debug system"""
    if not AUTO_DEBUG_AVAILABLE:
        return
    
    @app.get("/__nextpy/debug/status")
    async def get_debug_status():
        """Get debug system status"""
        return {
            "enabled": debug_core.enabled,
            "session_active": debug_core.session is not None,
            "websocket_hooks_installed": install_websocket_debugging(),
            "config": get_debug_config()
        }
    
    @app.post("/__nextpy/debug/start")
    async def start_debug_session_api():
        """Start debug session"""
        session_id = start_debug_session()
        return {
            "success": True,
            "session_id": session_id,
            "start_time": debug_core.session.start_time if debug_core.session else None
        }
    
    @app.post("/__nextpy/debug/end")
    async def end_debug_session_api():
        """End debug session"""
        summary = end_debug_session()
        return {
            "success": True,
            "summary": summary
        }
    
    @app.get("/__nextpy/debug/components")
    async def get_debug_components():
        """Get component states"""
        return debug_core.get_all_component_states()
    
    @app.get("/__nextpy/debug/events")
    async def get_debug_events():
        """Get event history"""
        return debug_core.get_event_history()
    
    @app.get("/__nextpy/debug/performance")
    async def get_debug_performance():
        """Get performance metrics"""
        return get_performance_data()
    
    @app.get("/__nextpy/debug/websocket")
    async def get_debug_websocket():
        """Get WebSocket state"""
        return get_websocket_state()
    
    @app.post("/__nextpy/debug/clear")
    async def clear_debug_data():
        """Clear debug data"""
        debug_core.clear_session_data()
        return {"success": True}
    
    @app.get("/__nextpy/debug/export")
    async def export_debug_data():
        """Export all debug data"""
        data = debug_core.export_session_data()
        return data or {}


# Convenience function to setup debug system
def setup_debug_system(app):
    """Setup complete debug system"""
    if not AUTO_DEBUG_AVAILABLE:
        return
    
    create_debug_api_routes(app)
    
    if should_show_debug():
        print("[NextPy Debug] Modular debug system initialized")
    else:
        print("[NextPy Debug] Debug system disabled")
