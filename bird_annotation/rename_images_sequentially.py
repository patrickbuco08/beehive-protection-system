# usage: python rename_images_sequentially.py --start 0 --folder to-label

import os
import argparse

# Parse command line arguments
def parse_args():
    parser = argparse.ArgumentParser(description='Rename images sequentially with a custom starting index')
    parser.add_argument('--start', type=int, default=0, help='Starting index for renaming (default: 0)')
    parser.add_argument('--folder', type=str, default='to-label', help='Folder name within the script directory (default: to-label)')
    return parser.parse_args()

def main():
    args = parse_args()
    start_index = args.start
    folder_name = args.folder
    
    # Get the folder path
    folder = os.path.join(os.path.dirname(__file__), folder_name)
    
    # Ensure folder exists
    if not os.path.exists(folder):
        print(f"Error: Folder '{folder}' does not exist.")
        return
    
    # Get all jpg images and sort them
    images = [f for f in os.listdir(folder) if f.lower().endswith('.jpg')]
    images.sort()  # Sort to ensure consistent ordering
    
    # Rename images
    for i, filename in enumerate(images):
        src = os.path.join(folder, filename)
        dst = os.path.join(folder, f"{i + start_index}.jpg")
        os.rename(src, dst)
    
    print(f"Renamed {len(images)} images to {start_index}.jpg, {start_index+1}.jpg, ... in '{folder}'")

if __name__ == "__main__":
    main()
