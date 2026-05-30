"""
NextPy Debug WebSocket Integration
Clean WebSocket monitoring and tracking
"""

from typing import Dict, Any, Optional, Callable
from .core import debug_core
import time
import asyncio


class WebSocketTracker:
    """Clean WebSocket state tracking"""
    
    def __init__(self):
        self.current_state = {
            'connected': False,
            'client_id': None,
            'connection_time': None,
            'last_message_time': None,
            'message_count': 0,
            'error_count': 0,
            'reconnect_count': 0,
            'url': None,
            'protocol': None
        }
        self.message_history = []
        self.max_history = 100
    
    def track_connection(self, client_id: str, url: str, protocol: str = None) -> None:
        """Track WebSocket connection"""
        self.current_state.update({
            'connected': True,
            'client_id': client_id,
            'connection_time': time.time(),
            'url': url,
            'protocol': protocol
        })
        
        debug_core.track_websocket_state({
            'event': 'connected',
            'client_id': client_id,
            'url': url,
            'timestamp': time.time()
        })
    
    def track_disconnection(self, reason: str = None) -> None:
        """Track WebSocket disconnection"""
        self.current_state.update({
            'connected': False,
            'disconnection_time': time.time(),
            'disconnection_reason': reason
        })
        
        debug_core.track_websocket_state({
            'event': 'disconnected',
            'reason': reason,
            'timestamp': time.time()
        })
    
    def track_message(self, message_type: str, data: Dict[str, Any], direction: str = 'outgoing') -> None:
        """Track WebSocket message"""
        message_info = {
            'type': message_type,
            'data': data,
            'direction': direction,
            'timestamp': time.time(),
            'size': len(str(data))
        }
        
        self.message_history.append(message_info)
        self.current_state['last_message_time'] = time.time()
        self.current_state['message_count'] += 1
        
        # Keep history bounded
        if len(self.message_history) > self.max_history:
            self.message_history.pop(0)
        
        debug_core.track_websocket_state({
            'event': 'message',
            'message_type': message_type,
            'direction': direction,
            'size': message_info['size'],
            'timestamp': time.time()
        })
    
    def track_error(self, error: Exception, context: str = None) -> None:
        """Track WebSocket error"""
        self.current_state['error_count'] += 1
        
        debug_core.track_websocket_state({
            'event': 'error',
            'error_type': type(error).__name__,
            'error_message': str(error),
            'context': context,
            'timestamp': time.time()
        })
    
    def track_reconnection(self) -> None:
        """Track WebSocket reconnection attempt"""
        self.current_state['reconnect_count'] += 1
        
        debug_core.track_websocket_state({
            'event': 'reconnection_attempt',
            'attempt_count': self.current_state['reconnect_count'],
            'timestamp': time.time()
        })
    
    def get_state(self) -> Dict[str, Any]:
        """Get current WebSocket state"""
        return self.current_state.copy()
    
    def get_recent_messages(self, limit: int = 20) -> list:
        """Get recent messages"""
        return self.message_history[-limit:] if self.message_history else []
    
    def get_connection_duration(self) -> Optional[float]:
        """Get connection duration in seconds"""
        if not self.current_state['connected'] or not self.current_state['connection_time']:
            return None
        
        return time.time() - self.current_state['connection_time']
    
    def get_message_rate(self) -> float:
        """Get messages per second"""
        duration = self.get_connection_duration()
        if not duration or duration == 0:
            return 0.0
        
        return self.current_state['message_count'] / duration


# Global WebSocket tracker
ws_tracker = WebSocketTracker()


