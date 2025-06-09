import cv2
import time
from beehive_utils.camera import draw_grid
from beehive_utils.detection import is_bird_detected_in_tiles
from beehive_utils.model import load_beehive_model


def main():

    # --- Load Model ---
    interpreter, input_details, output_details = load_beehive_model()

    # Load image instead of using camera
    image_path = "test_images/test-image.jpg"  # Update this path as needed
    frame = cv2.imread(image_path)
    if frame is None:
        print(f"Failed to load image: {image_path}")
        exit()

    while True:
        # Draw grid on the image
        frame_with_grid = draw_grid(frame.copy(), grid_size=(8, 8))

        # Resize for smaller popup window
        display_width = 640
        h, w = frame_with_grid.shape[:2]
        scale = display_width / w if w > display_width else 1.0
        display_dim = (int(w * scale), int(h * scale))
        resized_frame = cv2.resize(
            frame_with_grid, display_dim, interpolation=cv2.INTER_AREA)
        cv2.imshow("Image with Grid", resized_frame)

        # Convert to RGB for detection
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        bird_detected = is_bird_detected_in_tiles(
            frame_rgb,
            interpreter,
            input_details,
            output_details,
            with_logger=True
        )

        if bird_detected:
            print(f"Bird detected: {bird_detected}")
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        time.sleep(0.1)


if __name__ == '__main__':
    main()
