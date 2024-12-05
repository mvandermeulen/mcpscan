import shutil
import os

def copy_metrics(output_file, destination_dir):
    """Copy the metrics to a specified location."""
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
    shutil.copy(output_file, destination_dir)

if __name__ == "__main__":
    output_file = "/path/to/output/results.json"  # Replace with actual output file path
    destination_dir = "/path/to/destination/dir"  # Replace with desired destination directory
    copy_metrics(output_file, destination_dir)
