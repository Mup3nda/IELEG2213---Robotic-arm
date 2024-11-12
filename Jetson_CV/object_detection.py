import jetson.inference
import jetson.utils
import asyncio
import websockets

# Initialize the detection network
net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)

# Initialize the camera and display
camera = jetson.utils.videoSource("csi://0")  # Use CSI camera source
display = jetson.utils.videoOutput("display://0")
font = jetson.utils.cudaFont()

# Constants for distance calculation
KNOWN_DISTANCE = 36  # centimeter
KNOWN_WIDTH_OBJECT = 6.5  # for mouse
KNOWN_HEIGHT = 3.5 # for mouse
MOUSE_CLASS_ID = 74  # Adjust the class ID as per your need
focal_length_found = 2200  # Pre-measured focal length

# Moving average configuration
MAX_MEASUREMENTS = 15  # Number of measurements to average
last_x, last_y, last_distance = [], [], []

# Function for distance calculation without decimal values
def distance_finder(focal_length, known_width_OBJECT, width_in_image):
    
    return round((known_width_OBJECT * focal_length) / width_in_image)

# Moving average helper function without decimals
def moving_average(values):
    return round(sum(values) / len(values)) if values else 0

async def send_data():
    uri = "ws://192.168.0.135:9000"  # Replace with your WebSocket server URI
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
                    width_object_cm = detection.Width / KNOWN_WIDTH_OBJECT  # Width of the detected object
                    width_object_pixels = detection.Width
                    
                    # Convert x and y coordinates from pixels to cm without decimals
                    x_cm = round(center_x / width_object_cm)
                    y_cm = round(center_y / width_object_cm)
                    
                    # Calculate the distance without decimals
                    distance = distance_finder(focal_length_found, KNOWN_WIDTH_OBJECT, width_object_pixels)
                    
                    # Update lists for moving averages
                    last_x.append(x_cm)
                    last_y.append(y_cm)
                    last_distance.append(distance)
                    
                    # Maintain list size for moving average
                    if len(last_x) > MAX_MEASUREMENTS: # Only need for one of the variable (x,y,z)
                        last_x.pop(0) 
                        last_y.pop(0)
                        last_distance.pop(0)
                    
                    # Calculate averaged values
                    avg_x = moving_average(last_x)
                    avg_y = moving_average(last_y)
                    avg_distance = moving_average(last_distance)

                    # Check if there's a significant change
                    if (
                        last_sent_x is None or
                        abs(avg_x - last_sent_x) >= 2 or
                        abs(avg_y - last_sent_y) >= 2 or
                        abs(avg_distance - last_sent_distance) >= 2
                    ):
                        # Send data via WebSocket only if there's a significant change
                        data = f"{avg_x}, {avg_y}, {avg_distance}"
                        await websocket.send(data)

                        # Update the last sent values
                        last_sent_x, last_sent_y, last_sent_distance = avg_x, avg_y, avg_distance
                    
                    # Draw a circle at the object's center
                    jetson.utils.cudaDrawCircle(img, (center_x, center_y), 8, (255, 0, 0, 200))
                    
                    # Display the stabilized distance and coordinates on the image without decimals
                    text = f"Coordinates: x={avg_x} cm, y={avg_y} cm, z={avg_distance} cm"
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
