import cv2


def draw_grid(frame, grid_size=(8, 8), color=(0, 255, 0), thickness=1):
    """
    Draws a grid overlay on the given frame.
    Args:
        frame: The image (numpy array) to draw on.
        grid_size: Tuple (rows, cols) for the grid.
        color: BGR color tuple for the grid lines.
        thickness: Line thickness.
    Returns:
        The frame with the grid drawn on it.
    """
    h, w, _ = frame.shape
    rows, cols = grid_size
    # Draw vertical lines
    for i in range(1, cols):
        x = int(w * i / cols)
        cv2.line(frame, (x, 0), (x, h), color, thickness)
    # Draw horizontal lines
    for i in range(1, rows):
        y = int(h * i / rows)
        cv2.line(frame, (0, y), (w, y), color, thickness)
    return frame


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
