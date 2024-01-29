import os
import sys
import re
import shutil
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

def get_files_with_extension(directory, extension):
    file_list = []
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            file_list.append(filename)
    return file_list

def copy_file(src_path, dst_path):
    shutil.copy2(src_path, dst_path)
    #print(f"Copied file {src_path} to {dst_path}")
    return True

def copy_numbered_files(src_dir, dst_dir, file_ext, start_idx, end_idx, interval):
    # Ensure both source and destination directories exist
    if not os.path.exists(src_dir):
        print("Source directory does not exist.")
        return

    # Create destination directory if it doesn't already exist
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    # Get a list of files in the source directory
    files = get_files_with_extension(src_dir, file_ext)

    # Filter files based on a numeric part in the filename
    numbered_files = [f for f in files if any(char.isdigit() for char in f)]

    # Sort the file names based on the numerical part of their name
    numbered_files = sorted(numbered_files, key=lambda x: int(re.search(r'\d+', x).group()))

    with ThreadPoolExecutor() as executor:
        futures = []

        for i in range(start_idx, end_idx, interval):
            if i < len(numbered_files):
                src_path = os.path.join(src_dir, numbered_files[i])
                dst_path = os.path.join(dst_dir, numbered_files[i])
                futures.append(executor.submit(copy_file, src_path, dst_path))
            else:
                break

        files_copied = 0

        with tqdm(total=len(futures), desc="Copying files", unit="file") as pbar:
            for future in futures:
                if future.result():
                    files_copied += 1
                pbar.update(1)

    if files_copied == 0:
        print("No files copied.")
    else:
        print(f"Range copy completed. {files_copied} file(s) copied.")

if __name__ == "__main__":
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 7:
        script_file_name = os.path.basename(__file__)
        print(f"Usage: python3 {script_file_name} <src_dir> <dst_dir> <ext> <start_idx> <end_idx> <interval>")
        print("*NOTE: start index follows zero-based numbering and end index is exclusive")
        sys.exit(1)

    # grab arguments
    src_dir = sys.argv[1]
    dst_dir = sys.argv[2]
    file_ext = sys.argv[3]
    start_idx = int(sys.argv[4])
    end_idx = int(sys.argv[5])
    interval = int(sys.argv[6])

    # Call the function to sort and rename images
    copy_numbered_files(src_dir, dst_dir, file_ext, start_idx, end_idx, interval)
