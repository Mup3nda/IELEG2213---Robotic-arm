import asyncio
import websockets
import json
import numpy as np 

async def hello():
    async with websockets.connect("ws://192.168.0.178:9000") as websocket:
        test = "10, 10, 20"
        await websocket.send(test)
        message = await websocket.recv()
        print(f"Received: {message}")
        print(message[0])
        await websocket.close()

asyncio.run(hello())