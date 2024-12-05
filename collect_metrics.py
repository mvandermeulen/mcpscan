import shutil
import os

def copy_metrics(output_file, destination_dir):
    """Copy the metrics to a specified location."""
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
    shutil.copy(output_file, destination_dir)

if __name__ == "__main__":
    output_file = "./working/results.json"
    destination_dir = "./working/metrics"
    copy_metrics(output_file, destination_dir)
