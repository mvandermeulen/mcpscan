import subprocess
import os
import sys

def clone_repo(repo_url, clone_dir="./working"):
    """Clone a GitHub repository."""
    if not os.path.exists(clone_dir):
        os.makedirs(clone_dir)
    subprocess.run(["git", "clone", repo_url, clone_dir], check=True)

def get_latest_commit_hash(clone_dir="./working"):
    """Get the latest commit hash of the cloned repository."""
    result = subprocess.run(
        ["git", "-C", clone_dir, "rev-parse", "HEAD"],
        check=True,
        stdout=subprocess.PIPE,
        text=True
    )
    return result.stdout.strip()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python repo.py <repo_url>")
        sys.exit(1)
    repo_url = sys.argv[1]
    clone_repo(repo_url)
