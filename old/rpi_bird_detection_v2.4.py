import cv2
import numpy as np
import time
import os
import subprocess
from datetime import datetime
import random
from djitellopy import Tello

import tflite_runtime.interpreter as tflite

# --- Config ---
INPUT_SIZE = (180, 180)
ROWS, COLS = 8, 8
CONFIDENCE_THRESHOLD = 0.8
MODEL_PATH = "bird_detection_model_v2.4.tflite"
SOUND_FILES = [
    'alert1.wav',
    'alert1.wav',
    'alert1.wav',
    'alert1.wav',
    'alert1.wav'
]
CLASS_NAMES = ['no_bird', 'with_bird']
LOOP_INTERVAL = 3
BIRD_WARNING_THRESHOLD_SECONDS = 5   # Time before activating sound deterrent
BIRD_DRONE_THRESHOLD_SECONDS = 10    # Time after sound before deploying drone
DRONE_FORWARD_DISTANCE = 100  # distance in cm

loop_count = 0

# State variables for deterrents and timing
bird_detected_start_time = None
sound_proc = None
DRONE_DEPLOYED = False

# --- Load TFLite Model ---
interpreter = tflite.Interpreter(model_path="bird_detection_model_v2.4.tflite")
interpreter.allocate_tensors()

interpreter = tflite.Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()


# --- Functions --
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


def save_bird_logs(cam_id, tile_id, confidence):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    folder = "detections"
    os.makedirs(folder, exist_ok=True)

    log_entry = f"[{now}] Detection - Camera: {cam_id}, Tile: {tile_id}, Confidence: {confidence:.2f}\n"

    log_path = os.path.join(folder, "logs.txt")
    with open(log_path, "a") as log_file:
        log_file.write(log_entry)


def predict_tile(tile):
    img = cv2.resize(tile, INPUT_SIZE).astype(np.float32) / 255.0
    img = np.expand_dims(img, axis=0)
    interpreter.set_tensor(input_details[0]['index'], img)
    interpreter.invoke()
    output = interpreter.get_tensor(output_details[0]['index'])
    pred_class = np.argmax(output[0])
    confidence = output[0][pred_class]
    return CLASS_NAMES[pred_class], confidence


def play_sound_deterent():
    selected_sound = random.choice(SOUND_FILES)
    print(f"🔊 Playing sound: {selected_sound}")
    sound_path = os.path.join(os.getcwd(), selected_sound)
    return subprocess.Popen(["aplay", sound_path])


def deploy_drone():
    print("🚁 Drone: Starting mission...")

    try:
        tello = Tello()
        tello.connect()
        print("✅ Drone connected")

        time.sleep(2)

        tello.takeoff()
        print("🛫 Drone took off")

        tello.move_forward(DRONE_FORWARD_DISTANCE)
        print(f"➡️ Moved forward {DRONE_FORWARD_DISTANCE}cm")

        tello.move_back(DRONE_FORWARD_DISTANCE)
        print(f"⬅️ Returned backward {DRONE_FORWARD_DISTANCE}cm")

        tello.land()
        print("✅ Drone landed successfully")

    except Exception as e:
        print(f"⚠️ Drone error: {str(e)}")
        print("❌ Flight mission aborted, continuing system...")


def respond_to_bird():
    sound_proc = play_sound_deterent()
    deploy_drone()
    sound_proc.terminate()  # stop the sound (optional)


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


def get_available_cameras(max_index=10):
    working_indexes = []
    for i in range(max_index):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ret, _ = cap.read()
            if ret:
                working_indexes.append(i)
            cap.release()
    return working_indexes


# Get camera indexes
camera_indexes = get_available_cameras()
print("Available cameras:", camera_indexes)

# Setup cameras dynamically
if len(camera_indexes) < 2:
    print("Not enough working cameras found!")
    exit()

# Setup cameras
capture_one = cv2.VideoCapture(camera_indexes[0])
capture_two = cv2.VideoCapture(camera_indexes[1])

