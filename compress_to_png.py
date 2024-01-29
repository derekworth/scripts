import os
import sys
import re
from PIL import Image
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import math

def get_files_with_extension(directory, extension):
    file_list = []
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            file_list.append(filename)
    return file_list

def convert_image(input_path, output_dir, dimensions, remove_old):
    try:
        # Open the image
        with Image.open(input_path) as img:
            # Resize the image
            img_resized = img.resize(dimensions)
            
            # Save the resized image as PNG
            output_filename = os.path.splitext(os.path.basename(input_path))[0] + ".png"
            output_path = os.path.join(output_dir, output_filename)
            img_resized.save(output_path, "PNG")

            if remove_old and input_path != output_path:
                    os.remove(input_path)
                    print(f"Removed: {input_path}")
            
            return True
    except Exception as e:
        print(f"Error processing {input_path}: {e}")
        return False

def process_images(src_dir, dst_dir, ext, dimensions, remove_old, start_idx, end_idx, interval):
    # Ensure both source and destination directories exist
    if not os.path.exists(src_dir):
        print("Source directory does not exist.")
        return

    # Create destination directory if it doesn't already exist
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    # Get a list of files in the source directory
    files = get_files_with_extension(src_dir, ext)

    # Filter files based on a numeric part in the filename
    numbered_files = [f for f in files if any(char.isdigit() for char in f)]

    # Sort the file names based on the numerical part of their name
    numbered_files = sorted(numbered_files, key=lambda x: int(re.search(r'\d+', x).group()))

    with ThreadPoolExecutor() as executor:
        futures = []

        for i in range(start_idx, end_idx, interval):
            if i < len(numbered_files):
                src_path = os.path.join(src_dir, numbered_files[i])
                futures.append(executor.submit(convert_image, src_path, dst_dir, dimensions, remove_old))
            else:
                break

        converted_count = 0

        with tqdm(total=len(futures), desc="Compressing images", unit="image") as pbar:
            for future in futures:
                if future.result():
                    converted_count += 1
                pbar.update(1)

    if converted_count == 0:
        print("No valid images found.")
    else:
        print(f"Compression completed. {converted_count} image(s) compressed.")

def main():
    if len(sys.argv) < 5 or len(sys.argv) > 8:
        script_file_name = os.path.basename(__file__)
        print(f"Usage: python3 {script_file_name} <src_dir> <dest_dir> <ext> <width>x<height> [<start_idx>, <end_idx>, <interval>]")
        sys.exit(1)

    input_directory = sys.argv[1]
    output_directory = sys.argv[2]
    ext = sys.argv[3]
    dimensions = tuple(map(int, sys.argv[4].split('x')))
    start_idx = 0
    files = get_files_with_extension(input_directory, ext)
    end_idx = len(files)
    interval = 1

    # update (if specified)
    if len(sys.argv) > 5:
        start_idx = int(sys.argv[5])
    if len(sys.argv) > 6:
        end_idx = int(sys.argv[6])
    if len(sys.argv) > 7:
        interval = int(sys.argv[7])

    print("=============================")
    print(f"Input directory: {input_directory}")
    print(f"Output directory: {output_directory}")
    print(f"File extension: {ext}")
    print(f"Resized dimensions: {dimensions}")
    print(f"Range: [{start_idx}, {end_idx}]")
    print(f"Interval: {interval} ({math.floor((end_idx-start_idx)/interval)} images)")
    print("=============================")

    user_input = input("Are you sure you want to continue? (Y/n): ")
    if user_input != 'Y':
        print("Script aborted.")
        sys.exit(1)

    remove_old = False
    user_input = input("Do you want to remove original files after conversion? (Y/n): ")
    if user_input == 'Y':
        remove_old = True
        print("COMPRESSING, THEN REMOVING ORIGINALS...")
    else:
        print("Okay, compressing without removing original images.")

    process_images(input_directory, output_directory, ext, dimensions, remove_old, start_idx, end_idx, interval)

if __name__ == "__main__":
    main()
