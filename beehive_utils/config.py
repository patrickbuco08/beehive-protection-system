PREDICTION_SCORE_THRESHOLD = 0.8
DRONE_FORWARD_DISTANCE = 100  # distance in cm
SOUND_FILES = [
    'alarm sound.wav',
    'boom sound.wav',
    'construction.wav',
    'gun shots.wav',
    'hawk sound.wav',
    'police siren.wav',
    'tactical nuke alarm.wav'
]

MODEL_NAME = "bird_detection_model_v3.1.tflite"
MODEL_INPUT_SIZE = (180, 180)
MODEL_CLASS_NAMES = ['no_bird', 'with_bird']

TILE_SHAPES = [(4, 4), (6, 6), (8, 8)]
CONFIDENCE_THRESHOLD = 0.70
