import keyboard

def on_key_event(event):
    print(f"Key {event.name} was pressed")

# Set up the listener for key press events
keyboard.on_press(on_key_event)

# Keep the script running and listening for events
keyboard.wait()