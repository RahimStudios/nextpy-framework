"""
NextPy Debug Core System
Clean, modular debugging architecture
"""

from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass
import json
import time
import uuid


@dataclass
class DebugSession:
    """Debug session information"""
    session_id: str
    start_time: float
    component_states: Dict[str, Any]
    event_history: List[Dict[str, Any]]
    performance_metrics: Dict[str, Any]
    websocket_state: Dict[str, Any]


class DebugCore:
    """Core debug functionality without UI dependencies"""
    
    def __init__(self):
        self.session: Optional[DebugSession] = None
        self.enabled = False
        self.verbose = False
        self.capture_console = True
        self.capture_performance = True
        self.max_history = 1000
        
    def start_session(self) -> str:
        """Start a new debug session"""
        session_id = str(uuid.uuid4())
        self.session = DebugSession(
            session_id=session_id,
            start_time=time.time(),
            component_states={},
            event_history=[],
            performance_metrics={},
            websocket_state={}
        )
        
        self.enabled = True
        
        if self.verbose:
            print(f"[DebugCore] Started session {session_id}")
        
        return session_id
    
    def end_session(self) -> Optional[Dict[str, Any]]:
        """End current debug session and return summary"""
        if not self.session:
            return None
        
        summary = {
            'session_id': self.session.session_id,
            'duration': time.time() - self.session.start_time,
            'component_count': len(self.session.component_states),
            'event_count': len(self.session.event_history),
            'performance_metrics': self.session.performance_metrics,
            'websocket_state': self.session.websocket_state
        }
        
        if self.verbose:
            print(f"[DebugCore] Ended session {self.session.session_id}")
        
        self.session = None
        self.enabled = False
        
        return summary
    
    def track_component_state(self, component_id: str, state: Dict[str, Any]) -> None:
        """Track component state changes"""
        if not self.session or not self.enabled:
            return
        
        self.session.component_states[component_id] = {
            'state': state,
            'timestamp': time.time(),
            'last_updated': time.time()
        }
        
        if self.verbose:
            print(f"[DebugCore] Tracked state for {component_id}")
    
    def track_event(self, event_type: str, data: Dict[str, Any], source: str = "unknown") -> None:
        """Track runtime events"""
        if not self.session or not self.enabled:
            return
        
        event = {
            'type': event_type,
            'data': data,
            'source': source,
            'timestamp': time.time()
        }
        
        self.session.event_history.append(event)
        
        # Keep history bounded
        if len(self.session.event_history) > self.max_history:
            self.session.event_history.pop(0)
        
        if self.verbose:
            print(f"[DebugCore] Tracked event {event_type} from {source}")
    
    def track_performance(self, metric_name: str, value: Any, metadata: Dict[str, Any] = None) -> None:
        """Track performance metrics"""
        if not self.session or not self.enabled or not self.capture_performance:
            return
        
        self.session.performance_metrics[metric_name] = {
            'value': value,
            'timestamp': time.time(),
            'metadata': metadata or {}
        }
        
        if self.verbose:
            print(f"[DebugCore] Tracked performance {metric_name}: {value}")
    
    def track_websocket_state(self, state: Dict[str, Any]) -> None:
        """Track WebSocket state"""
        if not self.session or not self.enabled:
            return
        
        self.session.websocket_state.update(state)
        self.session.websocket_state['last_updated'] = time.time()
        
        if self.verbose:
            print(f"[DebugCore] Updated WebSocket state: {list(state.keys())}")
    
    def get_component_state(self, component_id: str) -> Optional[Dict[str, Any]]:
        """Get current component state"""
        if not self.session:
            return None
        
        component_info = self.session.component_states.get(component_id)
        return component_info['state'] if component_info else None
    
    def get_all_component_states(self) -> Dict[str, Any]:
        """Get all component states"""
        if not self.session:
            return {}
        
        return {
            comp_id: info['state'] 
            for comp_id, info in self.session.component_states.items()
        }
    
    def get_event_history(self, event_type: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Get event history"""
        if not self.session:
            return []
        
        events = self.session.event_history
        
        if event_type:
            events = [e for e in events if e['type'] == event_type]
        
        return events[-limit:] if events else []
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics"""
        if not self.session:
            return {}
        
        return {
            metric: info['value'] 
            for metric, info in self.session.performance_metrics.items()
        }
    
    def get_websocket_state(self) -> Dict[str, Any]:
        """Get WebSocket state"""
        if not self.session:
            return {}
        
        return self.session.websocket_state.copy()
    
    def export_session_data(self) -> Optional[Dict[str, Any]]:
        """Export complete session data"""
        if not self.session:
            return None
        
        return {
            'session_id': self.session.session_id,
            'start_time': self.session.start_time,
            'component_states': self.session.component_states,
            'event_history': self.session.event_history,
            'performance_metrics': self.session.performance_metrics,
            'websocket_state': self.session.websocket_state,
            'export_timestamp': time.time()
        }
    
    def set_verbose(self, enabled: bool) -> None:
        """Enable/disable verbose logging"""
        self.verbose = enabled
        print(f"[DebugCore] Verbose mode {'enabled' if enabled else 'disabled'}")
    
    def set_capture_console(self, enabled: bool) -> None:
        """Enable/disable console capture"""
        self.capture_console = enabled
        if self.verbose:
            print(f"[DebugCore] Console capture {'enabled' if enabled else 'disabled'}")
    
    def set_capture_performance(self, enabled: bool) -> None:
        """Enable/disable performance capture"""
        self.capture_performance = enabled
        if self.verbose:
            print(f"[DebugCore] Performance capture {'enabled' if enabled else 'disabled'}")
    
    def clear_session_data(self) -> None:
        """Clear all session data"""
        if self.session:
            self.session.component_states.clear()
            self.session.event_history.clear()
            self.session.performance_metrics.clear()
            self.session.websocket_state.clear()
        
        if self.verbose:
            print("[DebugCore] Cleared session data")


# Global debug core instance
debug_core = DebugCore()


# Convenience functions
def start_debug_session() -> str:
    """Start a debug session"""
    return debug_core.start_session()


def end_debug_session() -> Optional[Dict[str, Any]]:
    """End debug session"""
    return debug_core.end_session()


def track_component(component_id: str, state: Dict[str, Any]) -> None:
    """Track component state"""
    debug_core.track_component_state(component_id, state)


def track_event(event_type: str, data: Dict[str, Any], source: str = "unknown") -> None:
    """Track event"""
    debug_core.track_event(event_type, data, source)


def track_performance(metric_name: str, value: Any, metadata: Dict[str, Any] = None) -> None:
    """Track performance metric"""
    debug_core.track_performance(metric_name, value, metadata)


def track_websocket(state: Dict[str, Any]) -> None:
    """Track WebSocket state"""
    debug_core.track_websocket_state(state)


def get_debug_data() -> Optional[Dict[str, Any]]:
    """Get all debug data"""
    return debug_core.export_session_data()
