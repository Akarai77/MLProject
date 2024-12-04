# Importing all the required packages and libraries
import tensorflow as tf
import tensorflow_hub as hub
import cv2
import numpy as np

def preprocessing(img):
    image_plot = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    imageSize = (tf.convert_to_tensor(image_plot.shape[:-1]) // 4) * 4
    cropped_image = tf.image.crop_to_bounding_box(
		img, 0, 0, imageSize[0], imageSize[1])
    preprocessed_image = tf.cast(cropped_image, tf.float32)
    return tf.expand_dims(preprocessed_image, 0)


esrgn_path = "https://tfhub.dev/captain-pool/esrgan-tf2/1"
model = hub.load(esrgn_path)

def srmodel(img):
    preprocessed_image = preprocessing(img)
    new_image = model(preprocessed_image)
    
    # Convert the tensor to a NumPy array and normalize it
    new_image = tf.squeeze(new_image) / 255.0  # Normalize to [0, 1]
    
    # Convert tensor to a NumPy array (HWC format, uint8)
    new_image = new_image.numpy() * 255.0  # Scale back to [0, 255]
    new_image = np.clip(new_image, 0, 255).astype(np.uint8)  # Ensure valid range and convert to uint8
    
    return new_image
