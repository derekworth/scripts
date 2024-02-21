import os
import sys
import numpy as np
from PIL import Image
from tqdm import tqdm

def crop_to_aspect_ratio(image_path, aspect_ratio):
    # Open image using PIL
    image_pil = Image.open(image_path)
    
    # Calculate current aspect ratio
    width, height = image_pil.size
    current_aspect_ratio = width / height
    
    # Calculate target width and height based on aspect ratio
    if current_aspect_ratio > aspect_ratio:
        new_width = int(aspect_ratio * height)
        new_height = height
    else:
        new_width = width
        new_height = int(width / aspect_ratio)
    
    # Calculate coordinates for cropping
    left = (width - new_width) / 2
    top = (height - new_height) / 2
    right = (width + new_width) / 2
    bottom = (height + new_height) / 2
    
    # Crop the image
    cropped_image = image_pil.crop((left, top, right, bottom))
    
    return cropped_image

def crop_images_in_directory(directory, aspect_ratio):
    # Get a list of all files in the directory
    file_list = os.listdir(directory)
    
    # Filter the list to include only image files
    image_files = [file for file in file_list if file.lower().endswith(('.png', '.jpg', '.jpeg', '.jfif'))]
    
    # Loop through each image file
    for image_file in tqdm(image_files):
        # Construct the full path to the image file
        image_path = os.path.join(directory, image_file)
        
        # Crop the image to the specified aspect ratio
        cropped_image = crop_to_aspect_ratio(image_path, aspect_ratio)
        
        # Save the cropped image, overwrite the original file
        cropped_image.save(image_path)

if len(sys.argv) != 3:
    script_file_name = os.path.basename(__file__)
    print(f"Usage: python3 {script_file_name} <src_dir> <aspect_ratio>")
    sys.exit(1)

src_dir = sys.argv[1]
aspect_ratio = float(sys.argv[2])
crop_images_in_directory(src_dir, aspect_ratio)