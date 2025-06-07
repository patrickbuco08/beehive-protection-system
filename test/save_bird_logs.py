from pathlib import Path
import sys

# Add project root to sys.path so imports work
sys.path.append(str(Path(__file__).resolve().parent.parent))

from beehive_utils.logger import save_bird_logs


def test_save_bird_logs():
    cam_id = 1
    tile_id = 5
    confidence = 0.92

    save_bird_logs(cam_id, tile_id, confidence)

    # Verify log file was created
    log_path = Path(__file__).resolve().parent.parent / \
        "detections" / "logs.txt"
    assert log_path.exists(), "Log file was not created."

    print("✅ Log entry added successfully.")


if __name__ == "__main__":
    test_save_bird_logs()
