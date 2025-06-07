import cv2
from beehive_utils.camera import get_available_cameras

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

    # Set resolution (optional)
    for cap in [capture_one]:
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # Display both camera feeds
    while True:
        ret1, frame1 = capture_one.read()

        if ret1:
            cv2.imshow("Camera 1", frame1)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    capture_one.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
