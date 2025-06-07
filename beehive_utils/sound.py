import random
import subprocess
import platform

from beehive_utils.config import SOUND_FILES
from pathlib import Path

# Absolute path to assets/sounds
SOUND_DIR = Path(__file__).resolve().parent / "assets" / "sounds"


def play_sound_deterent():
    audio_player_cmd = _get_audio_player_command()
    selected_sound = random.choice(SOUND_FILES)
    sound_path = SOUND_DIR / selected_sound

    print(f"🔊 Playing sound: {selected_sound}")

    if not sound_path.exists():
        raise FileNotFoundError(f"Sound file not found: {sound_path}")

    return subprocess.Popen([audio_player_cmd, str(sound_path)])


def _get_audio_player_command():
    system = platform.system()

    if system == "Darwin":
        return "afplay"
    elif system == "Windows":
        return "afplay"
    elif system == "Linux":
        return "aplay"
    else:
        raise RuntimeError(f"Unsupported system: {system}")
