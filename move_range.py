import os
import shutil
import argparse
from tqdm import tqdm

def move_files(src, dst, start_idx, end_idx, zero_padding):
    # Ensure destination directory exists
    if not os.path.exists(dst):
        os.makedirs(dst)
    
    # Move files within the specified range
    for idx in tqdm(range(start_idx, end_idx + 1)):
        filename = str(idx).zfill(zero_padding)
        src_file = os.path.join(src, f"{filename}.png")
        dst_file = os.path.join(dst, f"{filename}.png")
        
        if os.path.exists(src_file):
            shutil.move(src_file, dst_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Move PNG files from source to destination directory.')
    parser.add_argument('src', type=str, help='Source directory')
    parser.add_argument('dst', type=str, help='Destination directory')
    parser.add_argument('zero_padding', type=int, help='Pad filenames with this many zeros')
    parser.add_argument('start_idx', type=int, help='Starting index of files to move')
    parser.add_argument('end_idx', type=int, help='Ending index of files to move')

    args = parser.parse_args()
    print(f'Moving images {str(args.start_idx).zfill(args.zero_padding)}.png thru {str(args.end_idx).zfill(args.zero_padding)}.png from {args.src} to {args.dst}')
    move_files(args.src, args.dst, args.start_idx, args.end_idx, args.zero_padding)
