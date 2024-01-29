#!/bin/bash

remove_last_slash() {
    local input_string="$1"
    # Check if the last character is a forward slash
    if [ "${input_string: -1}" == "/" ]; then
        # Remove the last character
        echo "${input_string:0:-1}"
    else
        # Return the original string if the last character is not a forward slash
        echo "$input_string"
    fi
}

get_after_last_slash() {
    local input_string="$1"
    # Extract characters after the last forward slash
    echo "${input_string##*/}"
}

#------------------------------------------------------------------------
# NOTES:
#
#   The input frame rate is equal to the total frame count divided 
#   by the output duration, where output duration is the total desired 
#   length of the video in seconds. Whereas, the output frame rate is 
#   simply the desired frame rate of the final video. A low output frame 
#   rate will results in a choppy video where you can "see" the actual 
#   frames. A high output frame rate will results in a smooth video 
#   where frame-to-frame transitions are hardly noticeable. Low output 
#   frame rates also result in a lot of dropped frames, while high 
#   output frame rates retain most of the original frames.
#
#------------------------------------------------------------------------

script_directory=$(dirname "$(readlink -f "$0")")
script_path="$0"
script_name=$(get_after_last_slash "$script_path")

# Check if the correct number of arguments is provided
if [ "$#" -ne 5 ]; then
    echo "Usage: ./$script_name <src_dir> <ext> <desired_dur_sec> <frate_out> <width:height>"
    exit 1
fi

folder_path="$1"
ext="$2"
desired_dur_sec="$3"
frate_out="$4"
img_size="$5"

# Check if the last character of folder path is a forward slash
folder_path=$(remove_last_slash "$folder_path")

img_cnt=$(ls -l "$folder_path" | grep "\\.$ext" | wc -l)
frate_in=$((img_cnt / desired_dur_sec))
folder_name="${folder_path##*/}"

python3 "$script_directory/renumber.py" "$folder_path" "$ext" 1

echo "============================================"
echo "Script directory: $script_directory"
echo "Image folder: $folder_name"
echo "Image count: $img_cnt"
echo "File extension: $ext"
echo "Desired duration (sec): $desired_dur_sec"
echo "Input frame rate: $frate_in"
echo "Output frame rate: $frate_out"
echo "Output dimensions: $img_size"
echo "============================================"

# Convert images to video
ffmpeg -r "$frate_in" -i "$folder_path/%d.png" -c:v libx264 -pix_fmt yuv420p -vf "scale=$img_size" -r "$frate_out" "$folder_path/../preview_$folder_name.mp4"