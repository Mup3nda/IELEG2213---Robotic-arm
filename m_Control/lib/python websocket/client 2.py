import asyncio
import websockets

async def hello():
    async with websockets.connect("ws://192.168.0.178:9000") as websocket:
        await websocket.send("Hello world!")
        message = await websocket.recv()
        print(f"Received: {message}")
        await websocket.close()

asyncio.run(hello())