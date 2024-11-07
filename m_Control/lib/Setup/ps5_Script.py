import asyncio
import websockets
import keyboard
import json
from vector_Handler import VectorHandler

websocket_url = "ws://192.168.0.27:81"

vector = [0] * 10
key_to_index = {
    'pil venstre': 0,
    'pil høyre': 1,
    'pil opp': 2,
    'pil ned': 3,
    'a': 4,
    'd': 5,
    'w': 6,
    's': 7,
    'space': 8,
    'esc': 9
}
vector_handler = VectorHandler()

async def send_vector_loop():
    async with websockets.connect(websocket_url) as websocket:
        print("Connected to ESP32 WebSocket server")
        
        while True:
            vector_handler.update_vector(vector)
            message = json.dumps(vector_handler.current_vector)
            await websocket.send(message)
            print(f"Sent vector {vector_handler.current_vector} to ESP32")
            await asyncio.sleep(0.1)

def on_key_event(event):
    if event.event_type == 'down' and event.name in key_to_index:
        vector[key_to_index[event.name]] = 1
    elif event.event_type == 'up' and event.name in key_to_index:
        vector[key_to_index[event.name]] = 0

async def main():
    keyboard.hook(on_key_event)
    await send_vector_loop() 

asyncio.run(main())
