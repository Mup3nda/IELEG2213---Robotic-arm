import jetson.inference
import jetson.utils

# Initialize the detection network
net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.6)

# Initialize the camera and display
camera = jetson.utils.videoSource("csi://0")  # Use CSI camera source
# display = jetson.utils.videoOutput("display://0", argv=["--weight=1280", "--height=720"])
display = jetson.utils.videoOutput("display://0")
font = jetson.utils.cudaFont()

# Constants for distance calculation
KNOWN_DISTANCE = 36  # centimeter
KNOWN_WIDTH_OBJECT = 6.5  # for mouse
KNOWN_HEIGHT_OBJECT = 10  # for mouse
MOUSE_CLASS_ID = 74  # Adjust the class ID as per your need

# Pre-calculate the focal length using a reference image width
focal_length_found = 2200 #2400  # Pre-measured focal length 2200 eller 2400

def distance_finder(focal_length, known_width_OBJECT, width_in_image):
    return round(((known_width_OBJECT * focal_length) / width_in_image),2)

def focal_length(measured_distance, real_width, width_in_image):
    return (width_in_image * measured_distance) / real_width

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
            height_object_cm = detection.Height / KNOWN_HEIGHT_OBJECT
            width_object_pixels = detection.Width
            
            # Convert x and y coordinates from pixels to cm
            x_cm = round(center_x / width_object_cm, 2)
            y_cm = round(center_y / height_object_cm, 2)

            #focal_length_found = focal_length(KNOWN_DISTANCE, KNOWN_WIDTH_OBJECT, width_object_pixels)
            # Calculate the distance
            distance = distance_finder(focal_length_found, KNOWN_WIDTH_OBJECT, width_object_pixels)
            
            # Draw a circle at the object's center
            jetson.utils.cudaDrawCircle(img, (center_x, center_y), 8, (255, 0, 0, 200))
            
            # Display the distance and coordinates on the image
            text = f"Coordinates: x={x_cm} cm, y={y_cm} cm, z={distance} cm"
            font.OverlayText(img, img.width, img.height, text, 5, 5, font.White, font.Gray80)
            print(text)
            print(f"Focal lenght: {focal_length_found}")
    
    # Render the image with the annotations
    display.Render(img)
    
    # Update display status with FPS
    display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))
