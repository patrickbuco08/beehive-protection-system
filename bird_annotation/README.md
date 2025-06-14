# Bird Annotation - YOLOv8 Bird Detector

A quick guide to setting up your environment and training a YOLOv8 model for bird annotation using bird detection.

---

## 🛠️ Setup

### 1. Create the Conda Environment
Create a new conda environment with Python 3.10:
```bash
conda create -n bird-detector python=3.10 -y
```

### 2. Activate the Environment
Activate the environment you just created:
```bash
conda activate bird-detector
```

### 3. Install Dependencies
Install the required Python packages:
```bash
pip install opencv-python numpy matplotlib
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install ultralytics
```

---

## 🚀 Training the Model

Train your YOLOv8 model on your bird dataset using the following command:
```bash
yolo detect train \
  data=data.yaml \
  model=yolov8n.pt \
  epochs=10 \
  imgsz=640 \
  name=bird-detector
```
- `data`: Path to your dataset configuration file.
- `model`: Pretrained YOLOv8 model to start from.
- `epochs`: Number of training epochs.
- `imgsz`: Input image size.
- `name`: Name for your training run.

---

For more details, see the [Ultralytics YOLOv8 documentation](https://docs.ultralytics.com/).