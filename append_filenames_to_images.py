import cv2
import os
import sys
from tqdm import tqdm

def append_filename_to_image(input_image_path, output_image_path=None):
    # Read the image using OpenCV
    image = cv2.imread(input_image_path)

    # Get the filename without extension
    filename = os.path.splitext(os.path.basename(input_image_path))[0]

    # Choose a font (you may need to adjust the font size based on your image size)
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_thickness = 2

    # Set the position where you want to write the filename
    position = (10, 50)

    # Set the text color to white
    text_color = (255, 255, 255)

    # Set the background color to black
    bg_color = (0, 0, 0)

    # Get text size to determine the background rectangle size
    text_size = cv2.getTextSize(filename, font, font_scale, font_thickness)[0]

    # Create a black background rectangle
    cv2.rectangle(image, position, (position[0] + text_size[0], position[1] - text_size[1]), bg_color, -1)

    # Write the filename on the image
    cv2.putText(image, filename, position, font, font_scale, text_color, font_thickness)

    # Save the modified image
    if output_image_path:
        cv2.imwrite(output_image_path, image)
    else:
        # If no output path is provided, overwrite the input image
        cv2.imwrite(input_image_path, image)

    # Release the image
    cv2.destroyAllWindows()

def process_images_in_directory(input_directory, output_directory=None):

    if output_directory:
        # Ensure output directory exists (if specified)
        os.makedirs(output_directory, exist_ok=True)

    # Iterate through all files in the input directory
    for filename in tqdm(os.listdir(input_directory)):
        if filename.endswith(('.jpg', '.jpeg', '.png')):  # Add more extensions if needed
            input_path = os.path.join(input_directory, filename)
            if output_directory:
                append_filename_to_image(input_path, os.path.join(output_directory, filename))
            else:
                append_filename_to_image(input_path)

if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 2 and len(sys.argv) != 3:
        script_file_name = os.path.basename(__file__)
        print(f"Usage: python3 {script_file_name} <src_dir> [<dst_dir>]")
        sys.exit(1)

    # Get source and destination directories from command-line arguments
    source_directory = sys.argv[1]
    if len(sys.argv) == 3:
        destination_directory = sys.argv[2]
        print(f"Appending filename to images (top left corner) and saving to: '{destination_directory}'")
        process_images_in_directory(source_directory, destination_directory)
    else:
        print("Appending filename to original images (top left corner).")
        process_images_in_directory(source_directory)

    print("Done.")