class WebSocketHooks:
    """WebSocket integration hooks"""
    
    @staticmethod
    def create_websocket_wrapper(original_websocket_class) -> type:
        """Create a wrapped WebSocket class for debugging"""
        
        class DebugWebSocket:
            def __init__(self, url, protocols=None, extensions=None):
                self._ws = original_websocket_class(url, protocols, extensions)
                self._url = url
                self._protocols = protocols
                self._client_id = None
                self._setup_hooks()
            
            def _setup_hooks(self):
                """Setup debugging hooks"""
                # Override event handlers if they exist
                if hasattr(self._ws, 'addEventListener'):
                    original_add_listener = self._ws.addEventListener
                    original_remove_listener = self._ws.removeEventListener
                    
                    def add_listener_wrapper(event, callback):
                        if event == 'open':
                            wrapped_callback = self._create_open_wrapper(callback)
                        elif event == 'close':
                            wrapped_callback = self._create_close_wrapper(callback)
                        elif event == 'message':
                            wrapped_callback = self._create_message_wrapper(callback)
                        elif event == 'error':
                            wrapped_callback = self._create_error_wrapper(callback)
                        else:
                            wrapped_callback = callback
                        
                        return original_add_listener.call(self._ws, event, wrapped_callback)
                    
                    def remove_listener_wrapper(event, callback):
                        return original_remove_listener.call(self._ws, event, callback)
                    
                    self._ws.addEventListener = add_listener_wrapper
                    self._ws.removeEventListener = remove_listener_wrapper
            
            def _create_open_wrapper(self, original_callback):
                """Create wrapper for open event"""
                def wrapper(event):
                    # Generate client ID
                    import uuid
                    self._client_id = str(uuid.uuid4())[:8]
                    
                    # Track connection
                    ws_tracker.track_connection(
                        self._client_id, 
                        self._url,
                        str(self._protocols) if self._protocols else None
                    )
                    
                    # Call original callback
                    if original_callback:
                        original_callback(event)
                
                return wrapper
            
            def _create_close_wrapper(self, original_callback):
                """Create wrapper for close event"""
                def wrapper(event):
                    # Track disconnection
                    reason = getattr(event, 'reason', None) or getattr(event, 'code', 'Unknown')
                    ws_tracker.track_disconnection(str(reason))
                    
                    # Call original callback
                    if original_callback:
                        original_callback(event)
                
                return wrapper
            
            def _create_message_wrapper(self, original_callback):
                """Create wrapper for message event"""
                def wrapper(event):
                    # Track incoming message
                    try:
                        data = getattr(event, 'data', None)
                        if data:
                            if isinstance(data, str):
                                try:
                                    import json
                                    parsed_data = json.loads(data)
                                    message_type = parsed_data.get('type', 'unknown')
                                except:
                                    message_type = 'text'
                                    parsed_data = {'raw': data}
                            else:
                                message_type = 'binary'
                                parsed_data = {'binary': str(data)[:100]}
                            
                            ws_tracker.track_message(message_type, parsed_data, 'incoming')
                    except Exception as e:
                        ws_tracker.track_error(e, 'message_tracking')
                    
                    # Call original callback
                    if original_callback:
                        original_callback(event)
                
                return wrapper
            
            def _create_error_wrapper(self, original_callback):
                """Create wrapper for error event"""
                def wrapper(event):
                    # Track error
                    error = getattr(event, 'error', event)
                    ws_tracker.track_error(error, 'websocket_error')
                    
                    # Call original callback
                    if original_callback:
                        original_callback(event)
                
                return wrapper
            
            def send(self, data):
                """Track outgoing messages"""
                try:
                    if isinstance(data, str):
                        try:
                            import json
                            parsed_data = json.loads(data)
                            message_type = parsed_data.get('type', 'unknown')
                        except:
                            message_type = 'text'
                            parsed_data = {'raw': data}
                    else:
                        message_type = 'binary'
                        parsed_data = {'binary': str(data)[:100]}
                    
                    ws_tracker.track_message(message_type, parsed_data, 'outgoing')
                except Exception as e:
                    ws_tracker.track_error(e, 'send_tracking')
                
                return self._ws.send(data)
            
            def close(self, code=None, reason=None):
                """Track close"""
                ws_tracker.track_disconnection(reason or str(code) if code else 'Manual close')
                return self._ws.close(code, reason)
            
            # Delegate all other attributes and methods
            def __getattr__(self, name):
                return getattr(self._ws, name)
        
        return DebugWebSocket
    
    @staticmethod
    def install_hooks():
        """Install WebSocket hooks globally"""
        try:
            # Try to patch the browser WebSocket
            import js
            original_websocket = js.WebSocket
            js.WebSocket = WebSocketHooks.create_websocket_wrapper(original_websocket)
            return True
        except ImportError:
            # Not in browser environment
            return False
        except Exception as e:
            debug_core.track_event('websocket_hook_error', {'error': str(e)}, 'debug')
            return False


# Performance monitoring for WebSocket
class WebSocketPerformanceMonitor:
    """WebSocket performance monitoring"""
    
    def __init__(self):
        self.metrics = {
            'connection_time': None,
            'first_message_time': None,
            'total_bytes_sent': 0,
            'total_bytes_received': 0,
            'latency_samples': [],
            'error_rate': 0.0
        }
    
    def track_connection_time(self, duration: float) -> None:
        """Track connection establishment time"""
        self.metrics['connection_time'] = duration
        debug_core.track_performance('ws_connection_time', duration)
    
    def track_first_message_latency(self, latency: float) -> None:
        """Track time to first message"""
        self.metrics['first_message_time'] = latency
        debug_core.track_performance('ws_first_message_latency', latency)
    
    def track_bytes(self, bytes_count: int, direction: str) -> None:
        """Track bytes transferred"""
        if direction == 'outgoing':
            self.metrics['total_bytes_sent'] += bytes_count
            debug_core.track_performance('ws_bytes_sent', self.metrics['total_bytes_sent'])
        else:
            self.metrics['total_bytes_received'] += bytes_count
            debug_core.track_performance('ws_bytes_received', self.metrics['total_bytes_received'])
    
    def track_latency(self, latency: float) -> None:
        """Track message latency"""
        self.metrics['latency_samples'].append(latency)
        
        # Keep only last 100 samples
        if len(self.metrics['latency_samples']) > 100:
            self.metrics['latency_samples'].pop(0)
        
        # Calculate average latency
        avg_latency = sum(self.metrics['latency_samples']) / len(self.metrics['latency_samples'])
        debug_core.track_performance('ws_avg_latency', avg_latency)
    
    def calculate_error_rate(self) -> float:
        """Calculate error rate"""
        state = ws_tracker.get_state()
        total_messages = state['message_count']
        total_errors = state['error_count']
        
        if total_messages == 0:
            self.metrics['error_rate'] = 0.0
        else:
            self.metrics['error_rate'] = total_errors / total_messages
        
        debug_core.track_performance('ws_error_rate', self.metrics['error_rate'])
        return self.metrics['error_rate']


# Global performance monitor
ws_performance = WebSocketPerformanceMonitor()


# Convenience functions
def get_websocket_state() -> Dict[str, Any]:
    """Get current WebSocket state"""
    return ws_tracker.get_state()


def get_websocket_metrics() -> Dict[str, Any]:
    """Get WebSocket performance metrics"""
    return {
        'state': ws_tracker.get_state(),
        'performance': ws_performance.metrics,
        'recent_messages': ws_tracker.get_recent_messages(10)
    }


def install_websocket_debugging() -> bool:
    """Install WebSocket debugging hooks"""
    return WebSocketHooks.install_hooks()
