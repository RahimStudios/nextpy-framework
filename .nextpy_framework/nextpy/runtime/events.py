"""
NextPy Runtime Event System
Clean event-driven architecture for debug and runtime communication
"""

from typing import Dict, Any, Callable, List, Optional
from dataclasses import dataclass
import json
import time
import asyncio


@dataclass
class RuntimeEvent:
    """Runtime event data structure"""
    event_type: str
    data: Dict[str, Any]
    timestamp: float
    source: str
    component_id: Optional[str] = None


class EventSystem:
    """Clean event system for NextPy runtime"""
    
    def __init__(self):
        self.listeners: Dict[str, List[Callable]] = {}
        self.event_history: List[RuntimeEvent] = []
        self.max_history = 1000
        self.debug_mode = False
    
    def on(self, event_type: str, callback: Callable) -> str:
        """
        Register event listener
        
        Args:
            event_type: Event type to listen for
            callback: Callback function
            
        Returns:
            Listener ID for removal
        """
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        
        listener_id = f"{event_type}_{len(self.listeners[event_type])}_{int(time.time())}"
        self.listeners[event_type].append({
            'id': listener_id,
            'callback': callback
        })
        
        if self.debug_mode:
            print(f"[EventSystem] Registered listener for {event_type}: {listener_id}")
        
        return listener_id
    
    def off(self, event_type: str, listener_id: str) -> bool:
        """
        Remove event listener
        
        Args:
            event_type: Event type
            listener_id: Listener ID
            
        Returns:
            True if removed, False if not found
        """
        if event_type not in self.listeners:
            return False
        
        self.listeners[event_type] = [
            listener for listener in self.listeners[event_type]
            if listener['id'] != listener_id
        ]
        
        if self.debug_mode:
            print(f"[EventSystem] Removed listener {listener_id} from {event_type}")
        
        return True
    
    def emit(self, event_type: str, data: Dict[str, Any], source: str = "runtime", component_id: Optional[str] = None) -> None:
        """
        Emit event to all listeners
        
        Args:
            event_type: Event type
            data: Event data
            source: Event source
            component_id: Component ID if applicable
        """
        event = RuntimeEvent(
            event_type=event_type,
            data=data,
            timestamp=time.time(),
            source=source,
            component_id=component_id
        )
        
        # Add to history
        self.event_history.append(event)
        if len(self.event_history) > self.max_history:
            self.event_history.pop(0)
        
        # Notify listeners
        if event_type in self.listeners:
            for listener_info in self.listeners[event_type]:
                try:
                    listener_info['callback'](event)
                except Exception as e:
                    if self.debug_mode:
                        print(f"[EventSystem] Error in listener {listener_info['id']}: {e}")
        
        if self.debug_mode:
            print(f"[EventSystem] Emitted {event_type} from {source}")
    
    def get_history(self, event_type: Optional[str] = None, limit: int = 100) -> List[RuntimeEvent]:
        """
        Get event history
        
        Args:
            event_type: Filter by event type (optional)
            limit: Maximum number of events
            
        Returns:
            List of events
        """
        events = self.event_history
        
        if event_type:
            events = [e for e in events if e.event_type == event_type]
        
        return events[-limit:] if events else []
    
    def get_listener_count(self, event_type: Optional[str] = None) -> int:
        """
        Get number of listeners
        
        Args:
            event_type: Event type (optional)
            
        Returns:
            Number of listeners
        """
        if event_type:
            return len(self.listeners.get(event_type, []))
        
        return sum(len(listeners) for listeners in self.listeners.values())
    
    def clear_history(self) -> None:
        """Clear event history"""
        self.event_history.clear()
        if self.debug_mode:
            print("[EventSystem] Cleared event history")
    
    def set_debug_mode(self, enabled: bool) -> None:
        """Enable/disable debug mode"""
        self.debug_mode = enabled
        print(f"[EventSystem] Debug mode {'enabled' if enabled else 'disabled'}")


# Global event system instance
event_system = EventSystem()


