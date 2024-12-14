import subprocess
import sys
import os
import json
import logging
from log_config import setup_logging

setup_logging()

def run_semgrep(clone_dir, output_file_name):
    results_dir = "./results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    """Run semgrep on the cloned repository using all YAML rules."""
    rules_dir = "semgrep_rules"
    errors = []
    
    # Get all YAML files from the rules directory
    rule_files = [os.path.join(rules_dir, f) for f in os.listdir(rules_dir) 
                 if f.endswith('.yml') or f.endswith('.yaml')]
    
    for rule_file in rule_files:
        output_file = os.path.join(results_dir, f"{os.path.basename(rule_file).replace('.yml', '')}_{output_file_name}")
        try:
            subprocess.run([
                "semgrep", 
                "--config", rule_file, 
                clone_dir, 
                "--json", 
                "-o", output_file
            ], check=True)
        except Exception as e:
            error_msg = f"Error running Semgrep with {rule_file}: {e}"
            logging.error(error_msg)
            errors.append(error_msg)

    if errors:
        with open(output_file, "a") as f:
            json.dump({"errors": errors}, f, indent=2)
        sys.exit(1)

if __name__ == "__main__":
    clone_dir = "./working"
    output_file = "./working/results.json"
    run_semgrep(clone_dir, output_file)
