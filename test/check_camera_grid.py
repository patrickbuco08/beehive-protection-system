import cv2
import time
from beehive_utils.camera import get_available_cameras, draw_grid
from beehive_utils.detection import is_bird_detected_in_tiles
from beehive_utils.model import load_beehive_model


def main():

    # --- Load Model ---
    interpreter, input_details, output_details = load_beehive_model()

    # Camera Setup
    camera_indexes = get_available_cameras()
    print("Available cameras:", camera_indexes)

    # Setup cameras dynamically
    if len(camera_indexes) < 1:
        print("Not enough working cameras found!")
        exit()

    # Setup cameras
    capture_one = cv2.VideoCapture(camera_indexes[0])
    capture_two = None

    # Set resolution (optional)
    for cap in filter(None, [capture_one, capture_two]):
        # 640x480 or 800x600
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # Display camera feed with grid
    while True:
        for cam_id, cap in enumerate(filter(None, [capture_one, capture_two])):
            ret, frame = cap.read()

            if not ret:
                print(f"Camera {cam_id} failed to read frame.")
                continue

            frame_with_grid = draw_grid(frame.copy(), grid_size=(8, 8))
            cv2.imshow(f"Camera {cam_id} with Grid", frame_with_grid)

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            bird_detected = is_bird_detected_in_tiles(
                frame_rgb,
                interpreter,
                input_details,
                output_details
            )

            print(f"Bird detected: {bird_detected}")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        time.sleep(0.1)

    for cap in filter(None, [capture_one, capture_two]):
        cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
