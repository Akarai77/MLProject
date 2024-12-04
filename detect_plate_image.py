from ultralytics import YOLO
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import cv2
import easyocr
import re
import os
from upscale import srmodel
from get_plate_details import get_plate_details

model = YOLO(r"C:\Users\Akarsh\Documents\Documents\Code\MLProject\models\best.pt")

file_path = r'C:\Users\Akarsh\Documents\Documents\Code\MLProject\test.jpg'

image = cv2.imread(file_path)

output_dir = r"C:\Users\Akarsh\Documents\Documents\Code\MLProject\cropped_plates"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
if len(os.listdir(output_dir)) != 0:
    for filename in os.listdir(output_dir):
        path = os.path.join(output_dir, filename)
        os.remove(path)

results = model.predict(source=file_path, save=True)

reader = easyocr.Reader(['en'])

plate_pattern = re.compile(r"^[A-Z]{2}\d{2}[A-Z]{1,3}\d{4}$")

detected_plates = []
plate_count = 0

for result in results:
    for box in result.boxes.xyxy:
        plate_count += 1
        x1, y1, x2, y2 = map(int, box)
        
        cropped_plate = image[y1:y2, x1:x2]
        
        cropped_plate = srmodel(cropped_plate)
        
        cropped_plate_path = os.path.join(output_dir, f"cropped_plate_{plate_count}.jpg")
        cv2.imwrite(cropped_plate_path, cropped_plate)
        
        texts = reader.readtext(cropped_plate, detail=0)
        print(f"\n\nExtracted Texts from Plate {plate_count}: {texts}")
        
        for i in range(len(texts)):
            texts[i] = texts[i].upper()
            texts[i] = re.sub(r'[^A-Za-z0-9]', '', texts[i])
            if plate_pattern.match(texts[i]):
                detected_plates.append(texts[i])

if detected_plates:
    print("\nValid License Plates Detected:")
    for idx, plate in enumerate(detected_plates, start=1):
        print(f"{idx}: {plate}")
        get_plate_details(plate)