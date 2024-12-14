import sys
import os
import datetime
import logging
from log_config import setup_logging

setup_logging()
from cleanup import cleanup
from repo import clone_repo
from run_scan import run_semgrep
from combine_results import combine_results
from package_scan import scan as package_scan

def main(repo_url):
    clone_dir = "./working"
    results_dir = "./results"
    output_file_name = "results.json"
    output_file = os.path.join(results_dir, output_file_name)

    # Cleanup before starting
    try:
        cleanup(clone_dir)

    except Exception as e:
        logging.error(f"Initial cleanup failed: {e}")
        sys.exit(1)
    try:
        # Clone the repository
        clone_repo(repo_url, clone_dir)

        # Run semgrep and package scanning
        run_semgrep(clone_dir, output_file_name)
        package_scan(clone_dir, results_dir)
        
        # Combine results
        repo_name = repo_url.split('/')[-1]
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        combine_results(results_dir, f"{repo_name}_{timestamp}.json")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        logging.error(str(e))
        sys.exit(1)
    finally:
        # Cleanup
        try:
            cleanup(clone_dir)
        except Exception as e:
            logging.error(f"Cleanup failed: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        logging.error("Usage: python run_all.py <repo_url>")
        sys.exit(1)
    repo_url = sys.argv[1]
    main(repo_url)
