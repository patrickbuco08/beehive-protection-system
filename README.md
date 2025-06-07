1. Create and Activate Virtual Environment
python3.11 -m venv beehiveenv
source beehiveenv/bin/activate

2. Install System Dependencies
sudo apt update
sudo apt install -y \
  ffmpeg libavdevice-dev libavfilter-dev libavformat-dev \
  libavcodec-dev libavutil-dev libswscale-dev libswresample-dev \
  libv4l-dev pkg-config build-essential python3.11-dev \
  libjpeg-dev libtiff5 libpng-dev

3. Upgrade pip and install required Python libraries
pip install --upgrade pip
pip install numpy==1.24.4 cython
pip install opencv-python
pip install av

4. Install TensorFlow Lite Runtime
pip install tflite-runtime

5. Install DJI Drone Control Library
pip install djitellopy

source beehiveenv/bin/activate


#instructions
before executing the python file, use the virtual environment, type:
source beehiveenv/bin/activate

beehiveenv C:\Users\User>

then go to Desktop
cd Desktop

to test the opencv, type:
python test_camera.py

to test the model, type:
python test_model.py

to test the sound, type:
python test_sound.py

to test the drone, type:
python test_drone.py

to run bird detection system, type:
python rpi_bird_detection.py


#auto run configuration

# Auto-connect to Tello WiFi

open terminal and then execute this command:
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf

then add this line:
network={
    ssid="TELLO-XXXXXX"
    key_mgmt=NONE
}

save and exit (Ctrl+X, Y, Enter)

# find startup_bird_detection.sh and move it to /home/beehive folder (not Desktop)
copy paste connection_success.wav to Desktop

# Make it executable
chmod +x /home/beehive/startup_bird_detection.sh

# Add to crontab
crontab -e

then add:
@reboot /home/beehive/startup_bird_detection.sh

# How to kill running script?
pkill -f rpi_bird_detection_v1.py

# install beehive_utils
pip install -e .

# install ai_edge_litert
pip install ai_edge_litert