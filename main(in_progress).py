import cv2
import numpy as np
import time
import os
import subprocess
from datetime import datetime
import random
from djitellopy import Tello

from beehive_utils.model import load_beehive_model
from beehive_utils.logger import save_bird_logs, save_detected_bird
from beehive_utils.detection import preprocess_frame_to_tiles, predict_tile
from beehive_utils.sound import play_sound_deterent
from beehive_utils.drone import deploy_drone
from beehive_utils.camera import get_available_cameras


# --- Config ---
INPUT_SIZE = (180, 180)
CONFIDENCE_THRESHOLD = 0.9
LOOP_INTERVAL = 3
BIRD_WARNING_THRESHOLD_SECONDS = 5   # Time before activating sound deterrent
BIRD_DRONE_THRESHOLD_SECONDS = 10    # Time after sound before deploying drone
DRONE_FORWARD_DISTANCE = 100  # distance in cm

loop_count = 0

# State variables for deterrents and timing
bird_detected_start_time = None
sound_proc = None
DRONE_DEPLOYED = False

# --- Load Beehive Model ---
interpreter, input_details, output_details = load_beehive_model()

# --- Functions ---


def respond_to_bird():
    sound_proc = play_sound_deterent()
    deploy_drone()
    sound_proc.terminate()  # stop the sound (optional)


# Get camera indexes
camera_indexes = get_available_cameras()
print("Available cameras:", camera_indexes)

# # Setup cameras dynamically
# if len(camera_indexes) < 2:
#     print("Not enough working cameras found!")
#     exit()

# # Setup cameras
# capture_one = cv2.VideoCapture(camera_indexes[0])
# capture_two = cv2.VideoCapture(camera_indexes[1])

# for cap in [capture_one, capture_two]:
#     cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
#     cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

# while True:
#     bird_found = False
#     detected_cam = None
#     detected_tile = None
#     detected_conf = None
#     detected_img = None

#     # Check both cameras for birds
#     for cam_id, cap in enumerate([capture_one, capture_two]):
#         ret, frame = cap.read()
#         if not ret:
#             print(f"❌ Failed to read from camera {cam_id}")
#             continue

#         frame = cv2.rotate(frame, cv2.ROTATE_180)
#         # Show the raw camera frame in a popup window (no grid)
#         cv2.imshow(f'Camera {cam_id} Feed', frame)
#         frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         tiles, coords = preprocess_frame_to_tiles(frame_rgb)

#         for i, tile in enumerate(tiles):
#             label, conf = predict_tile(
#                 tile, interpreter, input_details, output_details)
#             r, c, x, y = coords[i]
#             print(f"[CAM {cam_id}] Tile {i} [{r},{c}] → {label} ({conf:.2f})")

#             if label == "with_bird" and conf >= CONFIDENCE_THRESHOLD:
#                 print(f"[CAM {cam_id}] BIRD DETECTED at tile [{r},{c}]!")
#                 bird_found = True
#                 detected_cam = cam_id
#                 detected_tile = i
#                 detected_conf = conf
#                 detected_img = tiles[i]
#                 break
#         if bird_found:
#             break

#     current_time = time.time()

#     # --- STATE MACHINE LOGIC ---
#     # States: 'IDLE', 'WARNING', 'SOUND_ON', 'DRONE_DEPLOYED'
#     if 'bird_state' not in globals():
#         bird_state = 'IDLE'
#         warning_start_time = None
#         sound_start_time = None
#         sound_proc = None
#         DRONE_DEPLOYED = False
#         drone_started = False

#     if bird_found:
#         if bird_state == 'IDLE':
#             warning_start_time = current_time
#             bird_state = 'WARNING'
#             print('First warning: Bird detected, starting 5s timer.')

#         elif bird_state == 'WARNING':
#             if current_time - warning_start_time >= BIRD_WARNING_THRESHOLD_SECONDS:
#                 # Activate sound deterrent
#                 if sound_proc is None or sound_proc.poll() is not None:
#                     sound_proc = play_sound_deterent()
#                     print(
#                         f'Sound deterrent started after {BIRD_WARNING_THRESHOLD_SECONDS}s.')
#                 sound_start_time = current_time
#                 bird_state = 'SOUND_ON'

#         elif bird_state == 'SOUND_ON':
#             if current_time - sound_start_time >= BIRD_DRONE_THRESHOLD_SECONDS and not DRONE_DEPLOYED:
#                 # Deploy drone
#                 deploy_drone()
#                 DRONE_DEPLOYED = True
#                 drone_started = True
#                 print(
#                     f'Drone deployed after {BIRD_DRONE_THRESHOLD_SECONDS}s of sound deterrent.')
#             # Save detection image
#             if detected_img is not None:
#                 # save_bird_logs(detected_cam, detected_tile, detected_conf)
#                 save_detected_bird(detected_img, detected_cam,
#                                    detected_tile, detected_conf)
#             # After drone finishes, reset everything
#             if DRONE_DEPLOYED and drone_started:
#                 # Assume deploy_drone() is blocking and returns when done
#                 if sound_proc is not None and sound_proc.poll() is None:
#                     sound_proc.terminate()
#                     print('Sound deterrent stopped after drone.')
#                     sound_proc = None
#                 bird_state = 'IDLE'
#                 warning_start_time = None
#                 sound_start_time = None
#                 DRONE_DEPLOYED = False
#                 drone_started = False
#                 print('System reset after drone mission.')

#     else:
#         # No bird detected, reset everything
#         if sound_proc is not None and sound_proc.poll() is None:
#             sound_proc.terminate()
#             print('Sound deterrent stopped (no bird).')
#             sound_proc = None
#         if DRONE_DEPLOYED:
#             try:
#                 tello = Tello()
#                 tello.connect()
#                 tello.land()
#                 print('Drone landed (no bird detected).')
#             except Exception as e:
#                 print(f'Error landing drone: {str(e)}')
#             DRONE_DEPLOYED = False
#         bird_state = 'IDLE'
#         warning_start_time = None
#         sound_start_time = None
#         drone_started = False

#     print("Sleep...")
#     time.sleep(LOOP_INTERVAL)
#     loop_count = loop_count + 1

#     # Close if any window gets 'q'
#     if cv2.waitKey(1) & 0xFF == ord("q"):
#         print("Stopping...")
#         break
#     # Also close windows if user closes them manually
#     if cv2.getWindowProperty('Camera 0 Feed', cv2.WND_PROP_VISIBLE) < 1 or cv2.getWindowProperty('Camera 1 Feed', cv2.WND_PROP_VISIBLE) < 1:
#         print("Window closed by user.")
#         break

# capture_one.release()
# capture_two.release()
# cv2.destroyAllWindows()
