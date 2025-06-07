from djitellopy import Tello
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

        # Configurable movement variables
        forward_distance_cm = 100
        speed_cm_per_sec = 20
        forward_duration_sec = forward_distance_cm / speed_cm_per_sec

        # Move forward
        tello.send_rc_control(0, speed_cm_per_sec, 0, 0)
        time.sleep(forward_duration_sec)
        tello.send_rc_control(0, 0, 0, 0)
        print(f"➡️ Moved forward {forward_distance_cm}cm")

        time.sleep(1)

        # Move back
        tello.send_rc_control(0, -speed_cm_per_sec, 0, 0)
        time.sleep(forward_duration_sec)
        tello.send_rc_control(0, 0, 0, 0)
        print(f"⬅️ Returned backward {forward_distance_cm}cm")

        time.sleep(1)

        tello.land()
        print("✅ Drone landed successfully")

    except Exception as e:
        print(f"⚠️ Drone error: {str(e)}")
        print("❌ Flight mission aborted, continuing system...")

deploy_drone()