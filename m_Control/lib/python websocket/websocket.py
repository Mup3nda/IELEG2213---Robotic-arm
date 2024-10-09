import asyncio
from websockets import serve

# Set to store connected clients
connected_clients = set()

async def echo(websocket, path):
    # Register client
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            # Echo the received message back to the client
            await websocket.send(message)
    finally:
        # Unregister client
        connected_clients.remove(websocket)

async def broadcast_message(message):
    # Send a message to all connected clients
    if connected_clients:  # Check if there are any connected clients
        await asyncio.wait([client.send(message) for client in connected_clients])

async def main():
    async with serve(echo, "10.24.106.132", 8765):
        await asyncio.get_running_loop().create_future()  # run forever

# Start the WebSocket server
asyncio.run(main())

# Example usage: Broadcast a message to all clients after 10 seconds
async def example_broadcast():
    await asyncio.sleep(10)
    await broadcast_message("Hello, clients!")

# Run the example broadcast in the event loop
asyncio.run(example_broadcast())