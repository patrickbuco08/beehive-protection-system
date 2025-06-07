import time

# --- Config ---
CONFIDENCE_THRESHOLD = 0.7
BIRD_WARNING_THRESHOLD_SECONDS = 5   # Time before activating sound deterrent
BIRD_DRONE_THRESHOLD_SECONDS = 10    # Time after sound before deploying drone
LOOP_INTERVAL = 1  # Faster loop for test
TOTAL_TEST_LOOPS = 20

# --- Mocked State ---


def handle_idle(state, current_time):
    state['warning_start_time'] = current_time
    state['bird_state'] = 'WARNING'
    print('First warning: Bird detected, starting timer.')


def handle_warning(state, current_time):
    elapsed = current_time - state['warning_start_time']
    if elapsed >= BIRD_WARNING_THRESHOLD_SECONDS:
        print(
            f'Sound deterrent started after {BIRD_WARNING_THRESHOLD_SECONDS}s.')
        state['sound_start_time'] = current_time
        state['bird_state'] = 'SOUND_ON'
    else:
        print(f'WARNING: {elapsed:.2f}s elapsed, waiting for sound trigger.')


def handle_sound_on(state, current_time):
    elapsed = current_time - state['sound_start_time']
    if elapsed >= BIRD_DRONE_THRESHOLD_SECONDS and not state['DRONE_DEPLOYED']:
        print(
            f'Drone deployed after {BIRD_DRONE_THRESHOLD_SECONDS}s of sound deterrent.')
        state['DRONE_DEPLOYED'] = True
        state['drone_started'] = True
    else:
        print(f'SOUND_ON: {elapsed:.2f}s elapsed, waiting for drone trigger.')
    if state['DRONE_DEPLOYED'] and state['drone_started']:
        print('System reset after drone mission.')
        reset_state(state)


def reset_state(state):
    state['bird_state'] = 'IDLE'
    state['warning_start_time'] = None
    state['sound_start_time'] = None
    state['DRONE_DEPLOYED'] = False
    state['drone_started'] = False


def main():
    print('Starting logic test...')
    print(f"Current time: {time.time()}")
    loop_count = 0

    state = {
        'bird_state': 'IDLE',
        'warning_start_time': None,
        'sound_start_time': None,
        'DRONE_DEPLOYED': False,
        'drone_started': False
    }

    state_handlers = {
        'IDLE': handle_idle,
        'WARNING': handle_warning,
        'SOUND_ON': handle_sound_on
    }

    while loop_count < TOTAL_TEST_LOOPS:
        # Mock detection: always bird, always confident
        label = 'with_bird'
        conf = 0.99
        bird_found = label == 'with_bird' and conf >= CONFIDENCE_THRESHOLD

        current_time = time.time()
        print(f"\n[Loop {loop_count}] State: {state['bird_state']}")

        if bird_found:
            handler = state_handlers.get(state['bird_state'])
            if handler:
                handler(state, current_time)
        else:
            if state['bird_state'] != 'IDLE':
                print('No bird detected, resetting state.')
            reset_state(state)

        loop_count += 1
        # Prompt for user input to allow quitting
        user_input = input(
            "Press [q] then Enter to quit, or just Enter to continue: ")
        if user_input.strip().lower() == 'q':
            print('Terminated by user.')
            break
        time.sleep(LOOP_INTERVAL)

    print('Test complete.')


if __name__ == '__main__':
    main()
