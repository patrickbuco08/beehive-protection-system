import cv2
import numpy as np

from beehive_utils.config import MODEL_INPUT_SIZE, MODEL_CLASS_NAMES, TILE_SHAPES, CONFIDENCE_THRESHOLD
from beehive_utils.logger import save_detected_bird

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


def is_bird_detected_in_tiles(frame, interpreter, input_details, output_details):
    """
    Checks if a bird is detected in any tile of the frame using multiple tile shapes.
    Returns True as soon as a tile with 'with_bird' and confidence >= CONFIDENCE_THRESHOLD is found, otherwise False.
    """
    for tile_shape in TILE_SHAPES:
        print(f"\n--- Processing with tile shape: {tile_shape} ---")
        tiles, coords = preprocess_frame_to_tiles(frame, tile_shape)
        for i, tile in enumerate(tiles):
            label, conf = predict_tile(
                tile, interpreter, input_details, output_details)
            r, c, x, y = coords[i]

            # save_detected_bird(tiles[i], 1, i, conf) # enable this when you want to generate dataset

            if label == "with_bird" and conf >= CONFIDENCE_THRESHOLD:
                print(
                    f"bird detected at tile_shape {tile_shape} (tile {i}) confidence {conf:.2f} [{r},{c}] [{x},{y}]")

                # comment this when you want to generate dataset
                save_detected_bird(tiles[i], 1, i, conf)
                return True

    return False
