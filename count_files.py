import os
import sys
from tqdm import tqdm

def count_files_by_type(directory):
    file_types_count = {}
    for root, dirs, files in tqdm(os.walk(directory)):
        for file in files:
            file_extension = os.path.splitext(file)[1].lower()
            file_types_count[file_extension] = file_types_count.get(file_extension, 0) + 1
    return file_types_count

if __name__ == "__main__":
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 2:
        script_file_name = os.path.basename(__file__)
        print(f"Usage: python3 {script_file_name} <dir>")
        sys.exit(1)

    folder_path = sys.argv[1]
    file_types_count = count_files_by_type(folder_path)

    print("Number of files by type in directory and subdirectories:")
    for file_type, count in file_types_count.items():
        print(f"{file_type}: {count}")