"""
Main entry point for APIS Mellifera Beehive Bird Detection System.
Handles camera input, detection state machine, deterrents, and drone deployment.
"""
import cv2
import time

from djitellopy import Tello
from beehive_utils.model import load_beehive_model
from beehive_utils.detection import is_bird_detected_in_tiles
from beehive_utils.sound import play_sound_deterent
from beehive_utils.drone import deploy_drone
from beehive_utils.camera import get_available_cameras

# --- Main Configuration ---
LOOP_INTERVAL = 1  # seconds between detection cycles
BIRD_WARNING_THRESHOLD_SECONDS = 5   # Time before activating sound deterrent
BIRD_DRONE_THRESHOLD_SECONDS = 10    # Time after sound before deploying drone

# --- Load Model ---
interpreter, input_details, output_details = load_beehive_model()

# --- Camera Setup ---
camera_indexes = get_available_cameras()
print("Available cameras:", camera_indexes)
if not camera_indexes:
    print("No working cameras found!")
    exit()

capture_one = cv2.VideoCapture(camera_indexes[0])

if len(camera_indexes) < 1:
    print("Not enough working cameras found!")
    exit()

for cap in filter(None, [capture_one]):
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

# --- State Variables ---
bird_state = 'IDLE'
warning_start_time = None
sound_start_time = None
sound_proc = None
drone_deployed = False
drone_started = False
loop_count = 20

while True:
    bird_found = False
    detected_cam = None

    # Check all available cameras
    for cam_id, cap in enumerate(filter(None, [capture_one])):
        ret, frame = cap.read()
        if not ret:
            print(f"❌ Failed to read from camera {cam_id}")
            continue
        frame = cv2.rotate(frame, cv2.ROTATE_180)
        cv2.imshow(f'Camera {cam_id} Feed', frame)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        bird_detected = is_bird_detected_in_tiles(
            frame_rgb,
            interpreter,
            input_details,
            output_details
        )
        if bird_detected:
            bird_found = True
            detected_cam = cam_id
            break

    current_time = time.time()

    # --- STATE MACHINE LOGIC ---
    if bird_found:
        if bird_state == 'IDLE':
            warning_start_time = current_time
            bird_state = 'WARNING'
            print('First warning: Bird detected, starting timer.')
        elif bird_state == 'WARNING':
            if current_time - warning_start_time >= BIRD_WARNING_THRESHOLD_SECONDS:
                if sound_proc is None or sound_proc.poll() is not None:
                    sound_proc = play_sound_deterent()
                    print('Sound deterrent started.')
                sound_start_time = current_time
                bird_state = 'SOUND_ON'
        elif bird_state == 'SOUND_ON':
            if current_time - sound_start_time >= BIRD_DRONE_THRESHOLD_SECONDS and not drone_deployed:
                deploy_drone()
                drone_deployed = True
                drone_started = True
                print('Drone deployed.')
            # After drone finishes, reset everything
            if drone_deployed and drone_started:
                if sound_proc is not None and sound_proc.poll() is None:
                    sound_proc.terminate()
                    print('Sound deterrent stopped after drone.')
                    sound_proc = None

                bird_state = 'IDLE'
                warning_start_time = None
                sound_start_time = None
                drone_deployed = False
                drone_started = False
                print('System reset after drone mission.')
    else:
        # No bird detected, reset everything
        if sound_proc is not None and sound_proc.poll() is None:
            sound_proc.terminate()
            print('Sound deterrent stopped (no bird).')
            sound_proc = None
        if drone_deployed:
            try:
                tello = Tello()
                tello.connect()
                tello.land()
                print('Drone landed (no bird detected).')
            except Exception as e:
                print(f'Error landing drone: {str(e)}')
            drone_deployed = False
        bird_state = 'IDLE'
        warning_start_time = None
        sound_start_time = None
        drone_started = False

    print("Sleep...")
    time.sleep(LOOP_INTERVAL)
    loop_count += 1

    # Break on 'q' or window close
    if cv2.waitKey(1) & 0xFF == ord("q"):
        print("Stopping...")
        break

for cap in filter(None, [capture_one]):
    cap.release()
cv2.destroyAllWindows()