for cap in [capture_one, capture_two]:
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:
    bird_found = False
    detected_cam = None
    detected_tile = None
    detected_conf = None
    detected_img = None

    # Check both cameras for birds
    for cam_id, cap in enumerate([capture_one, capture_two]):
        ret, frame = cap.read()
        if not ret:
            print(f"❌ Failed to read from camera {cam_id}")
            continue

        frame = cv2.rotate(frame, cv2.ROTATE_180)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        tiles, coords = preprocess_frame_to_tiles(frame_rgb)

        for i, tile in enumerate(tiles):
            label, conf = predict_tile(tile)
            r, c, x, y = coords[i]
            print(f"[CAM {cam_id}] Tile {i} [{r},{c}] → {label} ({conf:.2f})")

            if label == "with_bird" and conf >= CONFIDENCE_THRESHOLD:
                print(f"[CAM {cam_id}] BIRD DETECTED at tile [{r},{c}]!")
                bird_found = True
                detected_cam = cam_id
                detected_tile = i
                detected_conf = conf
                detected_img = tiles[i]
                break
        if bird_found:
            break

    current_time = time.time()

    # --- STATE MACHINE LOGIC ---
    # States: 'IDLE', 'WARNING', 'SOUND_ON', 'DRONE_DEPLOYED'
    if 'bird_state' not in globals():
        bird_state = 'IDLE'
        warning_start_time = None
        sound_start_time = None
        sound_proc = None
        DRONE_DEPLOYED = False
        drone_started = False

    if bird_found:
        if bird_state == 'IDLE':
            warning_start_time = current_time
            bird_state = 'WARNING'
            print('First warning: Bird detected, starting 5s timer.')

        elif bird_state == 'WARNING':
            if current_time - warning_start_time >= BIRD_WARNING_THRESHOLD_SECONDS:
                # Activate sound deterrent
                if sound_proc is None or sound_proc.poll() is not None:
                    sound_proc = play_sound_deterent()
                    print(
                        f'Sound deterrent started after {BIRD_WARNING_THRESHOLD_SECONDS}s.')
                sound_start_time = current_time
                bird_state = 'SOUND_ON'

        elif bird_state == 'SOUND_ON':
            if current_time - sound_start_time >= BIRD_DRONE_THRESHOLD_SECONDS and not DRONE_DEPLOYED:
                # Deploy drone
                deploy_drone()
                DRONE_DEPLOYED = True
                drone_started = True
                print(
                    f'Drone deployed after {BIRD_DRONE_THRESHOLD_SECONDS}s of sound deterrent.')
            # Save detection image
            if detected_img is not None:
                # save_bird_logs(detected_cam, detected_tile, detected_conf)
                save_detected_bird(detected_img, detected_cam, detected_tile, detected_conf)
            # After drone finishes, reset everything
            if DRONE_DEPLOYED and drone_started:
                # Assume deploy_drone() is blocking and returns when done
                if sound_proc is not None and sound_proc.poll() is None:
                    sound_proc.terminate()
                    print('Sound deterrent stopped after drone.')
                    sound_proc = None
                bird_state = 'IDLE'
                warning_start_time = None
                sound_start_time = None
                DRONE_DEPLOYED = False
                drone_started = False
                print('System reset after drone mission.')

    else:
        # No bird detected, reset everything
        if sound_proc is not None and sound_proc.poll() is None:
            sound_proc.terminate()
            print('Sound deterrent stopped (no bird).')
            sound_proc = None
        if DRONE_DEPLOYED:
            try:
                tello = Tello()
                tello.connect()
                tello.land()
                print('Drone landed (no bird detected).')
            except Exception as e:
                print(f'Error landing drone: {str(e)}')
            DRONE_DEPLOYED = False
        bird_state = 'IDLE'
        warning_start_time = None
        sound_start_time = None
        drone_started = False

    print("Sleep...")
    time.sleep(LOOP_INTERVAL)
    loop_count = loop_count + 1

    if cv2.waitKey(1) & 0xFF == ord("q"):
        print("Stopping...")
        break

capture_one.release()
capture_two.release()
cv2.destroyAllWindows()
