# Apis Mellifera Beehive Protection System

A smart, modular system for automatic bird detection and deterrence using computer vision, sound, and drone deployment. Designed for Raspberry Pi and compatible with DJI Tello drones.

---

## 🚀 Project Overview
This project uses a camera, sound deterrents, and a drone to protect beehives from birds. It leverages deep learning (TensorFlow Lite) for real-time bird detection and can auto-deploy a drone for further deterrence.

## ✨ Features
- Real-time bird detection using TFLite models
- Modular tile-based image processing
- Sound deterrent activation
- Automated drone deployment (DJI Tello)
- Logging and image saving for detected events
- Easy testing for camera, model, sound, and drone
- Auto-run configuration for headless startup

## 🛠️ Requirements
- Raspberry Pi (recommended) or Linux PC
- Python 3.11+
- Compatible camera
- DJI Tello drone (optional)
- Speakers for sound deterrent

## 📦 Installation

### 1. Create and Activate Virtual Environment
```bash
python3.11 -m venv beehiveenv
```

- **On Linux/macOS:**
  ```bash
  source beehiveenv/bin/activate
  ```
- **On Windows (cmd):**
  ```cmd
  beehiveenv\Scripts\activate
  ```
- **On Windows (PowerShell):**
  ```powershell
  beehiveenv\Scripts\Activate.ps1
  ```

### 🐍 Using Conda Environments

#### Create a new conda environment (e.g., named birdenv) with Python 3.11:
```bash
conda create -n beehiveenv python=3.9
```

#### List all available conda environments:
```bash
conda env list
# or
conda info --envs
```

#### Activate a conda environment:
```bash
conda activate beehiveenv
```

#### Deactivate the current environment:
```bash
conda deactivate
```

### 2. Install System Dependencies
```bash
sudo apt update
sudo apt install -y \
  ffmpeg libavdevice-dev libavfilter-dev libavformat-dev \
  libavcodec-dev libavutil-dev libswscale-dev libswresample-dev \
  libv4l-dev pkg-config build-essential python3.11-dev \
  libjpeg-dev libtiff5 libpng-dev
```

### 3. Upgrade pip and Install Python Libraries
```bash
pip install --upgrade pip
pip install numpy==1.24.4 cython opencv-python av
```

### 4. Install TensorFlow Lite Runtime
```bash
pip install tflite-runtime
```

### 5. Install DJI Drone Control Library
```bash
pip install djitellopy
```

### 6. Install Project Utilities
```bash
pip install -e .
```

### 7. (Optional) Install AI Edge Lite Runtime
```bash
pip install ai-edge-litert
```

---

## 🧑‍💻 Usage

### 1. Activate the Virtual Environment
```bash
source beehiveenv/bin/activate
```

### 2. Run Tests and Main Scripts
- **Test Camera:**
  ```bash
  python test/check_camera.py
  ```
- **Test Model:**
  ```bash
  python test/model_litert.py
  python test/model_tflite.py
  ```
- **Test Sound:**
  ```bash
  python test/random_sound.py
  ```
- **Test Drone:**
  ```bash
  python test/drone.py
  ```
- **Run Bird Detection System:**
  ```bash
  python main.py
  ```

---

## ⚙️ Auto-Run Configuration (Headless / On Boot)

### 1. Auto-Connect to Tello WiFi
Edit your wpa_supplicant config:
```bash
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
```
Add:
```conf
network={
    ssid="TELLO-XXXXXX"
    key_mgmt=NONE
}
```
Save and exit (Ctrl+X, Y, Enter).

### 2. Auto-Start Bird Detection on Boot
- Move `startup_bird_detection.sh` to `/home/beehive` (not Desktop).
- Copy `connection_success.wav` to Desktop (or your desired location).
- Make the script executable:
  ```bash
  chmod +x /home/beehive/startup_bird_detection.sh
  ```
- Add to crontab for auto-run at boot:
  ```bash
  crontab -e
  ```
  Add this line:
  ```cron
  @reboot /home/beehive/startup_bird_detection.sh
  ```

---

## 🧪 Testing & Troubleshooting
- **To kill a running script:**
  ```bash
  pkill -f rpi_bird_detection_v1.py
  ```
- **If you encounter issues:**
  - Double-check all dependencies are installed.
  - Ensure your virtual environment is activated.
  - Confirm the camera and drone are connected and working.
  - Review log/output messages for hints.

---

## 📄 License
[MIT License](LICENSE)  
Feel free to use, modify, and contribute!

---

For questions, suggestions, or contributions, please open an issue or pull request.