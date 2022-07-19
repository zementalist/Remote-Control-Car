
import cv2 # pip install opencv-python
import torch

# Model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # or yolov5n - yolov5x6, custom

# Initialize Video Reader
cap = cv2.VideoCapture(0)

# Capture video
while True:
    ret, frame = cap.read()
    
    # If there is a new frame to read
    if ret:
        # Convert image to grayscale to reduce complexiy
        results = model(frame)
        img = results.render()[0]
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        cv2.imshow("window", img)
        out.write(img)
    else:
        break

# Stop video & Destroy window
cap.release()
cv2.destroyAllWindows()
