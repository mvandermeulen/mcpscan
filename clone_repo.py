import subprocess
import os

def clone_repo(repo_url, clone_dir):
    """Clone a GitHub repository."""
    if not os.path.exists(clone_dir):
        os.makedirs(clone_dir)
    subprocess.run(["git", "clone", repo_url, clone_dir], check=True)

if __name__ == "__main__":
    repo_url = "https://github.com/user/repo.git"  # Replace with actual repo URL
    clone_dir = "/path/to/clone/dir"  # Replace with desired clone directory
    clone_repo(repo_url, clone_dir)
