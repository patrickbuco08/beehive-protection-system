import cv2
import os
import glob

from beehive_utils.detection import is_bird_detected_in_tiles
from beehive_utils.model import load_beehive_model

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

    # Run detection over multiple tile shapes
    bird_detected = is_bird_detected_in_tiles(
        frame_rgb,
        interpreter,
        input_details,
        output_details
    )
    if bird_detected:
        print(f"Bird detected in {img_path}")
    else:
        print(f"No bird detected in {img_path}")

print("done")
