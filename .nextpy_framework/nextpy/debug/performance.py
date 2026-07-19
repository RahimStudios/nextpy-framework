"""
NextPy Debug Performance Monitoring
Clean performance tracking without polling
"""

from typing import Dict, Any, Optional, List, Callable
from .core import debug_core
import time
import asyncio
from dataclasses import dataclass


@dataclass
class PerformanceMetric:
    """Performance metric data"""
    name: str
    value: float
    unit: str
    timestamp: float
    metadata: Dict[str, Any]


class PerformanceMonitor:
    """Event-driven performance monitoring"""
    
    def __init__(self):
        self.metrics: Dict[str, PerformanceMetric] = {}
        self.timers: Dict[str, float] = {}
        self.counters: Dict[str, int] = {}
        self.averages: Dict[str, List[float]] = {}
        self.max_average_samples = 100
        self.enabled = True
    
    def start_timer(self, name: str) -> None:
        """Start a performance timer"""
        if not self.enabled:
            return
        
        self.timers[name] = time.perf_counter()
        
        if debug_core.verbose:
            print(f"[Performance] Started timer: {name}")
    
    def end_timer(self, name: str, unit: str = 'ms', metadata: Dict[str, Any] = None) -> Optional[float]:
        """End a performance timer and record the result"""
        if not self.enabled or name not in self.timers:
            return None
        
        start_time = self.timers.pop(name)
        duration = time.perf_counter() - start_time
        
        # Convert to requested unit
        if unit == 'ms':
            duration *= 1000
        elif unit == 'μs':
            duration *= 1000000
        
        self.record_metric(name, duration, unit, metadata)
        return duration
    
    def record_metric(self, name: str, value: float, unit: str = 'count', metadata: Dict[str, Any] = None) -> None:
        """Record a performance metric"""
        if not self.enabled:
            return
        
        metric = PerformanceMetric(
            name=name,
            value=value,
            unit=unit,
            timestamp=time.time(),
            metadata=metadata or {}
        )
        
        self.metrics[name] = metric
        
        # Track averages
        if name not in self.averages:
            self.averages[name] = []
        
        self.averages[name].append(value)
        
        # Keep average samples bounded
        if len(self.averages[name]) > self.max_average_samples:
            self.averages[name].pop(0)
        
        # Track in debug core
        debug_core.track_performance(name, value, metadata)
        
        if debug_core.verbose:
            print(f"[Performance] Recorded {name}: {value} {unit}")
    
    def increment_counter(self, name: str, increment: int = 1) -> None:
        """Increment a performance counter"""
        if not self.enabled:
            return
        
        self.counters[name] = self.counters.get(name, 0) + increment
        self.record_metric(name, self.counters[name], 'count')
    
    def get_metric(self, name: str) -> Optional[PerformanceMetric]:
        """Get a specific metric"""
        return self.metrics.get(name)
    
    def get_average(self, name: str) -> Optional[float]:
        """Get average value for a metric"""
        if name not in self.averages or not self.averages[name]:
            return None
        
        return sum(self.averages[name]) / len(self.averages[name])
    
    def get_all_metrics(self) -> Dict[str, Dict[str, Any]]:
        """Get all current metrics"""
        result = {}
        
        for name, metric in self.metrics.items():
            result[name] = {
                'value': metric.value,
                'unit': metric.unit,
                'timestamp': metric.timestamp,
                'metadata': metric.metadata,
                'average': self.get_average(name)
            }
        
        return result
    
    def get_counters(self) -> Dict[str, int]:
        """Get all counters"""
        return self.counters.copy()
    
    def clear_metrics(self) -> None:
        """Clear all metrics"""
        self.metrics.clear()
        self.timers.clear()
        self.counters.clear()
        self.averages.clear()
        
        if debug_core.verbose:
            print("[Performance] Cleared all metrics")
    
    def set_enabled(self, enabled: bool) -> None:
        """Enable/disable performance monitoring"""
        self.enabled = enabled
        if debug_core.verbose:
            print(f"[Performance] {'Enabled' if enabled else 'Disabled'}")


# Global performance monitor
performance_monitor = PerformanceMonitor()


