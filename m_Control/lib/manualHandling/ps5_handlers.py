import pygame
import time
from vectorHandler import VectorHandler

# Initialize pygame
pygame.init()

# Initialize the joystick module
pygame.joystick.init()

# Check if there is at least one joystick connected
if pygame.joystick.get_count() == 0:
    print("No joystick connected")
    exit()

# Get the first joystick
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Mapping of buttons to their respective vector indices
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

# Initialize the vector with 10 elements set to 0
vector = [0] * 10

# Initialize the VectorHandler
vector_handler = VectorHandler()

def update_vector_from_buttons():
    for button, index in button_to_index.items():
        vector[index] = joystick.get_button(button)
    vector_handler.update_vector(vector)

try:
    while True:
        # Process pygame events
        pygame.event.pump()

        # Update the vector based on button presses
        update_vector_from_buttons()

        # Add a small delay to avoid flooding the output
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Exiting...")

finally:
    # Quit pygame
    pygame.quit()