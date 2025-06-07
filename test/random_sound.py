import sys
from pathlib import Path
import time

# Add project root to sys.path
from beehive_utils.sound import play_sound_deterent



def main():
    test_sound = play_sound_deterent()
    time.sleep(5)
    test_sound.terminate()

if __name__ == '__main__':
    main()
