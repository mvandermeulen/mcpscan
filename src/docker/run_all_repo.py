# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

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

    # Check if results already exist for this repo
    results_dir = "./results"
    combined_dir = os.path.join(results_dir, "combined")
    repo_name = repo_url.split('/')[-1]
    
    if os.path.exists(combined_dir):
        existing_files = [f for f in os.listdir(combined_dir) if f.startswith(repo_name)]
        if existing_files:
            logging.info(f"Results already exist for {repo_name}")
            return

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
        logging.info("Running scans...")
        run_semgrep(clone_dir, output_file_name)
        logging.info("Running package scans...")
        package_scan(clone_dir, results_dir)
        
        # Combine results
        repo_name = repo_url.split('/')[-1]
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        logging.info("Combining results...")
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
