import asyncio
import websockets

async def handle_client(websocket, path):
    print("Client connected")
    while True:
        try:
            # Receive data from the websocket
            data = await websocket.recv()
            
            # Split the received data by commas
            parts = data.split(',')
            
            # Check if the first part is "C" to identify computer vision data
            if parts[0] == "C" and len(parts) == 4:
                # Extract x, y, z values
                x = int(parts[1])
                y = int(parts[2])
                z = int(parts[3])
                print(f"Received coordinates from Computer Vision: x={x}, y={y}, z={z}")
            else:
                print("Received unknown data format")
        
        except websockets.exceptions.ConnectionClosed:
            print("Client disconnected")
            break

# Start the websocket server
start_server = websockets.serve(handle_client, "0.0.0.0", 9000)

asyncio.get_event_loop().run_until_complete(start_server)
print("Started WebSocket server on port 9000")
asyncio.get_event_loop().run_forever()
