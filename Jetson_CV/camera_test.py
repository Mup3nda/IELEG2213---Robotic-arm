import cv2
import time

# Use GStreamer pipeline for CSI camera
gstreamer_pipeline = (
    "nvarguscamerasrc ! "
    "video/x-raw(memory:NVMM), width=1280, height=720, format=(string)NV12, framerate=30/1 ! "
    "nvvidconv flip-method=2 ! "
    "video/x-raw, width=1280, height=720, format=(string)BGRx ! "
    "videoconvert ! "
    "video/x-raw, format=(string)BGR ! appsink"
)

camera = cv2.VideoCapture(gstreamer_pipeline, cv2.CAP_GSTREAMER)

if not camera.isOpened():
    print("Error: Could not open camera.")
    exit()

# Add a delay to ensure the camera is ready
time.sleep(2)

while True:
    ret, frame = camera.read()
    if not ret:
        print("Failed to grab frame")
        break

    cv2.imshow("Camera Test", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()

