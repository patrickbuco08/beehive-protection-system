import os
from datetime import datetime
from pathlib import Path
import cv2

# Resolve root directory (assuming this file is inside beehive_utils or utils)
ROOT_DIR = Path(__file__).resolve().parent.parent
DETECTIONS_DIR = ROOT_DIR / "detections"
DETECTIONS_DIR.mkdir(exist_ok=True)


def save_detected_bird(tile_img, cam_id, tile_id, confidence, label="with_bird"):
    now = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f"{DETECTIONS_DIR}/{label}_cam{cam_id}_tile{tile_id}_{int(confidence*100)}_{now}.jpg"

    # Convert color from RGB to BGR for OpenCV saving
    tile_bgr = cv2.cvtColor(tile_img, cv2.COLOR_RGB2BGR)

    # resize
    # tile_bgr = cv2.resize(tile_bgr, (400, 400))

    cv2.imwrite(filename, tile_bgr)
    print(f"📸 Saved detection: {filename}")


def save_bird_logs(cam_id, tile_id, confidence):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_path = DETECTIONS_DIR / "logs.txt"

    log_entry = f"[{now}] Detection - Camera: {cam_id}, Tile: {tile_id}, Confidence: {confidence:.2f}\n"

    with open(log_path, "a") as log_file:
        log_file.write(log_entry)