# Runtime event constants
class RuntimeEvents:
    """Runtime event type constants"""
    
    # Component events
    COMPONENT_MOUNT = "component:mount"
    COMPONENT_UNMOUNT = "component:unmount"
    COMPONENT_UPDATE = "component:update"
    COMPONENT_RENDER = "component:render"
    COMPONENT_ERROR = "component:error"
    
    # WebSocket events
    WS_CONNECTED = "ws:connected"
    WS_DISCONNECTED = "ws:disconnected"
    WS_MESSAGE = "ws:message"
    WS_ERROR = "ws:error"
    
    # Performance events
    PERFORMANCE_METRIC = "performance:metric"
    RENDER_START = "render:start"
    RENDER_END = "render:end"
    
    # Debug events
    DEBUG_LOG = "debug:log"
    DEBUG_ERROR = "debug:error"
    DEBUG_WARNING = "debug:warning"
    
    # State events
    STATE_CHANGE = "state:change"
    STATE_SYNC = "state:sync"
    
    # User interaction events
    USER_CLICK = "user:click"
    USER_INPUT = "user:input"
    USER_SUBMIT = "user:submit"


def emit_component_event(event_type: str, component_id: str, data: Dict[str, Any]) -> None:
    """Convenience function to emit component events"""
    event_system.emit(event_type, data, source="component", component_id=component_id)


def emit_websocket_event(event_type: str, data: Dict[str, Any]) -> None:
    """Convenience function to emit WebSocket events"""
    event_system.emit(event_type, data, source="websocket")


def emit_performance_event(event_type: str, data: Dict[str, Any]) -> None:
    """Convenience function to emit performance events"""
    event_system.emit(event_type, data, source="performance")


def emit_debug_event(event_type: str, data: Dict[str, Any]) -> None:
    """Convenience function to emit debug events"""
    event_system.emit(event_type, data, source="debug")


# Runtime integration
class RuntimeIntegration:
    """Integration layer for NextPy runtime"""
    
    @staticmethod
    def setup_runtime_hooks():
        """Setup runtime event hooks"""
        
        # Hook into component lifecycle
        def on_component_mount(event):
            emit_component_event(RuntimeEvents.COMPONENT_MOUNT, event.component_id, event.data)
        
        def on_component_update(event):
            emit_component_event(RuntimeEvents.COMPONENT_UPDATE, event.component_id, event.data)
        
        def on_component_error(event):
            emit_component_event(RuntimeEvents.COMPONENT_ERROR, event.component_id, event.data)
        
        # Register hooks
        event_system.on(RuntimeEvents.COMPONENT_MOUNT, on_component_mount)
        event_system.on(RuntimeEvents.COMPONENT_UPDATE, on_component_update)
        event_system.on(RuntimeEvents.COMPONENT_ERROR, on_component_error)
        
        if event_system.debug_mode:
            print("[RuntimeIntegration] Runtime hooks setup complete")
    
    @staticmethod
    def setup_websocket_hooks():
        """Setup WebSocket event hooks"""
        
        def on_ws_connected(event):
            emit_websocket_event(RuntimeEvents.WS_CONNECTED, event.data)
        
        def on_ws_message(event):
            emit_websocket_event(RuntimeEvents.WS_MESSAGE, event.data)
        
        def on_ws_disconnected(event):
            emit_websocket_event(RuntimeEvents.WS_DISCONNECTED, event.data)
        
        # Register hooks
        event_system.on(RuntimeEvents.WS_CONNECTED, on_ws_connected)
        event_system.on(RuntimeEvents.WS_MESSAGE, on_ws_message)
        event_system.on(RuntimeEvents.WS_DISCONNECTED, on_ws_disconnected)
        
        if event_system.debug_mode:
            print("[RuntimeIntegration] WebSocket hooks setup complete")
    
    @staticmethod
    def setup_performance_hooks():
        """Setup performance monitoring hooks"""
        
        def on_render_start(event):
            emit_performance_event(RuntimeEvents.RENDER_START, event.data)
        
        def on_render_end(event):
            emit_performance_event(RuntimeEvents.RENDER_END, event.data)
        
        def on_performance_metric(event):
            emit_performance_event(RuntimeEvents.PERFORMANCE_METRIC, event.data)
        
        # Register hooks
        event_system.on(RuntimeEvents.RENDER_START, on_render_start)
        event_system.on(RuntimeEvents.RENDER_END, on_render_end)
        event_system.on(RuntimeEvents.PERFORMANCE_METRIC, on_performance_metric)
        
        if event_system.debug_mode:
            print("[RuntimeIntegration] Performance hooks setup complete")


# Initialize runtime integration
RuntimeIntegration.setup_runtime_hooks()
RuntimeIntegration.setup_websocket_hooks()
RuntimeIntegration.setup_performance_hooks()
