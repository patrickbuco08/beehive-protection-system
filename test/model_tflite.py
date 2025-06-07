from beehive_utils.model import load_beehive_model_tflite

interpreter, input_details, output_details = load_beehive_model_tflite()

print("✅ Model loaded successfully!")
print("📥 Input shape:", input_details[0]['shape'])
print("📤 Output shape:", output_details[0]['shape'])
