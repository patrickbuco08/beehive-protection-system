import cv2


def list_available_cameras(max_index=4):
    print("Scanning for available cameras...\n")
    available_cameras = []

    for index in range(max_index):
        cap = cv2.VideoCapture(index)
        if cap.isOpened():
            ret, _ = cap.read()
            if ret:
                print(f"Camera found at index {index}")
                available_cameras.append(index)
            else:
                print(f"Camera at index {index} opened but failed to read.")
            cap.release()
        else:
            print(f"No camera at index {index}")

    if not available_cameras:
        print("No available cameras found.")
    else:
        print(f"Available camera indexes: {available_cameras}")


def get_available_cameras(max_index=3):
    print("Scanning for available cameras...\n")
    working_indexes = []
    for i in range(max_index):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ret, _ = cap.read()
            if ret:
                working_indexes.append(i)
            cap.release()

    return working_indexes
