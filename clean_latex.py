import os
import sys

def remove_files_with_extension(directory_path, target_extensions):
    try:
        cnt = 0
        # Iterate over all files in the directory
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)

            # Check if the file has one of the target extensions
            if os.path.isfile(file_path) and any(filename.lower().endswith(ext) for ext in target_extensions):
                os.remove(file_path)
                print(f"File removed: {file_path}")
                cnt += 1

        print(f"Removed {cnt} file(s).")
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 2:
        script_file_name = os.path.basename(__file__)
        print(f"Usage: python3 {script_file_name} <latex_dir>")
        sys.exit(1)

    directory_path = sys.argv[1]
    target_extensions = ['.aux', '.bbl', '.blg', '.log', '.out', '.gz']  # Specify the extensions to be removed

    remove_files_with_extension(directory_path, target_extensions)