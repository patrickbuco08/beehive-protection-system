from beehive_utils.model import load_beehive_model

interpreter, input_details, output_details = load_beehive_model()

print("✅ Model loaded with LiteRT!")
print("📥 Input shape:", input_details[0]['shape'])
print("📤 Output shape:", output_details[0]['shape'])
