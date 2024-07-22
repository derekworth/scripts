import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

def make_histogram(file_path, bin_cnt, threshold=None, upper_limit=None):

    # Read the CSV file into a pandas DataFrame
    data = pd.read_csv(file_path, header=None)

    # Apply upper limit if provided
    #if upper_limit is not None:
    #    data = data.apply(lambda x: x.clip(upper=upper_limit))

    # Plot the histogram
    if upper_limit is not None:
        plt.hist(data.iloc[:,0], bins=bin_cnt, range=(0, upper_limit), color='tab:blue', edgecolor='black', linewidth=0.1)
    else:
        plt.hist(data.iloc[:,0], bins=bin_cnt, color='tab:blue', edgecolor='black', linewidth=0.1)

    # Add vertical line for threshold if provided
    if threshold is not None:
        plt.axvline(x=threshold, color='red', linestyle='--', linewidth=0.25)

        # Shade region to the left of the threshold line in green
        plt.axvspan(0, threshold, color='green', alpha=0.1)

        # Shade region to the right of the threshold line in red
        plt.axvspan(threshold, upper_limit, color='red', alpha=0.1)

        # Add text label
        plt.text(threshold + 0.002, plt.gca().get_ylim()[1], '7 cm                       ', rotation=90, verticalalignment='top')

        error_rt_of_line = plt.Line2D([], [], color='red', linewidth=8.0, label='Unacceptable', alpha=0.1)
        error_lt_of_line = plt.Line2D([], [], color='green', linewidth=8.0, label='Acceptable', alpha=0.1)
        # Add legend
        plt.legend(handles=[error_rt_of_line, error_lt_of_line], loc='upper right', handlelength=2.0)

    plt.xlabel('Magnitude error (m)')
    plt.ylabel('Frequency')
    plt.title('Histogram of PtD Prediction Error')
    plt.grid(False)
    plt.tight_layout()
    plt.subplots_adjust(left=0.2, right=0.8, bottom=0.25, top=0.75)  # Adjust the left and right margins
    plt.savefig(file_path+".pdf", bbox_inches='tight')
    plt.clf()  # Clear the current figure to avoid plots overlapping

if __name__ == "__main__":
    # Check if the correct number of arguments is provided
    if len(sys.argv) not in (3, 4, 5):
        script_file_name = os.path.basename(__file__)
        print(f"Usage: python3 {script_file_name} <file_path> <bin_cnt> [threshold] [upper_limit]")
        sys.exit(1)

    # grab arguments
    file_path = sys.argv[1]
    bin_cnt = int(sys.argv[2])
    threshold = float(sys.argv[3]) if len(sys.argv) >= 4 else None
    upper_limit = float(sys.argv[4]) if len(sys.argv) == 5 else None

    make_histogram(file_path, bin_cnt, threshold, upper_limit)
