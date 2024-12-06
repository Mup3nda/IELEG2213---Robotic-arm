import asyncio
import websockets

async def handle_client(websocket, path):
    
    while True:
        data = await websocket.recv()
        x, y, z = data.split(',')
        print(f"Received coordinates: x={x}, y={y}, z={z}")

start_server = websockets.serve(handle_client, "0.0.0.0", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
print("Started Websocket..")
asyncio.get_event_loop().run_forever()