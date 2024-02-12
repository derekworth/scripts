import os
import sys

def append_line(source_file, destination_file, line_number):
    try:
        with open(source_file, 'r') as src:
            lines = src.readlines()
            if 0 < line_number <= len(lines):
                line_to_append = lines[line_number - 1]
            else:
                print("Invalid line number.")
                return

        with open(destination_file, 'a') as dest:
            dest.write("\n")
            dest.write(line_to_append)

        print(f"Line {line_number} from {source_file} appended to {destination_file} successfully.")

    except FileNotFoundError:
        print("One of the files does not exist.")

if len(sys.argv) != 4:
    script_file_name = os.path.basename(__file__)
    print(f"Usage: python3 {script_file_name} <src_path> <dest_path> <line_num>")
    sys.exit(1)

src_path = sys.argv[1]
dest_path = sys.argv[2]
line_num = int(sys.argv[3])

append_line(src_path, dest_path, line_num)