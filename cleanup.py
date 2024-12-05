import shutil
import os

def cleanup(clone_dir, output_file):
    """Remove the cloned repository and output file."""
    if os.path.exists(clone_dir):
        shutil.rmtree(clone_dir)
    if os.path.exists(output_file):
        os.remove(output_file)

if __name__ == "__main__":
    clone_dir = "/path/to/clone/dir"  # Replace with actual clone directory
    output_file = "/path/to/output/results.json"  # Replace with actual output file path
    cleanup(clone_dir, output_file)
