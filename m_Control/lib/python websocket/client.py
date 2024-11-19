import asyncio
import websockets
import json
import numpy as np 

async def hello():
    async with websockets.connect("ws://192.168.0.178:9000") as websocket:
        test = ["10,10,20", "20,20,10", "15,15,10", "35,35,10"]
        for i in test: 
            await websocket.send(i)
        message = await websocket.recv()
        print(f"Received: {message}")
        await websocket.close()

asyncio.run(hello())