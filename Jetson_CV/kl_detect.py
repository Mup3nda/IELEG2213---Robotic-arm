import jetson.inference
import jetson.utils

# Initialize the detection network
net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.7)

# Initialize the camera and display
camera = jetson.utils.videoSource("csi://0")  # Use CSI camera source
display = jetson.utils.videoOutput("display://0", argv=["--weight=640", "--height=480"])
font = jetson.utils.cudaFont()

# Constants for distance calculation
KNOWN_DISTANCE = 32  # centimeter
KNOWN_WIDTH = 6  # for mouse
MOBILE_CLASS_ID = 77  # Adjust the class ID as per your need
MOUSE_CLASS_ID = 74

# Function to calculate the focal length
# Width in image: 372
# Focal lenght: 2400
def focal_length(measured_distance, real_width, width_in_image):
    return (width_in_image * measured_distance) / real_width

# Function to estimate distance based on detected object width
def distance_finder(focal_length, real_width, width_in_image):
    return (real_width * focal_length) / width_in_image

# Pre-calculate the focal length using a reference image width
# Here, we assume you already have this calculated. Replace with actual values.
focal_length_found = 2400 #615  # Use a pre-measured value

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
            width_in_image = detection.Width  # Width of the detected object
            
            # Calculate the distance
            #focal_length_found = focal_length(KNOWN_DISTANCE, KNOWN_WIDTH, width_in_image)
            distance = distance_finder(focal_length_found, KNOWN_WIDTH, width_in_image)
            
            # Draw a circle at the object's center
            jetson.utils.cudaDrawCircle(img, (center_x, center_y), 8, (255, 0, 0, 200))
            
            # Display the distance on the image
            text = f"Distance: {round(distance, 2)} cm (x={center_x},y={center_y})"
            font.OverlayText(img, img.width, img.height, text, 5, 5, font.White, font.Gray80)
            print(text)
            print(f"Width in image: {width_in_image}")
            print(f"Focal lenght: {focal_length_found}")
    
    # Render the image with the annotations
    display.Render(img)
    
    # Update display status with FPS
    display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))

