#!/usr/bin/env python
# coding: utf-8

# In[1]:


# jupyter nbconvert --to script rpi_bird_detection.ipynb


# In[27]:


import cv2
import numpy as np
import tensorflow as tf  # ON PC, we can use full TensorFlow
import matplotlib.pyplot as plt
import time
import os
import subprocess
import glob
from datetime import datetime

# import tflite_runtime.interpreter as tflite
tflite = tf.lite


# In[85]:


# --- Config ---
INPUT_SIZE = (180, 180)
ROWS, COLS = 4, 4
CONFIDENCE_THRESHOLD = 0.80
MODEL_PATH = "models/bird_detection_model_v1.tflite"
SOUND_FILENAME = 'alert.wav'
CLASS_NAMES = ['no_bird', 'with_bird']


# In[87]:


# load model
interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()


# In[101]:


# --- Load TFLite Model ---
interpreter = tflite.Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()


def predict_tile(tile):
    img = cv2.resize(tile, INPUT_SIZE).astype(np.float32) / 255.0
    img = np.expand_dims(img, axis=0)
    interpreter.set_tensor(input_details[0]['index'], img)
    interpreter.invoke()
    output = interpreter.get_tensor(output_details[0]['index'])
    pred_class = np.argmax(output[0])
    confidence = output[0][pred_class]
    return CLASS_NAMES[pred_class], confidence

def preprocess_frame_to_tiles(frame):
    tiles = []
    coords = []
    height, width = frame.shape[:2]
    tile_h, tile_w = height // ROWS, width // COLS

    for r in range(ROWS):
        for c in range(COLS):
            y1, y2 = r * tile_h, (r + 1) * tile_h
            x1, x2 = c * tile_w, (c + 1) * tile_w
            tile = frame[y1:y2, x1:x2]
            tiles.append(tile)
            coords.append((r, c, x1, y1))
    return tiles, coords

def save_detected_bird(tile_img, cam_id, tile_id, confidence):
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder = "detections"
    os.makedirs(folder, exist_ok=True)
    filename = f"{folder}/cam{cam_id}_tile{tile_id}_{int(confidence*100)}_{now}.jpg"
    # Convert color from RGB to BGR for OpenCV saving
    tile_bgr = cv2.cvtColor(tile_img, cv2.COLOR_RGB2BGR)
    # Resize to 400x400 before saving
    tile_bgr_resized = cv2.resize(tile_bgr, (400, 400))
    cv2.imwrite(filename, tile_bgr_resized)
    print(f"📸 Saved detection: {filename}")


# In[103]:


# Directory containing test images
TEST_IMAGES_DIR = "test_images"
IMAGE_EXTENSIONS = ("*.jpg", "*.jpeg", "*.png")

# Gather all image files
image_files = []
for ext in IMAGE_EXTENSIONS:
    image_files.extend(glob.glob(os.path.join(TEST_IMAGES_DIR, ext)))

if not image_files:
    print("No images found in test_images directory.")
    exit()


# In[107]:


for img_path in image_files:
    img = cv2.imread(img_path)
    if img is None:
        print(f" Could not read image: {img_path}")
        continue
    frame_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    tiles, coords = preprocess_frame_to_tiles(frame_rgb)
    bird_found = False
    bird_conf = 0
    for i, tile in enumerate(tiles):
        label, conf = predict_tile(tile)
        r, c, x, y = coords[i]
        if label == "with_bird" and (0.85 <= conf <= 0.90):
            print(f"bird detected. confidence {conf:.2f}")
            save_detected_bird(tiles[i], 1, i, conf)

print("done")


# In[ ]:




