import time

# --- Config ---
CONFIDENCE_THRESHOLD = 0.7
BIRD_WARNING_THRESHOLD_SECONDS = 5   # Time before activating sound deterrent
BIRD_DRONE_THRESHOLD_SECONDS = 10    # Time after sound before deploying drone
LOOP_INTERVAL = 1  # Faster loop for test
TOTAL_TEST_LOOPS = 20

# --- Mocked State ---
loop_count = 0
bird_state = 'IDLE'
warning_start_time = None
sound_start_time = None
sound_proc = None
DRONE_DEPLOYED = False
drone_started = False

print('Starting logic test...')

current_time = time.time()
print(f"Current time: {current_time}")

while loop_count < TOTAL_TEST_LOOPS:
    # Mock detection: always bird, always confident
    label = 'with_bird'
    conf = 0.99
    detected_img = 'mock_img'  # placeholder
    detected_cam = 0
    detected_tile = 0
    detected_conf = conf
    bird_found = label == 'with_bird' and conf >= CONFIDENCE_THRESHOLD

    current_time = time.time()
    print(f"\n[Loop {loop_count}] State: {bird_state}")

    if bird_found:
        if bird_state == 'IDLE':
            warning_start_time = current_time
            bird_state = 'WARNING'
            print('First warning: Bird detected, starting timer.')
        elif bird_state == 'WARNING':
            if current_time - warning_start_time >= BIRD_WARNING_THRESHOLD_SECONDS:
                print(f'Sound deterrent started after {BIRD_WARNING_THRESHOLD_SECONDS}s.')
                sound_start_time = current_time
                bird_state = 'SOUND_ON'
            else:
                print(f'WARNING: {current_time - warning_start_time:.2f}s elapsed, waiting for sound trigger.')
        elif bird_state == 'SOUND_ON':
            if current_time - sound_start_time >= BIRD_DRONE_THRESHOLD_SECONDS and not DRONE_DEPLOYED:
                print(f'Drone deployed after {BIRD_DRONE_THRESHOLD_SECONDS}s of sound deterrent.')
                DRONE_DEPLOYED = True
                drone_started = True
            else:
                print(f'SOUND_ON: {current_time - sound_start_time:.2f}s elapsed, waiting for drone trigger.')
            if DRONE_DEPLOYED and drone_started:
                print('System reset after drone mission.')
                bird_state = 'IDLE'
                warning_start_time = None
                sound_start_time = None
                DRONE_DEPLOYED = False
                drone_started = False
    else:
        if bird_state != 'IDLE':
            print('No bird detected, resetting state.')
        bird_state = 'IDLE'
        warning_start_time = None
        sound_start_time = None
        DRONE_DEPLOYED = False
        drone_started = False

    loop_count += 1
    time.sleep(LOOP_INTERVAL)

print('Test complete.')
