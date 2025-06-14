# Bird Annotation - YOLOv8 Bird Detector

A quick guide to setting up your environment and training a YOLOv8 model for bird annotation using bird detection.

---

## 🛠️ Setup

### Install Dependencies
Install the required Python packages:
```bash
pip install opencv-python numpy matplotlib
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install ultralytics
```

---

## 🏷️ Annotating Images

If you want to annotate your images, you can use [LabelImg](https://github.com/HumanSignal/labelImg/releases) — a free and popular graphical image annotation tool. Download the latest release for your operating system from the official GitHub page above.

---

## 🚀 Training the Model

Train your YOLOv8 model on your bird dataset using the following command:
```bash
yolo detect train model=yolov8n.pt data=data.yaml epochs=30 imgsz=640 name=bird-detector augment=True
```
- `data`: Path to your dataset configuration file.
- `model`: Pretrained YOLOv8 model to start from.
- `epochs`: Number of training epochs.
- `imgsz`: Input image size.
- `name`: Name for your training run.

---

For more details, see the [Ultralytics YOLOv8 documentation](https://docs.ultralytics.com/).