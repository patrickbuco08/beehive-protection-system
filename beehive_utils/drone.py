from djitellopy import Tello
from beehive_utils.config import DRONE_FORWARD_DISTANCE

import time


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
