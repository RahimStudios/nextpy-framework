# WebSocket Support in NextPy

Real-time communication with WebSockets.

## Setup

WebSocket route in FastAPI:

```python
# pages/api/ws.py
from nextpy.websocket import manager

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            await manager.publish(message["channel"], message["payload"])
    finally:
        await manager.disconnect(websocket)
```

## Client Usage

```html
<script>
const ws = new WebSocket('ws://localhost:5000/ws/client1');

ws.onmessage = (event) => {
    const message = JSON.parse(event.data);
    console.log('Received:', message);
};

// Send message
ws.send(JSON.stringify({
    type: 'publish',
    channel: 'chat',
    payload: {text: 'Hello'}
}));
</script>
```

## Features

- **Broadcasting** - Send to all clients
- **Channels** - Pub/sub messaging
- **Real-time** - Instant delivery
- **Async** - Non-blocking connections

## Use Cases

- Live chat
- Notifications
- Live updates
- Multiplayer games
- Real-time dashboards
