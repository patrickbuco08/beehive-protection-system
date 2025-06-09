import cv2
from beehive_utils.camera import get_available_cameras, draw_grid


def main():
    # Get camera indexes
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
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    # Display camera feed with grid
    while True:
        for cam_id, cap in enumerate(filter(None, [capture_one, capture_two])):
            ret, frame = cap.read()

            if not ret:
                print(f"Camera {cam_id} failed to read frame.")
                continue

            frame_with_grid = draw_grid(frame.copy(), grid_size=(8, 8))
            cv2.imshow(f"Camera {cam_id} with Grid", frame_with_grid)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    capture_one.release()
    capture_two.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
