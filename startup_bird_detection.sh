#!/bin/bash

echo "🐝 Beehive system starting..."

# Wait until WiFi (Tello) is connected and Pi has an IP
until ping -c1 8.8.8.8 &>/dev/null; do
    echo "🔄 Waiting for WiFi connection to TELLO..."
    sleep 2
done

echo "✅ WiFi connected to Tello!"

# Play sound to confirm connection
aplay /home/beehive/Desktop/connection_success.wav

# Activate virtual environment
source /home/beehive/beehiveenv/bin/activate

# Run detection script
python /home/beehive/Desktop/rpi_bird_detection_v1.py