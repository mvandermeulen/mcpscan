import subprocess
import sys
import os

def main(repo_url):
    clone_dir = "./working"
    output_file = "./results.json"
    destination_dir = "./metrics"

    try:
        # Clone the repository
        subprocess.run(["python", "clone_repo.py", repo_url], check=True)

        # Run Semgrep scan
        subprocess.run(["python", "run_scan.py", clone_dir, output_file], check=True)

        # Collect metrics
        subprocess.run(["python", "collect_metrics.py", output_file, destination_dir], check=True)

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
    finally:
        # Cleanup
        try:
            subprocess.run(["python", "cleanup.py", clone_dir, output_file], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Cleanup failed: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python run_all.py <repo_url>")
        sys.exit(1)
    repo_url = sys.argv[1]
    main(repo_url)
