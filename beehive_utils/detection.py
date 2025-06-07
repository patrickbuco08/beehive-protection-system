from beehive_utils.config import MODEL_INPUT_SIZE, MODEL_CLASS_NAMES
import cv2
import numpy as np


# Usage:
# tiles, coords = preprocess_frame_to_tiles(frame)  # Defaults to (4, 4)
# tiles, coords = preprocess_frame_to_tiles(frame, (8, 8))
def preprocess_frame_to_tiles(frame, tile_shape=(4, 4)):
    tiles = []
    coords = []
    rows, cols = tile_shape
    height, width = frame.shape[:2]
    tile_h, tile_w = height // rows, width // cols

    for r in range(rows):
        for c in range(cols):
            y1, y2 = r * tile_h, (r + 1) * tile_h
            x1, x2 = c * tile_w, (c + 1) * tile_w
            tile = frame[y1:y2, x1:x2]
            tiles.append(tile)
            coords.append((r, c, x1, y1))

    return tiles, coords


def predict_tile(tile, interpreter, input_details, output_details):
    img = cv2.resize(tile, MODEL_INPUT_SIZE).astype(np.float32) / 255.0
    img = np.expand_dims(img, axis=0)
    interpreter.set_tensor(input_details[0]['index'], img)
    interpreter.invoke()
    output = interpreter.get_tensor(output_details[0]['index'])
    pred_class = np.argmax(output[0])
    confidence = output[0][pred_class]
    return MODEL_CLASS_NAMES[pred_class], confidence
