import asyncio
import websockets
import json
import pygame
from vectorHandler import VectorHandler


websocket_url = "ws://192.168.0.27:81" 




pygame.init()
pygame.joystick.init()
joystick = None

if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print("Connected to controller:", joystick.get_name())
else:
    print("No controller found.")
    exit()


button_to_index = {
    9: 0,   # L1
    10: 1,  # R1
    3: 2,   # Triangle
    0: 3,   # X
    11: 4,  # Arrow up
    12: 5,  # Arrow down
    13: 6,  # Arrow left
    14: 7,  # Arrow right
    2: 8,   # Square
    1: 9    # Circle
}


vector = [0] * 10


vector_handler = VectorHandler()

def update_vector_from_buttons():
    pygame.event.pump()  
    for button, index in button_to_index.items():
        vector[index] = joystick.get_button(button)
    vector_handler.update_vector(vector)

async def send_vector_loop():
    async with websockets.connect(websocket_url) as websocket:
        print("Connected to ESP32 WebSocket server")

        while True:
            update_vector_from_buttons()
            message = json.dumps(vector_handler.current_vector)
            await websocket.send(message)
            print(f"Sent vector {vector_handler.current_vector} to ESP32")
            await asyncio.sleep(0.1)  

async def main():
    await send_vector_loop()  


asyncio.run(main())