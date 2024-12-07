import shutil
import os

def cleanup(clone_dir, ):
    """Remove the cloned repository and output file."""
    if os.path.exists(clone_dir):
        shutil.rmtree(clone_dir)

if __name__ == "__main__":
    clone_dir = "./working"
    cleanup(clone_dir, )
