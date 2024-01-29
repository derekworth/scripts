import os
import sys
import re
import shutil
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import numpy as np

def get_filenames_with_extension(directory_path):
    names = []
    
    # Iterate over all files in the directory
    ext = None
    print(f"Loading file names from {directory_path}")
    for filename in tqdm(os.listdir(directory_path)):
        if os.path.isfile(os.path.join(directory_path, filename)):
            # Split the filename and extension
            name, extension = os.path.splitext(filename)
            
            if ext == None:
                ext = extension
            elif ext != extension:
                print(f"Error: more than one file extension present in '{directory_path}'")
                return None, None
            
            # Add the filename to the corresponding extension in the dictionary
            names.append(name)

    return names, ext

def make_dir_if_not_exist(path):
    if not os.path.exists(path):
        os.makedirs(path)

def train_valid_split(src_dir, dst_dir, valid_perc):
    # check src_dir
    if not os.path.exists(src_dir):
        print("Source directory not found.")
        sys.exit(1)
    # make sure src_dir has images/labels
    images_path = os.path.join(src_dir, "images")
    labels_path = os.path.join(src_dir, "labels")
    if not os.path.exists(images_path) or not os.path.exists(labels_path):
        print(f"Error: check images/labels folders exist in '{src_dir}'")
        sys.exit(1)
    # check dst_dir
    make_dir_if_not_exist(dst_dir)
    # make sure dst_dir has train/valid folders, each with images/labels folders
    train_path = os.path.join(dst_dir, "train")
    valid_path = os.path.join(dst_dir, "valid")
    trn_img_path = os.path.join(train_path, "images")
    trn_lbl_path = os.path.join(train_path, "labels")
    val_img_path = os.path.join(valid_path, "images")
    val_lbl_path = os.path.join(valid_path, "labels")
    make_dir_if_not_exist(train_path)
    make_dir_if_not_exist(valid_path)
    make_dir_if_not_exist(trn_img_path)
    make_dir_if_not_exist(trn_lbl_path)
    make_dir_if_not_exist(val_img_path)
    make_dir_if_not_exist(val_lbl_path)

    # get image filenames
    img_names, img_ext = get_filenames_with_extension(images_path)
    lbl_names, lbl_ext = get_filenames_with_extension(labels_path)

    if img_ext == None or lbl_ext == None:
        sys.exit(1)

    if len(img_names) != len(lbl_names):
        print("Error: label/image count mismatch")
        sys.exit(1)

    if lbl_ext != ".txt":
        print("Error: labels not stored in .txt files")
        sys.exit(1)

    print("Checking images and labels match...")
    for iname in tqdm(img_names):
        path = os.path.join(labels_path, iname + lbl_ext)
        if not os.path.exists(path):
            print(f"Error: label missing for {iname}{img_ext}")
            sys.exit(1)

    curr_idx = 0
    stop_idx = int(len(img_names) * valid_perc)
    print(f'Randomly copying {stop_idx} images to training set and {len(img_names) - stop_idx} to validation set.')
    for i in tqdm(range(len(img_names))):
        rand_idx = int(np.random.uniform() * (len(img_names)-1))
        name = img_names[rand_idx]
        img_names.remove(name)
        curr_idx += 1
        if curr_idx <= stop_idx:
            shutil.copy(os.path.join(images_path, name + img_ext), os.path.join(trn_img_path, name + img_ext))
            shutil.copy(os.path.join(labels_path, name + lbl_ext), os.path.join(trn_lbl_path, name + lbl_ext))
        else:
            shutil.copy(os.path.join(images_path, name + img_ext), os.path.join(val_img_path, name + img_ext))
            shutil.copy(os.path.join(labels_path, name + lbl_ext), os.path.join(val_lbl_path, name + lbl_ext))
    print("Done.")

if __name__ == "__main__":
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 4:
        script_file_name = os.path.basename(__file__)
        print(f"Usage: python3 {script_file_name} <src_dir> <dst_dir> <valid_perc>")
        sys.exit(1)

    # grab arguments
    src_dir = sys.argv[1]
    dst_dir = sys.argv[2]
    valid_perc = float(sys.argv[3])

    train_valid_split(src_dir, dst_dir, valid_perc)
