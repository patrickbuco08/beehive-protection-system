
import cv2
import time
from beehive_utils.model import load_beehive_model
from beehive_utils.detection import is_bird_detected_in_tiles
from beehive_utils.sound import play_sound_deterent
from beehive_utils.drone import deploy_drone, force_land_drone
from beehive_utils.camera import get_available_cameras

# --- Helper Functions ---


def reset_system_state():
    global bird_state, warning_start_time, sound_start_time, drone_deployed, drone_started
    bird_state = 'IDLE'
    warning_start_time = None
    sound_start_time = None
    drone_deployed = False
    drone_started = False


def stop_sound_deterrent(message):
    global sound_proc
    if sound_proc is not None and sound_proc.poll() is None:
        sound_proc.terminate()
        print(message)
        sound_proc = None


def main():
    global sound_proc, drone_deployed, drone_started, bird_state, warning_start_time, sound_start_time

    # --- Main Configuration ---
    LOOP_INTERVAL = 0.1  # seconds between detection cycles
    BIRD_WARNING_THRESHOLD_SECONDS = 5   # Time before activating sound deterrent
    BIRD_DRONE_THRESHOLD_SECONDS = 10    # Time after sound before deploying drone

    # --- Load Model ---
    interpreter, input_details, output_details = load_beehive_model()

    # --- Camera Setup ---
    available_cameras = get_available_cameras()

    print(f"Available cameras: {available_cameras}")
    if len(available_cameras) < 2:
        print("Two cameras are required for this script.")
        return
    capture_one = cv2.VideoCapture(available_cameras[0])
    capture_two = cv2.VideoCapture(available_cameras[1])

    # Set both cameras to 1280x720 (16:9, lighter than 1920x1080)
    for cap in [capture_one, capture_two]:
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    # --- State Variables ---
    bird_state = 'IDLE'
    warning_start_time = None
    sound_start_time = None
    sound_proc = None
    drone_deployed = False
    drone_started = False

    while True:
        bird_found = False
        # --- Camera Read Loop ---
        for cam_id, cap in enumerate([capture_one, capture_two]):
            ret, frame = cap.read()
            if not ret:
                print(f"❌ Failed to read from camera {cam_id}")
                continue
            # No display to save CPU
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            bird_detected = is_bird_detected_in_tiles(
                frame_rgb,
                interpreter,
                input_details,
                output_details,
                cam_id,
                with_image_logger=False,
                with_text_logger=True
            )
            if bird_detected:
                bird_found = True
                break

        current_time = time.time()

        if bird_found:
            if bird_state == 'IDLE':
                print("👀 Ohh, I detected a bird! Let's keep an eye on it...")
                warning_start_time = current_time
                bird_state = 'WARNING'
            elif bird_state == 'WARNING':
                print("🤔 Hmm, the bird is still here... Should I do something?")
                if current_time - warning_start_time >= BIRD_WARNING_THRESHOLD_SECONDS:
                    print("🔊 Enough waiting! Time to scare it off with some sound!")
                    if sound_proc is None or sound_proc.poll() is not None:
                        sound_proc = play_sound_deterent()
                        print('Sound deterrent started.')
                    sound_start_time = current_time
                    bird_state = 'SOUND_ON'
            elif bird_state == 'SOUND_ON':
                print("🎵 I'm making noise, but the bird is still hanging around...")
                if current_time - sound_start_time >= BIRD_DRONE_THRESHOLD_SECONDS and not drone_deployed:
                    print("🚁 Deploying the drone now, wish me luck!")
                    deploy_drone()
                    print("Drone finished.")
                    drone_deployed = True
                    drone_started = True
                # After drone finishes, reset everything
                if drone_deployed and drone_started:
                    print(
                        "✅ Mission complete! Resetting system for next bird encounter.")
                    stop_sound_deterrent(
                        'Sound deterrent stopped after drone.')
                    reset_system_state()
                    print('System reset after drone mission.')
        else:
            stop_sound_deterrent('Sound deterrent stopped (no bird).')
            if drone_deployed:
                force_land_drone()
                drone_deployed = False
            reset_system_state()

        # Break on 'q' or window close
        if cv2.waitKey(1) & 0xFF == ord("q"):
            if sound_proc is not None and sound_proc.poll() is None:
                sound_proc.terminate()
                print('Sound deterrent stopped (no bird).')
            print("Stopping...")
            break
        time.sleep(LOOP_INTERVAL)

    for cap in filter(None, [capture_one, capture_two]):
        cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
