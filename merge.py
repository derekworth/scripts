# adapted from Ben's response posted at:
# https://stackoverflow.com/questions/40895785/using-opencv-to-overlay-transparent-image-onto-another-image

import cv2
import numpy as np
import os
import sys
from tqdm import tqdm
    
# prereq's:
# -both images must be square with exactly 3 channels (BGR)
# -alpha is assumed to be a transparency mask of foreground image
# -alpha must have 3 channels (i.e., dimensions of [w, h, t]) where all 3 channels are duplicates
def merge_images(background, foreground, alpha):
    bg_h, bg_w, bg_channels = background.shape
    fg_h, fg_w, fg_channels = foreground.shape

    # enforce 3 color channels
    assert bg_channels == 3, f'background image should have exactly 3 channels (BGR). found:{bg_channels}'
    assert fg_channels == 3, f'foreground image should have exactly 3 channels (BGR). found:{fg_channels}'
    # ensure square images
    assert bg_w == bg_h, f'background image not square. dimensions:{bg_w}x{bg_h}'
    assert fg_w == fg_h, f'foreground image not square. dimensions:{fg_w}x{fg_h}'
    # ensure bg and fg are same dimensions
    assert bg_w == fg_w, 'background and foreground dimensions do not match.'
    assert bg_h == fg_h, 'background and foreground dimensions do not match.'
    
    # apply alpha transparency
    bg = background * (1 - alpha)
    fg = foreground * alpha
    
    # combine foreground/background
    composite = bg + fg
    # float64 -> unint8
    return composite.astype(np.uint8)

def get_file_number(filename):
    return int(filename.split('.')[0])

def show(name, img, wait_ms):
    cv2.imshow(name, img)
    cv2.waitKey(wait_ms)
    
def close_windows():
    cv2.destroyAllWindows()
    
def get_filenames_and_extensions(folder_path):
    # Check if the provided path is a valid directory
    if not os.path.isdir(folder_path):
        return "Invalid directory path"

    # Lists to store filenames and file extensions
    filenames = []
    extensions = []

    # Iterate through files in the directory
    for filename in os.listdir(folder_path):
        # Split the filename and extension
        name, extension = os.path.splitext(filename)
        
        # Add the filename and extension to their respective lists
        filenames.append(name)
        extensions.append(extension)

    return filenames, extensions

if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 5:
        script_file_name = os.path.basename(__file__)
        print(f"Usage: python3 {script_file_name} <bg_dir> <fg_dir> <alpha_path> <out_dir>")
        sys.exit(1)

    bg_folder = sys.argv[1]
    fg_folder = sys.argv[2]
    alpha_path = sys.argv[3]
    out_folder = sys.argv[4]
    
    # read alpha values (this will be our transparency channel)
    alpha = cv2.imread(alpha_path)

    # get filenames as lists of strings
    bg_fnames, bg_ext = get_filenames_and_extensions(bg_folder)
    fg_fnames, fg_ext = get_filenames_and_extensions(fg_folder)
    # sort strings numerically
    bg_fnames = sorted(bg_fnames, key=lambda x: int(os.path.splitext(x)[0]))
    fg_fnames = sorted(fg_fnames, key=lambda x: int(os.path.splitext(x)[0]))

    if len(set(bg_ext)) == 1 and len(set(fg_ext)) == 1 :
        bg_ext = bg_ext[0]
        fg_ext = fg_ext[0]
    else:
        print("Too many file types! Try reducing to one bg and one fg file extension.")
        sys.exit(1)
    
    # get number of image pairs
    count = min(len(bg_fnames), len(fg_fnames))
    
    # resize alpha dimensions to match first bg image (assuming it's square)
    tmp = cv2.imread(f'{bg_folder}/{bg_fnames[0]}{bg_ext}')
    s = tmp.shape[0]
    # resize and normalize between 0 and 1 (i.e., 0-255 -> 0.0-1.0)
    alpha = cv2.resize(alpha, (s, s)) / 255

    if not os.path.exists(out_folder):
        os.makedirs(out_folder)

    print(f"{count} image pair(s) found, merging...")

    for i in tqdm(range(0, count)):
        bg = cv2.imread(f'{bg_folder}/{bg_fnames[i]}{bg_ext}')
        fg = cv2.imread(f'{fg_folder}/{fg_fnames[i]}{fg_ext}')
        cv2.imwrite(f'{out_folder}/{i+1}.png', merge_images(bg, fg, alpha))
        
    print("done!")