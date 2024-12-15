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
from reduce_results import reduce_results

def main(repo_url):
    from config import WORKING_DIR, RESULTS_DIR, COMBINED_DIR
    
    output_file_name = "results.json"
    output_file = os.path.join(RESULTS_DIR, output_file_name)

    # Check if results already exist for this repo
    repo_name = repo_url.split('/')[-1]
    
    if os.path.exists(COMBINED_DIR):
        existing_files = [f for f in os.listdir(COMBINED_DIR) if f.startswith(repo_name)]
        if existing_files:
            logging.info(f"Results already exist for {repo_name}")
            return

    # Cleanup before starting
    try:
        cleanup(WORKING_DIR)
    except Exception as e:
        logging.error(f"Initial cleanup failed: {e}")
        sys.exit(1)

    try:
        # Clone the repository
        clone_repo(repo_url, WORKING_DIR)

        # Run semgrep and package scanning
        logging.info("Running scans...")
        run_semgrep(WORKING_DIR, output_file_name)
        logging.info("Running package scans...")
        package_scan(WORKING_DIR, RESULTS_DIR)
        
        # Combine results
        repo_name = repo_url.split('/')[-1]
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        combined_filename = f"{repo_name}_{timestamp}.json"
        logging.info("Combining results...")
        combine_results(RESULTS_DIR, combined_filename)
        
        # Reduce results
        logging.info("Reducing results...")
        combined_file_path = os.path.join(COMBINED_DIR, combined_filename)
        reduce_results(combined_file_path)

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        logging.error(str(e))
        sys.exit(1)
    finally:
        # Cleanup
        try:
            cleanup(WORKING_DIR)
        except Exception as e:
            logging.error(f"Cleanup failed: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        logging.error("Usage: python run_all.py <repo_url>")
        sys.exit(1)
    repo_url = sys.argv[1]
    main(repo_url)
