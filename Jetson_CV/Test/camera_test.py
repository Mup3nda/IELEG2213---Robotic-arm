import jetson.inference
import jetson.utils

# Initialize the detection network
net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)

# Initialize the camera and display
camera = jetson.utils.videoSource("csi://0")  # Use CSI camera source
display = jetson.utils.videoOutput()
font = jetson.utils.cudaFont()

# Class ID for "mobile" (verify this ID based on your model)
MOBILE_CLASS_ID = 77 #84 for book

while True:
    # Capture the image
    img = camera.Capture()
    
    # Detect objects in the image
    detections = net.Detect(img)
    
    for detection in detections:
        if detection.ClassID == MOBILE_CLASS_ID:
            center_x = int(detection.Center[0])
            center_y = int(detection.Center[1])
            jetson.utils.cudaDrawCircle(img, (center_x, center_y), 8, (255, 0, 0, 200))
            text = f"Target's coordinates: (x={center_x},y={center_y})"
            font.OverlayText(img, img.width, img.height, text, 5,5, font.White, font.Gray80)
            print(text)
    
    # Render the image
    display.Render(img)
    
    # Update the display status
    display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))
    


