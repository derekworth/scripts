import sys
import os
import random
import shutil
from tqdm import tqdm

def move_random_files(src_dir, dst_dir, cnt):
    # Get a list of all files in the source directory
    files = os.listdir(src_dir)
    
    # Randomly select m files from the list
    selected_files = random.sample(files, cnt)
    
    # Move selected files to the destination directory
    for file in tqdm(selected_files):
        source_path = os.path.join(src_dir, file)
        dest_path = os.path.join(dst_dir, file)
        if not os.path.exists(dst_dir):
            os.mkdir(dst_dir)
        shutil.move(source_path, dest_path)
    print(f'{cnt} files randomly moved from {src_dir} to {dst_dir}')

if len(sys.argv) != 4:
    script_file_name = os.path.basename(__file__)
    print(f"Usage: python3 {script_file_name} <src_dir> <dst_dir> <cnt>")
    sys.exit(1)
    
src_dir = sys.argv[1]
dst_dir = sys.argv[2]
cnt = int(sys.argv[3])

move_random_files(src_dir, dst_dir, cnt)
