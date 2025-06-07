from djitellopy import Tello
import time


# go to your env by typing source beehiveenv/bin/activate
# then type pip show djitellopy. it should show the name, version, etc.

# make sure your rpi is connected to tello hotspot TELO-XXXXX

def deploy_drone():
    print("🚁 Drone: Starting mission...")

    forward_distance = 100  # distance in cm

    try:
        tello = Tello()
        tello.connect()
        print("✅ Drone connected")

        time.sleep(2)

        tello.takeoff()
        print("🛫 Drone took off")

        tello.move_forward(forward_distance)
        print(f"➡️ Moved forward {forward_distance}cm")

        time.sleep(1)

        tello.move_back(forward_distance)
        print(f"⬅️ Returned backward {forward_distance}cm")

        tello.land()
        print("✅ Drone landed successfully")

    except Exception as e:
        print(f"⚠️ Drone error: {str(e)}")
        print("❌ Flight mission aborted, continuing system...")


deploy_drone()
