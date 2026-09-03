"""
NextPy State Synchronization - Enhanced Client-Server State Management
Provides seamless state synchronization between client components and server
"""

import asyncio
import json
from typing import Any, Callable, Dict, Optional, Set, List
from datetime import datetime
from dataclasses import dataclass, field

from nextpy.websocket import manager


@dataclass
class StateSubscription:
    """Represents a subscription to state changes"""
    channel: str
    callback: Callable
    filters: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StateSnapshot:
    """Represents a snapshot of state at a point in time"""
    data: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.utcnow)
    version: int = 0


class StateManager:
    """
    Centralized state management with synchronization capabilities
    Handles client-server state synchronization with WebSocket support
    """
    
    def __init__(self):
        self._state: Dict[str, Any] = {}
        self._subscriptions: Dict[str, List[StateSubscription]] = {}
        self._history: List[StateSnapshot] = []
        self._version = 0
        self._locks: Dict[str, asyncio.Lock] = {}
    
    def get_lock(self, key: str) -> asyncio.Lock:
        """Get or create a lock for a specific state key"""
        if key not in self._locks:
            self._locks[key] = asyncio.Lock()
        return self._locks[key]
    
    async def get(self, key: str, default: Any = None) -> Any:
        """Get state value"""
        return self._state.get(key, default)
    
    async def set(self, key: str, value: Any, broadcast: bool = True) -> None:
        """
        Set state value and optionally broadcast changes
        
        Args:
            key: State key
            value: New value
            broadcast: Whether to broadcast changes to subscribers
        """
        async with self.get_lock(key):
            old_value = self._state.get(key)
            self._state[key] = value
            self._version += 1
            
            # Create snapshot
            snapshot = StateSnapshot(
                data={key: value},
                timestamp=datetime.utcnow(),
                version=self._version
            )
            self._history.append(snapshot)
            
            # Keep only last 100 snapshots
            if len(self._history) > 100:
                self._history.pop(0)
            
            if broadcast:
                await self._notify_subscribers(key, old_value, value)
    
    async def update(self, key: str, updater: Callable[[Any], Any]) -> Any:
        """
        Update state value using a function
        
        Args:
            key: State key
            updater: Function that takes current value and returns new value
            
        Returns:
            New value
        """
        async with self.get_lock(key):
            current = await self.get(key)
            new_value = updater(current)
            await self.set(key, new_value)
            return new_value
    
    async def delete(self, key: str, broadcast: bool = True) -> None:
        """Delete state key"""
        async with self.get_lock(key):
            if key in self._state:
                old_value = self._state.pop(key)
                self._version += 1
                
                if broadcast:
                    await self._notify_subscribers(key, old_value, None)
    
    async def subscribe(self, channel: str, callback: Callable, filters: Dict[str, Any] = None) -> str:
        """
        Subscribe to state changes
        
        Args:
            channel: Channel name to subscribe to
            callback: Callback function to call on changes
            filters: Optional filters for subscription
            
        Returns:
            Subscription ID
        """
        if filters is None:
            filters = {}
        
        subscription = StateSubscription(
            channel=channel,
            callback=callback,
            filters=filters
        )
        
        if channel not in self._subscriptions:
            self._subscriptions[channel] = []
        
        self._subscriptions[channel].append(subscription)
        return f"{channel}_{len(self._subscriptions[channel])}"
    
    async def unsubscribe(self, subscription_id: str) -> None:
        """Unsubscribe from state changes"""
        channel, index = subscription_id.rsplit('_', 1)
        if channel in self._subscriptions:
            try:
                index = int(index)
                if 0 <= index < len(self._subscriptions[channel]):
                    self._subscriptions[channel].pop(index)
            except (ValueError, IndexError):
                pass
    
    async def _notify_subscribers(self, key: str, old_value: Any, new_value: Any) -> None:
        """Notify subscribers of state changes"""
        # Broadcast via WebSocket
        try:
            await manager.broadcast({
                "type": "STATE_CHANGE",
                "key": key,
                "old_value": old_value,
                "new_value": new_value,
                "timestamp": datetime.utcnow().isoformat(),
                "version": self._version
            })
        except Exception as e:
            print(f"WebSocket broadcast failed: {e}")
        
        # Call local subscribers
        for channel, subscriptions in self._subscriptions.items():
            for subscription in subscriptions:
                try:
                    # Check filters
                    if subscription.filters:
                        if not self._matches_filters(key, subscription.filters):
                            continue
                    
                    # Call callback
                    if asyncio.iscoroutinefunction(subscription.callback):
                        await subscription.callback(key, old_value, new_value)
                    else:
                        subscription.callback(key, old_value, new_value)
                except Exception as e:
                    print(f"Subscription callback failed: {e}")
    
    def _matches_filters(self, key: str, filters: Dict[str, Any]) -> bool:
        """Check if key matches subscription filters"""
        if 'key_pattern' in filters:
            import re
            pattern = filters['key_pattern']
            return re.match(pattern, key) is not None
        if 'keys' in filters:
            return key in filters['keys']
        return True
    
    async def get_snapshot(self, version: Optional[int] = None) -> StateSnapshot:
        """Get a state snapshot at a specific version"""
        if version is None:
            return StateSnapshot(data=self._state.copy(), version=self._version)
        
        for snapshot in reversed(self._history):
            if snapshot.version == version:
                return snapshot
        
        return StateSnapshot(data=self._state.copy(), version=self._version)
    
    async def get_history(self, limit: int = 10) -> List[StateSnapshot]:
        """Get state change history"""
        return self._history[-limit:]
    
    def get_version(self) -> int:
        """Get current state version"""
        return self._version
    
    async def export_state(self) -> Dict[str, Any]:
        """Export entire state"""
        return {
            "state": self._state.copy(),
            "version": self._version,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def import_state(self, state_data: Dict[str, Any], merge: bool = True) -> None:
        """
        Import state from exported data
        
        Args:
            state_data: State data to import
            merge: Whether to merge with existing state or replace
        """
        if merge:
            self._state.update(state_data.get("state", {}))
        else:
            self._state = state_data.get("state", {}).copy()
        
        self._version = state_data.get("version", self._version + 1)


# Global state manager instance
_global_state_manager: Optional[StateManager] = None


def get_state_manager() -> StateManager:
    """Get the global state manager instance"""
    global _global_state_manager
    if _global_state_manager is None:
        _global_state_manager = StateManager()
    return _global_state_manager


# Convenience functions for common state operations
async def get_state(key: str, default: Any = None) -> Any:
    """Get state value using global manager"""
    manager = get_state_manager()
    return await manager.get(key, default)


async def set_state(key: str, value: Any, broadcast: bool = True) -> None:
    """Set state value using global manager"""
    manager = get_state_manager()
    await manager.set(key, value, broadcast)


async def update_state(key: str, updater: Callable[[Any], Any]) -> Any:
    """Update state value using global manager"""
    manager = get_state_manager()
    return await manager.update(key, updater)


async def delete_state(key: str, broadcast: bool = True) -> None:
    """Delete state key using global manager"""
    manager = get_state_manager()
    await manager.delete(key, broadcast)


# React-like hooks for state management
class ServerState:
    """Server-side state hook similar to React useState"""
    
    def __init__(self, key: str, initial_value: Any = None):
        self.key = key
        self.initial_value = initial_value
        self._subscribers: Set[Callable] = set()
    
    async def get(self) -> Any:
        """Get current state value"""
        manager = get_state_manager()
        value = await manager.get(self.key, self.initial_value)
        return value
    
    async def set(self, value: Any) -> None:
        """Set state value and notify subscribers"""
        manager = get_state_manager()
        await manager.set(self.key, value)
        
        # Notify local subscribers
        for callback in self._subscribers:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(value)
                else:
                    callback(value)
            except Exception as e:
                print(f"State subscriber callback failed: {e}")
    
    def subscribe(self, callback: Callable) -> Callable:
        """
        Subscribe to state changes
        
        Returns:
            Unsubscribe function
        """
        self._subscribers.add(callback)
        
        def unsubscribe():
            self._subscribers.discard(callback)
        
        return unsubscribe
    
    async def use(self) -> tuple[Any, Callable]:
        """
        React-like hook interface
        
        Returns:
            Tuple of (current_value, setter_function)
        """
        current = await self.get()
        return current, self.set


# Database-backed state persistence
class DatabaseState:
    """State manager with database persistence"""
    
    def __init__(self, table_name: str = "app_state"):
        self.table_name = table_name
        self._cache: Dict[str, Any] = {}
    
    async def initialize(self):
        """Initialize database table for state storage"""
        from nextpy.db import Base, get_session
        from sqlalchemy import Column, String, Text, DateTime
        from sqlalchemy import text
        
        # Create table if it doesn't exist
        session = get_session()
        try:
            session.execute(text(f"""
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                    key VARCHAR(255) PRIMARY KEY,
                    value TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            session.commit()
        finally:
            session.close()
    
    async def get(self, key: str, default: Any = None) -> Any:
        """Get state from database"""
        from nextpy.db import get_session
        from sqlalchemy import text
        
        # Check cache first
        if key in self._cache:
            return self._cache[key]
        
        session = get_session()
        try:
            result = session.execute(
                text(f"SELECT value FROM {self.table_name} WHERE key = :key"),
                {"key": key}
            ).fetchone()
            
            if result:
                value = json.loads(result[0])
                self._cache[key] = value
                return value
            
            return default
        finally:
            session.close()
    
    async def set(self, key: str, value: Any) -> None:
        """Set state in database"""
        from nextpy.db import get_session
        from sqlalchemy import text
        
        session = get_session()
        try:
            serialized = json.dumps(value)
            session.execute(
                text(f"""
                    INSERT INTO {self.table_name} (key, value, updated_at)
                    VALUES (:key, :value, CURRENT_TIMESTAMP)
                    ON CONFLICT (key) DO UPDATE SET
                        value = :value,
                        updated_at = CURRENT_TIMESTAMP
                """),
                {"key": key, "value": serialized}
            )
            session.commit()
            
            # Update cache
            self._cache[key] = value
        finally:
            session.close()
    
    async def delete(self, key: str) -> None:
        """Delete state from database"""
        from nextpy.db import get_session
        from sqlalchemy import text
        
        session = get_session()
        try:
            session.execute(
                text(f"DELETE FROM {self.table_name} WHERE key = :key"),
                {"key": key}
            )
            session.commit()
            
            # Remove from cache
            if key in self._cache:
                del self._cache[key]
        finally:
            session.close()


__all__ = [
    'StateManager',
    'StateSubscription',
    'StateSnapshot',
    'get_state_manager',
    'get_state',
    'set_state',
    'update_state',
    'delete_state',
    'ServerState',
    'DatabaseState',
]