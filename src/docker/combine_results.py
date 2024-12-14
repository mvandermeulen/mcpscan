# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import json
import logging
from datetime import datetime
from log_config import setup_logging

setup_logging()

def combine_results(results_dir, combined_file):
    """Combine all JSON results into a single file."""
    logging.info(f"Starting results combination process from {results_dir}")
    combined_data = []
    json_files = [f for f in os.listdir(results_dir) if f.endswith('.json')]
    logging.info(f"Found {len(json_files)} JSON files to process")

    for filename in json_files:
        if filename == "combined_results.json" or filename == combined_file:
            logging.info(f"Skipping {filename} as it's a combined results file")
            continue

        file_path = os.path.join(results_dir, filename)
        logging.info(f"Processing {filename}")
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                rulename = filename.replace(".json", '')
                data['rulename'] = rulename
                combined_data.append(data)
        except json.JSONDecodeError as e:
            logging.error(f"Error processing {filename}: {str(e)}")
        except Exception as e:
            logging.error(f"Unexpected error processing {filename}: {str(e)}")
    
    combined_dir = f"{results_dir}/combined"
    if not os.path.exists(combined_dir):
        logging.info(f"Creating combined results directory: {combined_dir}")
        os.mkdir(combined_dir)
    
    output_path = f"{combined_dir}/{combined_file}"
    logging.info(f"Writing combined results to {output_path}")
    try:
        with open(output_path, 'w') as f:
            json.dump(combined_data, f, indent=2)
        logging.info(f"Successfully combined {len(combined_data)} results")
    except Exception as e:
        logging.error(f"Error writing combined results: {str(e)}")
        raise

if __name__ == "__main__":
    results_dir = "./results"
    combined_file = "./results/combined_results.json"
    combine_results(results_dir, combined_file)
