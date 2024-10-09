import pygame
import time

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

print(f"Joystick name: {joystick.get_name()}")
print(f"Number of axes: {joystick.get_numaxes()}")
print(f"Number of buttons: {joystick.get_numbuttons()}")
print(f"Number of hats: {joystick.get_numhats()}")

try:
    while True:
        # Process pygame events
        pygame.event.pump()

        # Read button values
        for i in range(joystick.get_numbuttons()):
            button = joystick.get_button(i)
            if button:  # Only print if the button is pressed
                print(f"Button {i} pressed")

        # Add a small delay to avoid flooding the output
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Exiting...")

finally:
    # Quit pygame
    pygame.quit()