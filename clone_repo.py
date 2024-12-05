import subprocess
import os
import sys

def clone_repo(repo_url, clone_dir="./working"):
    """Clone a GitHub repository."""
    if not os.path.exists(clone_dir):
        os.makedirs(clone_dir)
    subprocess.run(["git", "clone", repo_url, clone_dir], check=True)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python clone_repo.py <repo_url>")
        sys.exit(1)
    repo_url = sys.argv[1]
    clone_repo(repo_url)
