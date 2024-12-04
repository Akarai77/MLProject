from ultralytics import YOLO
import cv2
import easyocr
import re
import numpy as np

# Load YOLO model
model = YOLO(r"C:\Users\Akarsh\Documents\Documents\Code\MLProject\models\best.pt")

# Path to video file
video_path = 'test.mp4'

# Initialize video capture
cap = cv2.VideoCapture(video_path)

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

# Regular expression to validate license plate format
plate_pattern = re.compile(r"^[A-Z]{2}\d{2}[A-Z]{1,2}\d{4}$")

while True:
    ret, frame = cap.read()
    if not ret:  # Break loop if the video ends
        break

    # Predict license plate location using YOLO
    results = model.predict(source=frame, save=False)

    for result in results:
        for box in result.boxes.xyxy:
            x1, y1, x2, y2 = map(int, box)  # Extract bounding box coordinates
            cropped_plate = frame[y1:y2, x1:x2]  # Crop the license plate region

            # Perform OCR on the cropped plate
            texts = reader.readtext(cropped_plate, detail=0)

            detected_text = None
            for text in texts:
                if plate_pattern.match(text):
                    print(f"Detected Valid License Plate: {text}")
                    detected_text = text
                    break

            # Draw bounding box and label the license plate text
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Bounding box
            label = detected_text if detected_text else "Plate"
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # Display the frame with bounding boxes and text
    cv2.imshow("License Plate Detection", frame)

    # Press 'q' to exit the visualization loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture and close windows
cap.release()
cv2.destroyAllWindows()
