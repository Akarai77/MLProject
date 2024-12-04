# Vehicle Number Plate Detection and Information Extraction

This project aims to detect vehicle number plates from images and videos, and then display vehicle information by querying a third-party website, **Car-Info**. The model is custom-trained using the **YOLOv5** object detection model on a number plate dataset.

## Project Structure

```
MLProject/
│
├── training/                   # Contains the dataset used for training and Jupyter notebook
│   ├── dataset_split_yolo.zip  # Dataset zip file with images of number plates
│   └── train_model.ipynb       # Jupyter notebook for training the YOLOv5 model
│
├── models/                     # Folder containing trained models
│   └── best.pt                 # Trained YOLOv5 model weights
│
├── detect_plate_image.py       # Python script for detecting plates from an image
├── detect_plate_video.py       # Python script for detecting plates from a video
├── get_plate_details.py        # Python script for querying Car-Info API (imported in detect scripts)
├── upscale.py                  # Python script for upscaling number plate images (imported in detect scripts)
├── test.jpg                    # Test image for plate detection
├── test.mp4                    # Test video for plate detection
└── README.md                   # This README file
```

## Requirements

To run this project, you'll need the following Python libraries:

- `torch` (for PyTorch)
- `yolov5` (for YOLOv5 object detection)
- `easyocr` (for optical character recognition)
- `esrgan` (for image upscaling)
- `requests` (for querying Car-Info website)
- `opencv-python` (for video frame processing)
- `Pillow` (for image handling)

You can install these dependencies using the following command:

```bash
pip install -r requirements.txt
```

## Training the Model

The YOLOv5 model was trained on a custom number plate dataset, which is available in the `training/dataset_split_yolo.zip` file. The training script `train_model.ipynb` is available in the `training/` directory to guide you through the process of retraining the model if necessary.

The trained model weights are saved in `models/best.pt`.

### Training Process

1. Unzip the `dataset_split_yolo.zip` dataset into the appropriate directory.
2. Prepare the dataset in YOLOv5 format (images and labels).
3. Train the model using the Jupyter notebook `train_model.ipynb`.
4. The model outputs the weights `best.pt` after training, which are saved in the `models/` folder.

## Number Plate Detection

There are two primary Python scripts for detecting number plates:

### 1. `detect_plate_image.py`

This script is used to detect the number plate from a static image (`test.jpg`):

```bash
python detect_plate_image.py
```

- **Flow**:
  1. The model detects the vehicle number plate in the image.
  2. It provides the bounding box coordinates of the detected plate.
  3. The cropped number plate image is then upscaled using the **ESRGAN** model (imported from `upscale.py`).
  4. The upscaled image is passed through **EasyOCR** to detect the text (number plate).
  5. The detected text is validated, and vehicle details are fetched from **Car-Info** using the `get_plate_details.py` script (imported within the `detect_plate_image.py`).

### 2. `detect_plate_video.py`

This script is used to detect number plates from a video (`test.mp4`):

```bash
python detect_plate_video.py
```

- **Flow**:
  1. The video is processed frame by frame.
  2. The model detects the number plate on each frame.
  3. The detected plate is cropped and upscaled (using `upscale.py`), then passed through EasyOCR to extract the text.
  4. The vehicle details are fetched in the same manner as the image detection.

## Image Upscaling

The `upscale.py` script is used to upscale the cropped number plate image to improve OCR accuracy. This script is imported into both the `detect_plate_image.py` and `detect_plate_video.py` files. 

### Upscaling Flow:
- After detecting the number plate and cropping the image, the cropped plate is passed to the **ESRGAN** model for upscaling. This improves the image quality for better text extraction.

## Car-Info API Integration

The `get_plate_details.py` script is used to fetch vehicle details from the **Car-Info API**. This script is imported into the `detect_plate_image.py` and `detect_plate_video.py` files.

### Car-Info API Flow:
- The extracted number plate text is validated, and vehicle details are fetched from **Car-Info** using the API.

## How It Works

1. **YOLOv5 Model**: The YOLOv5 model detects the number plate in the image/video by predicting the bounding box of the plate.
   
2. **ESRGAN Model**: After detecting the number plate, the image is cropped and upscaled using the **ESRGAN** model (via `upscale.py`) to enhance the plate quality for better OCR recognition.

3. **EasyOCR**: The cropped and upscaled image is passed through EasyOCR to extract the text (vehicle number plate).

4. **Car-Info API**: Once the text is extracted, it is validated, and vehicle details are fetched from a third-party website called **Car-Info** using the `get_plate_details.py` script.

## Testing the Model

To test the model:

1. Place a test image (`test.jpg`) or video (`test.mp4`) in the root directory.
2. Run the relevant script (`detect_plate_image.py` or `detect_plate_video.py`).
3. The results will be printed in the terminal, and the vehicle details will be shown in the output.

## Example

For an image:
```bash
python detect_plate_image.py
```

For a video:
```bash
python detect_plate_video.py
```

## Conclusion

This project leverages custom-trained YOLOv5 models for vehicle number plate detection. By integrating image enhancement, OCR, and API queries, we can accurately extract number plate details and query additional vehicle information through an external website.
