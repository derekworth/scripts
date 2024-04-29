import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def make_violin_plot(file_path, std_threshold, plot_title):
    # Step 1: Read the CSV file into a pandas DataFrame
    data = pd.read_csv(file_path)

    # Step 2: Convert non-float values to NaN and drop rows containing NaN values
    data = data.apply(pd.to_numeric, errors='coerce').dropna()

    # Step 3: Remove values greater than 6 standard deviations from the mean for each column
    for column in data.columns:
        mean = data[column].mean()
        std_dev = data[column].std()
        upper_limit = mean + std_threshold * std_dev
        data = data[data[column] <= upper_limit]

    # Step 4: Plot the data as violin plots using matplotlib
    plt.figure(figsize=(10, 6))  # Adjust the figure size as needed

    # Extract column headers from the DataFrame
    data_columns = data.columns.tolist()

    # Create violin plots for each column
    violin_parts = plt.violinplot(data.values, showmeans=True, widths=0.7, showextrema=False)
    for partname in ('cmeans',):
        violin_parts[partname].set_color('red')  # Set color of mean line
        violin_parts[partname].set_linewidth(1.0)  # Decrease line thickness

    # Add title and labels
    plt.title(plot_title)
    plt.xlabel('Composition')
    plt.ylabel('PtD magnitude error (m)')

    box_parts = plt.boxplot(data.values, positions=np.arange(1, len(data_columns) + 1), patch_artist=True, widths=0.15)
    
    plt.setp(box_parts['medians'], color='blue')  # Set boxplot element color
        
    # Customize boxplot colors
    for patch in box_parts['boxes']:
        patch.set_facecolor('white')  # Change boxplot color to white

    # Add x-axis tick labels
    plt.xticks(range(1, len(data_columns) + 1), data_columns)

    # Manually create legend lines to match plot lines
    median_line = plt.Line2D([], [], color='blue', marker='_', markersize=5, label='Median')
    mean_line = plt.Line2D([], [], color='red', marker='_', markersize=10, label='Mean')

    # Add legend
    plt.legend(handles=[median_line, mean_line], loc='upper right')

    # Show plot
    plt.grid(True)
    plt.tight_layout()
    plt.subplots_adjust(left=0.25, right=0.75, bottom=0.25, top=0.75)  # Adjust the left and right margins
    plt.savefig(file_path+".pdf", bbox_inches='tight')

if __name__ == "__main__":
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 4:
        script_file_name = os.path.basename(__file__)
        print(f"Usage: python3 {script_file_name} <file_path> <std_threshold> <plot_title>")
        sys.exit(1)

    # grab arguments
    file_path = sys.argv[1]
    std_threshold = float(sys.argv[2])
    plot_title = sys.argv[3]

    make_violin_plot(file_path, std_threshold, plot_title)
