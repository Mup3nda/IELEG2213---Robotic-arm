import keyboard
from vectorHandler import VectorHandler

# Initialize the vector with 10 elements set to 0
vector = [0] * 10

# Mapping of keys to their respective vector indices
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

# Initialize the VectorHandler
vector_handler = VectorHandler()

def on_key_event(event):
    if event.event_type == 'down':
        if event.name in key_to_index:
            vector[key_to_index[event.name]] = 1
    elif event.event_type == 'up':
        if event.name in key_to_index:
            vector[key_to_index[event.name]] = 0

    vector_handler.update_vector(vector)

# Set up the listener for key press and release events
keyboard.hook(on_key_event)

# Keep the script running and listening for events
keyboard.wait()