import shutil
import os

def cleanup(clone_dir, output_file):
    """Remove the cloned repository and output file."""
    if os.path.exists(clone_dir):
        shutil.rmtree(clone_dir)
    if os.path.exists(output_file):
        os.remove(output_file)

if __name__ == "__main__":
    clone_dir = "./working"
    output_file = "./results/results.json"
    cleanup(clone_dir, output_file)
