"""
Generate empty .txt files for every .png and .jpg image in the specified folder.

Usage:
    python generate_empty_labels.py --folder <target_folder>

Arguments:
    --folder   (required) Path to the folder containing .png/.jpg files (relative or absolute)

Example:
    python generate_empty_labels.py --folder no_bird_first_batch
"""
import os
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Generate empty .txt files for every .png image in the given folder.')
    parser.add_argument('--folder', type=str, required=True, help='Target folder containing .png files')
    return parser.parse_args()

def main():
    args = parse_args()
    folder = os.path.abspath(os.path.join(os.path.dirname(__file__), args.folder))
    if not os.path.exists(folder):
        print(f"Error: Folder '{folder}' does not exist.")
        return
    count = 0
    for fname in os.listdir(folder):
        if fname.lower().endswith('.png') or fname.lower().endswith('.jpg'):
            base = os.path.splitext(fname)[0]
            txt_path = os.path.join(folder, base + '.txt')
            if not os.path.exists(txt_path):
                open(txt_path, 'w').close()
                count += 1
    print(f'Generated {count} empty .txt files for all PNG and JPG images in {folder}.')

if __name__ == "__main__":
    main()
