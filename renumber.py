import os
import re
import sys
from tqdm import tqdm
    
def sort_and_rename_files(folder_path, file_ext, start_index):
    # Get a list of image files in the specified folder
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(file_ext)]

    # Sort the image files based on the numerical part of their name
    sorted_images = sorted(image_files, key=lambda x: int(re.search(r'\d+', x).group()))

    print("Renaming files... please wait.")

    # Rename and move the images
    for index, image_name in enumerate(tqdm(sorted_images), start=start_index):
        old_path = os.path.join(folder_path, image_name)
        new_name = f"{index}.{file_ext}_" #add underscore at the end so it's impossible to overwrite an existing image
        new_path = os.path.join(folder_path, new_name)
        #print(f'\r{image_name} -> {new_name}')

        os.rename(old_path, new_path)

    # Get updated list of image files in the specified folder (ending with underscore)
    sorted_images = [f for f in os.listdir(folder_path) if f.lower().endswith(file_ext + "_")]

    # let's keep track of how many filenames were changed
    names_changed = 0

    print("Removing underscores...")

    # Remove underscore from end of names
    for index, image_name in enumerate(tqdm(sorted_images), start=start_index):
        old_path = os.path.join(folder_path, image_name)
        new_name = image_name[:-1] #remove underscore
        new_path = os.path.join(folder_path, new_name)

        os.rename(old_path, new_path)
        names_changed += 1

    print(f'Done! {names_changed} file name(s) changed.')

if __name__ == "__main__":
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 4:
        script_file_name = os.path.basename(__file__)
        print(f"Usage: python3 {script_file_name} <dir> <ext> <start_idx>")
        sys.exit(1)

    folder_path = sys.argv[1]

    # Check if the provided path is a valid directory
    if not os.path.isdir(folder_path):
        print(f"Error: {folder_path} is not a valid directory.")
        sys.exit(1)

    # Get file extension from the second argument
    file_ext = sys.argv[2]

    # Get the start index from the third argument
    start_index = int(sys.argv[3])

    # Call the function to sort and rename images
    sort_and_rename_files(folder_path, file_ext, start_index)
