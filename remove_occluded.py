import os
import sys
import re
import shutil
from tqdm import tqdm
from shapely.geometry import Polygon, Point

def remove_non_numeric_chars(input_string):
    # Define a regular expression pattern to match characters that are not numbers, periods, or commas
    pattern = re.compile('[^0-9.,]')
    
    # Use the sub() method to replace matched characters with an empty string
    result_string = pattern.sub('', input_string)
    
    return result_string

def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            return lines
    except FileNotFoundError:
        return f"File not found: {file_path}"

def is_point_inside_polygon(polygon, point):

    # Create a Shapely point from the provided coordinates
    point = Point(point)

    # Check if the point is inside the polygon
    return polygon.contains(point)

if len(sys.argv) != 5:
    script_file_name = os.path.basename(__file__)
    print(f"Usage: python3 {script_file_name} <label_dir> <polygon_path> <min_visible> <occlusion_max>")
    print("Note: image files must be png format.")
    print("Hint: specify points in range between [0.0,1.0], for example poly.txt could contain:")
    print(" 0.1046,1.0000")
    print(" 0.1798,0.9120")
    print(" 0.1742,0.8328")
    print(" 1.0000,0.8270")
    print(" 1.0000,1.0000")
    print("Also, occlusion_max is a percentage between [0.0,1.0]")

    sys.exit(1)

label_dir = sys.argv[1]
polygon_path = sys.argv[2]
min_visible = int(sys.argv[3])
occlusion_max = float(sys.argv[4])

if occlusion_max > 1.0 or occlusion_max < 0.0:
    print(f"Please specify an occlusion threadhold in the range of: [0.0, 1.0]")
    sys.exit(1)

lines_list = read_file(polygon_path)

if isinstance(lines_list, list):
    poly_verts = [] # start with empty list
    for line in lines_list:
        line = remove_non_numeric_chars(line)
        line = line.split(",")
        if len(line) == 2:
            poly_verts.append((float(line[0]), float(line[1])))

if len(poly_verts) < 3:
    print(f'Not enough polygon verticies. {len(poly_verts)} specified.')
    sys.exit(1)
    
# Create a Shapely polygon from the provided vertices
polygon = Polygon(poly_verts)

# Get a list of image files in the specified folder
label_files = [f for f in os.listdir(label_dir) if f.lower().endswith(".txt")]

for index, filename in enumerate(tqdm(label_files)):
    filepath = os.path.join(label_dir, filename)
    lines_list = read_file(filepath)
    if isinstance(lines_list, list):
        num_occluded = 0
        num_visible = 0
        for line in lines_list:
            tokens = line.split()
            if len(tokens) == 5:
                u = float(tokens[1])
                v = float(tokens[2])
                test_point = (u, v)
                if is_point_inside_polygon(polygon, test_point):
                    num_occluded += 1
                else:
                    num_visible += 1

        if num_visible < min_visible or (num_occluded / (num_occluded + num_visible)) >= occlusion_max:
            #remove both image and label
            image_dir = os.path.join(label_dir, "../images")
            name, ext = filename.split(".")
            rm_label_path = os.path.join(label_dir, filename)
            rm_image_path = os.path.join(image_dir, name + ".png")
            removed_path = os.path.join(label_dir, "../removed")
            removed_label_path = os.path.join(removed_path,"labels")
            removed_image_path = os.path.join(removed_path,"images")
            if not os.path.exists(removed_path):
                os.makedirs(removed_path)
            if not os.path.exists(removed_label_path):
                os.makedirs(removed_label_path)
            if not os.path.exists(removed_image_path):
                os.makedirs(removed_image_path)
            shutil.move(rm_label_path, os.path.join(removed_label_path, filename))
            shutil.move(rm_image_path, os.path.join(removed_image_path, name + ".png"))