import jetson.inference
import jetson.utils

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

# Function for distance calculation without decimal values
def distance_finder(focal_length, known_width_OBJECT, width_in_image):
    return round((known_width_OBJECT * focal_length) / width_in_image)

# Moving average helper function without decimals
def moving_average(values):
    return round(sum(values) / len(values)) if values else 0

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
            if len(last_x) > MAX_MEASUREMENTS:
                last_x.pop(0)
                last_y.pop(0)
                last_distance.pop(0)
            
            # Calculate averaged values
            avg_x = moving_average(last_x)
            avg_y = moving_average(last_y)
            avg_distance = moving_average(last_distance)

            # Draw a circle at the object's center
            jetson.utils.cudaDrawCircle(img, (center_x, center_y), 8, (255, 0, 0, 200))
            
            # Display the stabilized distance and coordinates on the image without decimals
            text = f"Coordinates: x={avg_x} cm, y={avg_y} cm, z={avg_distance} cm"
            font.OverlayText(img, img.width, img.height, text, 5, 5, font.White, font.Gray80)
    
    # Render the image with the annotations
    display.Render(img)
    
    # Update display status with FPS
    display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))
