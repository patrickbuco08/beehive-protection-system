"""
Distribute images and labels from a YOLO-format dataset batch into
bird-dataset/images/train, images/val, labels/train, labels/val folders.
Supports both .jpg and .png images.

Usage:
    python distribute_dataset.py --folder <source_folder>

Arguments:
    --folder   (required) Path to the folder containing the batch to distribute (relative to this script or absolute)

Example:
    python distribute_dataset.py --folder dataset_label_first_batch
"""
import os
import shutil
import random
import argparse

random.seed(42)

def parse_args():
    parser = argparse.ArgumentParser(description="Distribute YOLO-format images and labels into train/val folders.")
    parser.add_argument('--folder', type=str, required=True, help='Source folder containing images and labels to distribute')
    return parser.parse_args()

def main():
    args = parse_args()
    source_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), args.folder))
    target_dir = os.path.join(os.path.dirname(__file__), 'bird-dataset')

    # Define train/val split ratio
    train_ratio = 0.8

    # Get all image files (.jpg and .png)
    image_files = [f for f in os.listdir(source_dir) if f.lower().endswith('.jpg') or f.lower().endswith('.png')]
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

if __name__ == "__main__":
    main()