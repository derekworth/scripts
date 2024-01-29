import os
import re
import sys
from tqdm import tqdm

def create_empty_text_file(file_path):
    try:
        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:
                pass  # Empty block, as we just want to create an empty file
    except Exception as e:
        print(f"Error occurred: {e}")
    
def generate_yolov5_yaml(prb_cnt, drg_cnt, yaml_path):
    # create if not already exists
    create_empty_text_file(yaml_path)

    content = 'a' * prb_cnt + 'b' * drg_cnt

    content = "train: ../train/images\n"
    content += "val: ../valid/images\n\n"
    content += f"nc: {prb_cnt + drg_cnt}\n"

    names = []
    for i in range(prb_cnt):
        names.append(f'p{i}')
    
    for i in range(drg_cnt):
        names.append(f'd{i}')

    content += f"names: {names}"

    with open(yaml_path, 'w') as file:
        file.write(content)

if __name__ == "__main__":
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 4:
        script_file_name = os.path.basename(__file__)
        print(f"Usage: python3 {script_file_name} <yaml_path> <prb_cnt> <drg_cnt>")
        sys.exit(1)

    yaml_path = sys.argv[1]
    prb_cnt = int(sys.argv[2])
    drg_cnt = int(sys.argv[3])

    generate_yolov5_yaml(prb_cnt, drg_cnt, yaml_path)
    print("Done.")