class PerformanceHooks:
    """Performance monitoring hooks"""
    
    @staticmethod
    def create_render_monitor():
        """Create render performance monitor"""
        
        def start_render(component_id: str = None):
            """Start render timing"""
            timer_name = f"render_{component_id or 'global'}"
            performance_monitor.start_timer(timer_name)
        
        def end_render(component_id: str = None, node_count: int = None):
            """End render timing"""
            timer_name = f"render_{component_id or 'global'}"
            metadata = {'component_id': component_id} if component_id else {}
            if node_count is not None:
                metadata['node_count'] = node_count
            
            duration = performance_monitor.end_timer(timer_name, 'ms', metadata)
            
            # Track render rate
            if duration:
                performance_monitor.record_metric('render_rate', 1000 / duration if duration > 0 else 0, 'fps')
        
        return start_render, end_render
    
    @staticmethod
    def create_component_monitor():
        """Create component lifecycle monitor"""
        
        def track_component_mount(component_id: str, props: Dict[str, Any] = None):
            """Track component mounting"""
            performance_monitor.increment_counter('components_mounted')
            performance_monitor.record_metric(
                f'component_mount_{component_id}',
                time.time(),
                'timestamp',
                {'props': props} if props else {}
            )
        
        def track_component_unmount(component_id: str):
            """Track component unmounting"""
            performance_monitor.increment_counter('components_unmounted')
            performance_monitor.record_metric(
                f'component_unmount_{component_id}',
                time.time(),
                'timestamp'
            )
        
        def track_component_update(component_id: str, update_type: str = 'state'):
            """Track component updates"""
            performance_monitor.increment_counter('components_updated')
            performance_monitor.increment_counter(f'updates_{update_type}')
        
        return track_component_mount, track_component_unmount, track_component_update
    
    @staticmethod
    def create_memory_monitor():
        """Create memory usage monitor"""
        
        def track_memory_usage():
            """Track current memory usage"""
            try:
                import gc
                import sys
                
                # Get basic memory info
                gc.collect()  # Force garbage collection
                
                # Try to get more detailed memory info if available
                try:
                    import psutil
                    process = psutil.Process()
                    memory_info = process.memory_info()
                    
                    performance_monitor.record_metric('memory_rss', memory_info.rss, 'bytes')
                    performance_monitor.record_metric('memory_vms', memory_info.vms, 'bytes')
                    
                except ImportError:
                    # Fallback to basic Python memory tracking
                    objects = len(gc.get_objects())
                    performance_monitor.record_metric('python_objects', objects, 'count')
                
            except Exception as e:
                debug_core.track_event('memory_monitor_error', {'error': str(e)}, 'performance')
        
        return track_memory_usage
    
    @staticmethod
    def create_network_monitor():
        """Create network performance monitor"""
        
        def track_request(url: str, method: str = 'GET', status_code: int = None, duration: float = None):
            """Track network request"""
            metadata = {
                'url': url,
                'method': method
            }
            
            if status_code:
                metadata['status_code'] = status_code
            
            if duration:
                performance_monitor.record_metric('network_request_duration', duration, 'ms', metadata)
            
            performance_monitor.increment_counter('network_requests')
            
            if status_code:
                if 200 <= status_code < 300:
                    performance_monitor.increment_counter('network_success')
                elif 400 <= status_code < 500:
                    performance_monitor.increment_counter('network_client_errors')
                elif 500 <= status_code < 600:
                    performance_monitor.increment_counter('network_server_errors')
        
        def track_response_size(size: int, content_type: str = None):
            """Track response size"""
            metadata = {'content_type': content_type} if content_type else {}
            performance_monitor.record_metric('network_response_size', size, 'bytes', metadata)
        
        return track_request, track_response_size


# Install performance hooks
def install_performance_hooks():
    """Install all performance monitoring hooks"""
    
    # Render monitoring
    start_render, end_render = PerformanceHooks.create_render_monitor()
    
    # Component monitoring
    mount_component, unmount_component, update_component = PerformanceHooks.create_component_monitor()
    
    # Memory monitoring
    track_memory = PerformanceHooks.create_memory_monitor()
    
    # Network monitoring
    track_request, track_response = PerformanceHooks.create_network_monitor()
    
    # Return hook functions for external use
    return {
        'render': {
            'start': start_render,
            'end': end_render
        },
        'component': {
            'mount': mount_component,
            'unmount': unmount_component,
            'update': update_component
        },
        'memory': {
            'track': track_memory
        },
        'network': {
            'request': track_request,
            'response': track_response
        }
    }


# Convenience functions
def start_timer(name: str) -> None:
    """Start a performance timer"""
    performance_monitor.start_timer(name)


def end_timer(name: str, unit: str = 'ms', metadata: Dict[str, Any] = None) -> Optional[float]:
    """End a performance timer"""
    return performance_monitor.end_timer(name, unit, metadata)


def record_metric(name: str, value: float, unit: str = 'count', metadata: Dict[str, Any] = None) -> None:
    """Record a performance metric"""
    performance_monitor.record_metric(name, value, unit, metadata)


def increment_counter(name: str, increment: int = 1) -> None:
    """Increment a performance counter"""
    performance_monitor.increment_counter(name, increment)


def get_performance_data() -> Dict[str, Any]:
    """Get all performance data"""
    return {
        'metrics': performance_monitor.get_all_metrics(),
        'counters': performance_monitor.get_counters(),
        'averages': {name: performance_monitor.get_average(name) for name in performance_monitor.averages}
    }


# Install hooks on import
performance_hooks = install_performance_hooks()
