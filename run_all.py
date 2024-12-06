import sys
import os
from cleanup import cleanup
from clone_repo import clone_repo
from run_scan import run_semgrep

def main(repo_url):
    clone_dir = "./working"
    output_file_name = "results.json"
    output_file = os.path.join("./results", output_file_name)

    # Cleanup before starting
    try:
        cleanup(clone_dir, output_file)
    except Exception as e:
        print(f"Initial cleanup failed: {e}")
        sys.exit(1)
    # Clone the repository
    clone_repo(repo_url, clone_dir)

    # Run Semgrep scan
    run_semgrep(clone_dir, output_file_name)

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
    finally:
        # Cleanup
        try:
            cleanup(clone_dir, output_file)
        except Exception as e:
            print(f"Cleanup failed: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python run_all.py <repo_url>")
        sys.exit(1)
    repo_url = sys.argv[1]
    main(repo_url)
