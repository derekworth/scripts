import sys
import os
import random
import shutil
from tqdm import tqdm

def copy_random_files(src_dir, dst_dir, cnt):
    src_img_path = os.path.join(src_dir, "images")
    src_lbl_path = os.path.join(src_dir, "labels")
    dst_img_path = os.path.join(dst_dir, "images")
    dst_lbl_path = os.path.join(dst_dir, "labels")

    # Get a list of all image files in the source directory
    img_files = os.listdir(src_img_path)
    
    # Randomly select m files from the list
    selected_images = random.sample(img_files, cnt)
    
    # Move selected file pairs (images w/labels) to the destination directory
    for img in tqdm(selected_images):
        filename,_ = os.path.splitext(img)

        src_img_file = os.path.join(src_img_path, img)
        src_lbl_file = os.path.join(src_lbl_path, filename + ".txt")

        dst_img_file = os.path.join(dst_img_path, img)
        dst_lbl_file = os.path.join(dst_lbl_path, filename + ".txt")

        if not os.path.exists(dst_img_path):
            os.mkdir(dst_img_path)
        if not os.path.exists(dst_lbl_path):
            os.mkdir(dst_lbl_path)
            
        shutil.copy(src_img_file, dst_img_file)
        shutil.copy(src_lbl_file, dst_lbl_file)

    print(f'{cnt} files randomly copied from {src_dir} to {dst_dir}')

if len(sys.argv) != 4:
    script_file_name = os.path.basename(__file__)
    print(f"Usage: python3 {script_file_name} <src_dir> <dst_dir> <cnt>")
    sys.exit(1)
    
src_dir = sys.argv[1]
dst_dir = sys.argv[2]
cnt = int(sys.argv[3])

copy_random_files(src_dir, dst_dir, cnt)
