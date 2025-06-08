from pathlib import Path
from beehive_utils.config import MODEL_NAME

# from ai_edge_litert.interpreter import Interpreter

# if using rpi/linux:
# import tflite_runtime.interpreter as tflite

# if using windows/mac:
import tensorflow as tf
tflite = tf.lite

model_path = Path(__file__).resolve().parent.parent / "models" / MODEL_NAME


def load_beehive_model():
    interpreter = tflite.Interpreter(model_path=str(model_path))
    # interpreter = Interpreter(model_path=str(model_path))
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    return interpreter, input_details, output_details


def load_beehive_model_tflite():
    interpreter = tflite.Interpreter(model_path=str(model_path))
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    return interpreter, input_details, output_details
