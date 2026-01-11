import jetson.inference
import jetson.utils
import asyncio
import websockets
import numpy as np

# Initialize the detection network
net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)

# Initialize the camera and display
camera = jetson.utils.videoSource("csi://0")  # Use CSI camera source
display = jetson.utils.videoOutput("display://0")
font = jetson.utils.cudaFont()

# Constants for distance calculation
KNOWN_DISTANCE = 45  # centimeter
KNOWN_WIDTH_OBJECT = 6.5  # for mouse
MOUSE_CLASS_ID = 74  # Adjust the class ID as per your need
focal_length_found = 2400  # Pre-measured focal length

# Moving average configuration
MAX_MEASUREMENTS = 15  # Number of measurements to average
last_x, last_y, last_distance = [], [], []

# Base correction factor and scaling factor
BASE_CORRECTION_FACTOR = 0.20  # cm (initial correction at close range)
CORRECTION_SCALING = 0.10  # Scaling factor for correction based on distance

# Function for distance calculation without decimal values
def distance_finder(focal_length, known_width_OBJECT, width_in_image):
    return round((known_width_OBJECT * focal_length) / width_in_image)

# Moving average helper function without decimals
def moving_average(values):
    return round(sum(values) / len(values)) if values else 0

async def send_data():
    uri = "ws://192.168.0.178:9000"  # ABDI
    #uri = "ws://192.168.0.135:8765"  # DIDI
    async with websockets.connect(uri) as websocket:
        # Store last sent values to check for significant changes
        last_sent_x, last_sent_y, last_sent_distance = None, None, None

        while True:
            # Capture the image from the camera
            img = camera.Capture()
        
            # Detect objects in the image
            detections = net.Detect(img)
            
            for detection in detections:
                if detection.ClassID == MOUSE_CLASS_ID:
                    # Get the center and width of the detected object
                    center_x = int(detection.Center[0])
                    center_y = int(detection.Center[1])

                    width_object_pixels = detection.Width
                    scaling_factor = width_object_pixels / KNOWN_WIDTH_OBJECT  # Width of the detected object
                    
                    # Invert the x-coordinate to start from the top-right
                    img_width = img.width  # Get the image width
                    inverted_x = img_width - center_x

                    
                    # Convert x and y coordinates from pixels to cm without decimals
                    x_cm = round(inverted_x / scaling_factor)
                    y_cm = round(center_y / scaling_factor)
                    
                    # Calculate the distance without decimals
                    distance = distance_finder(focal_length_found, KNOWN_WIDTH_OBJECT, width_object_pixels)
                    
                    # Update lists for moving averages
                    last_x.append(x_cm)
                    last_y.append(y_cm)
                    last_distance.append(distance)
                    
                    # Maintain list size for moving average
                    if len(last_x) > MAX_MEASUREMENTS:
                        last_x.pop(0)
                        last_y.pop(0)
                        last_distance.pop(0)
                    
                    # Calculate averaged values
                    avg_x = moving_average(last_x)
                    avg_y = moving_average(last_y)
                    avg_distance = moving_average(last_distance)

                    # Apply a dynamic correction factor based on distance
                    dynamic_correction = BASE_CORRECTION_FACTOR + (avg_distance * CORRECTION_SCALING)
                    corrected_x = round(avg_x + dynamic_correction)
                    corrected_y = round(avg_y + dynamic_correction)
                    corrected_z = round(avg_distance)

                    # Check if there's a significant change before sending data
                    if (
                        last_sent_x is None or
                        abs(corrected_x - last_sent_x) >= 3 or
                        abs(corrected_y - last_sent_y) >= 3 or
                        abs(avg_distance - last_sent_distance) >= 3
                    ):
                        # Send data via WebSocket
                        data = f"{corrected_x}, {corrected_y}, {corrected_z}"
                        await websocket.send(data)
                        
                        # Update the last sent values
                        last_sent_x, last_sent_y, last_sent_distance = corrected_x, corrected_y, corrected_z
                    
                    # Draw a circle at the object's center
                    jetson.utils.cudaDrawCircle(img, (center_x, center_y), 8, (255, 0, 0, 200))
                    
                    # Display the stabilized distance and corrected coordinates on the image without decimals
                    text = f"Coordinates: x={corrected_x} cm, y={corrected_y} cm, z={corrected_z} cm"
                    font.OverlayText(img, img.width, img.height, text, 5, 5, font.White, font.Gray60)
            
            # Render the image with the annotations
            display.Render(img)
            
            # Update display status with FPS
            display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))
            
            # Control the loop delay
            await asyncio.sleep(0.1)

# Run the main function with WebSocket integration
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(send_data())
