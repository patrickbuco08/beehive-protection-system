from djitellopy import Tello
from beehive_utils.config import DRONE_FORWARD_DISTANCE

import time

def force_land_drone():
    """
    Attempts to force land the Tello drone, handling connection and landing exceptions gracefully.
    Useful for emergency or programmatic landing scenarios.
    """
    try:
        tello = Tello()
        tello.connect()
        tello.land()
        print('Drone landed (force_land_drone).')
    except Exception as e:
        print(f'Error landing drone: {str(e)}')


def deploy_drone():
    print("🚁 Drone: Starting mission...")

    try:
        tello = Tello()
        tello.connect()
        print("✅ Drone connected")

        time.sleep(2)

        tello.takeoff()
        print("🛫 Drone took off")

        tello.move_forward(DRONE_FORWARD_DISTANCE)
        print(f"➡️ Moved forward {DRONE_FORWARD_DISTANCE}cm")

        time.sleep(1)

        tello.move_back(DRONE_FORWARD_DISTANCE)
        print(f"⬅️ Returned backward {DRONE_FORWARD_DISTANCE}cm")

        tello.land()
        print("✅ Drone landed successfully")

    except Exception as e:
        print(f"⚠️ Drone error: {str(e)}")
        print("❌ Flight mission aborted, continuing system...")
