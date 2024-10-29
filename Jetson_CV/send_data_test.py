import asyncio
import websockets
import random

async def send_coordinates():
    #uri = "ws://10.22.75.29:8765"  # Didier
    uri = "ws://192.168.0.135:9000" # ABS
    async with websockets.connect(uri) as websocket:
        while True:
            x = random.randint(0, 100)
            y = random.randint(0, 100)
            z = random.randint(0, 100)
            data = f"{x},{y},{z}"
            await websocket.send(data)
            await asyncio.sleep(1)

asyncio.get_event_loop().run_until_complete(send_coordinates())



