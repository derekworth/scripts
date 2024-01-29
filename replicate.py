import shutil
import os
import sys
from tqdm import tqdm

def copy_file_multiple_times(src_path, dst_dir, num_copies):
    try:
        _, file_ext = os.path.splitext(src_path)
        for i in tqdm(range(1, num_copies + 1)):
            
            new_filename = f"{i}{file_ext}"
            dst_path = os.path.join(dst_dir, new_filename)
            shutil.copy2(src_path, dst_path)
    except FileNotFoundError:
        print(f"File not found: {src_path}")
    except Exception as e:
        print(f"Error occurred: {e}")

# Example usage:
if len(sys.argv) != 4:
    script_file_name = os.path.basename(__file__)
    print(f"Usage: python3 {script_file_name} <src_path> <dst_dir> <num_copies>")
    sys.exit(1)

src_path = sys.argv[1]
dst_dir = sys.argv[2]
num_copies = int(sys.argv[3])

copy_file_multiple_times(src_path, dst_dir, num_copies)
print("Done.")
