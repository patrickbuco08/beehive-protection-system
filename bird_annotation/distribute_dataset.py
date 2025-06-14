import os
import shutil
import random

# Set the random seed for reproducibility
random.seed(42)

# Define paths
source_dir = os.path.join(os.path.dirname(__file__), 'dataset_label_first_batch')
target_dir = os.path.join(os.path.dirname(__file__), 'bird-dataset')

# Define train/val split ratio
train_ratio = 0.8

# Get all image files
image_files = [f for f in os.listdir(source_dir) if f.lower().endswith('.jpg')]
image_files.sort()

# Determine split
num_images = len(image_files)
num_train = int(num_images * train_ratio)

# Randomly shuffle the files
random.shuffle(image_files)

# Split into train and val sets
train_images = image_files[:num_train]
val_images = image_files[num_train:]

# Ensure target directories exist
dirs_to_create = [
    os.path.join(target_dir, 'images', 'train'),
    os.path.join(target_dir, 'images', 'val'),
    os.path.join(target_dir, 'labels', 'train'),
    os.path.join(target_dir, 'labels', 'val')
]

for dir_path in dirs_to_create:
    os.makedirs(dir_path, exist_ok=True)

# Function to copy files to destination
def copy_files(files, is_train):
    dest_type = 'train' if is_train else 'val'
    for image_file in files:
        # Get corresponding label file
        file_base = os.path.splitext(image_file)[0]
        label_file = f"{file_base}.txt"
        
        # Define source and destination paths
        img_src = os.path.join(source_dir, image_file)
        img_dest = os.path.join(target_dir, 'images', dest_type, image_file)
        
        label_src = os.path.join(source_dir, label_file)
        label_dest = os.path.join(target_dir, 'labels', dest_type, label_file)
        
        # Copy files if they exist
        if os.path.exists(img_src):
            shutil.copy2(img_src, img_dest)
        else:
            print(f"Warning: {img_src} does not exist")
        
        if os.path.exists(label_src):
            shutil.copy2(label_src, label_dest)
        else:
            print(f"Warning: {label_src} does not exist")

# Copy class file if it exists
class_file_src = os.path.join(source_dir, 'classes.txt')
if os.path.exists(class_file_src):
    class_file_dest = os.path.join(target_dir, 'classes.txt')
    shutil.copy2(class_file_src, class_file_dest)

# Copy files to train and val directories
copy_files(train_images, True)
copy_files(val_images, False)

print(f"Dataset distribution complete:")
print(f"- {len(train_images)} images in train set")
print(f"- {len(val_images)} images in validation set")
