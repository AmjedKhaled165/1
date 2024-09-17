https://colab.research.google.com/drive/1BdtCs1TAOIl3QExcRfjdkAC0n4kwBW2A
from ultralytics import YOLO
import cv2

# Load the YOLO model (you can use 'yolov8n.pt' for a lighter model)
model = YOLO('yolov8n.pt')  # yolov8n.pt (nano) is smaller and faster

# Open the camera
cap = cv2.VideoCapture(0)

# Set a lower resolution for better performance on Raspberry Pi
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Inference with YOLO model
    results = model(frame)

    # Annotate the frame with results
    annotated_frame = results[0].plot()

    # Display the frame with detection boxes
    cv2.imshow("YOLOv8 Detection", annotated_frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
