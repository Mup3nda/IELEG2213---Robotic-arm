import asyncio
import websockets

connected_clients = set()

async def handler(websocket, path):
    # Register the new client
    connected_clients.add(websocket)
    try:
        # Listen for messages from clients
        async for message in websocket:
            print(f"Received message: {message}")
            print(message[-1])

            for client in connected_clients:
                await client.send(message)
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")
    finally:
        # Unregister the client when it disconnects
        connected_clients.remove(websocket)

async def main():
    async with websockets.serve(handler, "192.168.0.135", 9000) as server: #Didier ABS
    #async with websockets.serve(handler, "192.168.0.178", 9000) as server: #Abdi
        print("WebSocket server started on port 9000")
        await asyncio.get_running_loop().create_future()

asyncio.run(main())
