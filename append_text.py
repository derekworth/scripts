import os
import sys
from tqdm import tqdm

def append_text_to_files(source_file_path, target_directory):
    try:
        # Read text from the source file
        with open(source_file_path, 'r') as source_file:
            appended_text = source_file.read()

        # Iterate through all text files in the target directory
        for filename in tqdm(os.listdir(target_directory)):
            if filename.endswith(".txt"):
                target_file_path = os.path.join(target_directory, filename)

                # Append text to each target file
                with open(target_file_path, 'a') as target_file:
                    target_file.write('\n')  # Add a new line before appending
                    target_file.write(appended_text)

    except FileNotFoundError:
        print(f"File not found: {source_file_path}")
    except IsADirectoryError:
        print(f"Specified target is a directory, not a file: {target_directory}")
    except Exception as e:
        print(f"Error occurred: {e}")

if len(sys.argv) != 3:
    script_file_name = os.path.basename(__file__)
    print(f"Usage: python3 {script_file_name} <src_path> <target_dir>")
    sys.exit(1)

src_path = sys.argv[1]
target_dir = sys.argv[2]

append_text_to_files(src_path, target_dir)
