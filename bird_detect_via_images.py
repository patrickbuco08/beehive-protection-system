import cv2
import os
import glob

from beehive_utils.detection import preprocess_frame_to_tiles, predict_tile
from beehive_utils.logger import save_detected_bird
from beehive_utils.model import load_beehive_model


# --- Config ---
TILE_SHAPE = (4, 4)
CONFIDENCE_THRESHOLD = 0.80
MIN_CONFIDENCE_THRESHOLD = 0.50
MAX_CONFIDENCE_THRESHOLD = 0.95


# --- Load TFLite Model ---
interpreter, input_details, output_details = load_beehive_model()

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

for img_path in image_files:
    img = cv2.imread(img_path)
    if img is None:
        print(f" Could not read image: {img_path}")
        continue
    frame_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    tiles, coords = preprocess_frame_to_tiles(frame_rgb, TILE_SHAPE)
    bird_found = False
    bird_conf = 0
    for i, tile in enumerate(tiles):
        label, conf = predict_tile(
            tile, interpreter, input_details, output_details)
        r, c, x, y = coords[i]

        # save_detected_bird(tiles[i], 1, i, conf) # enable this to generate dataset

        if label == "with_bird" and (MIN_CONFIDENCE_THRESHOLD <= conf <= MAX_CONFIDENCE_THRESHOLD):
            print(f"bird detected. confidence {conf:.2f}")
            # save_detected_bird(tiles[i], 1, i, conf)

print("done")
