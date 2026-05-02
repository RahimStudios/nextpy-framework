"""
NextPy WebSocket Support
Real-time communication with clients
"""

from fastapi import WebSocket
from starlette.websockets import WebSocketState, WebSocketDisconnect
from typing import Set, Dict, Callable, Any, List
import json
import asyncio


class ConnectionManager:
    """Enhanced WebSocket connection manager with client IDs and structured events"""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}  # client_id -> websocket
        self.connection_metadata: Dict[str, Dict[str, Any]] = {}  # client_id -> metadata
        self.subscribers: Dict[str, Set[str]] = {}  # channel -> set of client_ids
        self.client_counter = 0
        self.component_states: Dict[str, Dict[str, Any]] = {}  # component_id -> state
    
    def _generate_client_id(self) -> str:
        """Generate unique client ID"""
        self.client_counter += 1
        return f"client_{self.client_counter}_{int(asyncio.get_event_loop().time())}"
    
    async def connect(self, websocket: WebSocket, metadata: Dict[str, Any] = None) -> str:
        """Accept new connection and return client ID"""
        await websocket.accept()
        client_id = self._generate_client_id()
        
        self.active_connections[client_id] = websocket
        self.connection_metadata[client_id] = metadata or {}
        
        # Send welcome event with current component states
        await self.send_to_client(client_id, {
            "type": "CONNECTION_ESTABLISHED",
            "payload": {
                "client_id": client_id,
                "timestamp": int(asyncio.get_event_loop().time()),
                "component_states": self.component_states
            }
        })
        
        return client_id
    
    async def disconnect(self, client_id: str):
        """Remove connection by client ID"""
        if client_id in self.active_connections:
            del self.active_connections[client_id]
        if client_id in self.connection_metadata:
            del self.connection_metadata[client_id]
        
        # Remove from all subscriptions
        for channel_subs in self.subscribers.values():
            channel_subs.discard(client_id)
    
    async def send_to_client(self, client_id: str, event: Dict[str, Any]):
        """Send structured event to specific client"""
        if client_id in self.active_connections:
            try:
                websocket = self.active_connections[client_id]
                await websocket.send_json(event)
            except:
                # Connection broken, remove it
                await self.disconnect(client_id)
    
    async def broadcast(self, event: Dict[str, Any]):
        """Send event to all connected clients"""
        for client_id in list(self.active_connections.keys()):
            await self.send_to_client(client_id, event)
    
    async def subscribe(self, client_id: str, channel: str):
        """Subscribe client to channel"""
        if channel not in self.subscribers:
            self.subscribers[channel] = set()
        self.subscribers[channel].add(client_id)
        
        # Confirm subscription
        await self.send_to_client(client_id, {
            "type": "SUBSCRIPTION_CONFIRMED",
            "payload": {
                "channel": channel
            }
        })
    
    async def publish(self, channel: str, event: Dict[str, Any]):
        """Publish event to channel subscribers"""
        if channel in self.subscribers:
            for client_id in self.subscribers[channel]:
                await self.send_to_client(client_id, event)
    
    async def emit_state_update(self, component_id: str, state: Dict[str, Any]):
        """Emit structured state update event and store state"""
        # Store the component state
        self.component_states[component_id] = state
        
        event = {
            "type": "STATE_UPDATE",
            "component_id": component_id,
            "payload": state,
            "timestamp": int(asyncio.get_event_loop().time())
        }
        await self.broadcast(event)
    
    async def emit_component_event(self, component_id: str, event_name: str, data: Dict[str, Any]):
        """Emit component-specific event"""
        event = {
            "type": "COMPONENT_EVENT",
            "component_id": component_id,
            "event_name": event_name,
            "payload": data,
            "timestamp": int(asyncio.get_event_loop().time())
        }
        await self.broadcast(event)
    
    async def emit_ui_update(self, component_id: str, update_type: str, data: Dict[str, Any]):
        """Emit server-driven UI update"""
        event = {
            "type": "UI_UPDATE",
            "component_id": component_id,
            "update_type": update_type,
            "payload": data,
            "timestamp": int(asyncio.get_event_loop().time())
        }
        await self.broadcast(event)
    
    def get_connected_clients(self) -> List[str]:
        """Get list of connected client IDs"""
        return list(self.active_connections.keys())
    
    def get_client_metadata(self, client_id: str) -> Dict[str, Any]:
        """Get metadata for a specific client"""
        return self.connection_metadata.get(client_id, {})
    
    def get_component_state(self, component_id: str) -> Dict[str, Any]:
        """Get current state of a component"""
        return self.component_states.get(component_id, {})


# Global manager instance
manager = ConnectionManager()


async def broadcast_error(error_data: Dict[str, Any]):
    """Broadcast error message to all connected clients"""
    await manager.broadcast(error_data)


async def handle_websocket(websocket: WebSocket):
    """Enhanced WebSocket handler with client ID support and multi-user sync"""
    client_id = None
    try:
        # Connect and get client ID
        client_id = await manager.connect(websocket, {
            "user_agent": websocket.headers.get("user-agent", "unknown"),
            "connected_at": int(asyncio.get_event_loop().time())
        })
        
        # Main message loop
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Route message to appropriate handler
            msg_type = message.get("type")
            
            if msg_type == "subscribe":
                await manager.subscribe(client_id, message.get("channel"))
            
            elif msg_type == "publish":
                await manager.publish(message.get("channel"), message.get("payload"))
            
            elif msg_type == "broadcast":
                await manager.broadcast(message.get("payload"))
            
            elif msg_type == "state_update":
                # Handle client-side state updates for multi-user sync
                component_id = message.get("component_id")
                state = message.get("payload")
                if component_id and state:
                    await manager.emit_state_update(component_id, state)
            
            elif msg_type == "component_event":
                # Handle component events (clicks, form submissions, etc.)
                component_id = message.get("component_id")
                event_name = message.get("event_name")
                data = message.get("payload", {})
                if component_id and event_name:
                    await manager.emit_component_event(component_id, event_name, data)
            
            elif msg_type == "sync_request":
                # Handle multi-user sync requests
                component_id = message.get("component_id")
                if component_id:
                    current_state = manager.get_component_state(component_id)
                    await manager.send_to_client(client_id, {
                        "type": "SYNC_RESPONSE",
                        "component_id": component_id,
                        "payload": current_state,
                        "timestamp": int(asyncio.get_event_loop().time())
                    })
            
            elif msg_type == "ping":
                # Handle ping for connection health check
                await manager.send_to_client(client_id, {
                    "type": "pong",
                    "timestamp": int(asyncio.get_event_loop().time())
                })
            
            elif msg_type == "error":
                # Handle error messages for development overlay
                error_data = message.get("payload", {})
                error_data["client_id"] = client_id  # Add client ID for tracking
                await manager.broadcast({
                    "type": "ERROR_BROADCAST",
                    "payload": error_data
                })
    
    except WebSocketDisconnect:
        # Client disconnected gracefully
        if client_id:
            await manager.disconnect(client_id)
    
    except Exception as e:
        # Handle errors gracefully
        if client_id:
            try:
                await manager.send_to_client(client_id, {
                    "type": "ERROR",
                    "message": f"WebSocket error: {str(e)}",
                    "timestamp": int(asyncio.get_event_loop().time())
                })
            except:
                pass
        if client_id:
            await manager.disconnect(client_id)
