import sys
import os
import datetime
from cleanup import cleanup
from database import add_plugin_record, get_plugin_and_hash
import hashlib
from repo import clone_repo, get_latest_commit_hash
from run_scan import run_semgrep
from combine_results import combine_results

def main(repo_url):
    clone_dir = "./working"
    results_dir = "./results"
    output_file_name = "results.json"
    output_file = os.path.join(results_dir, output_file_name)

    # Cleanup before starting
    try:
        cleanup(clone_dir)

    except Exception as e:
        print(f"Initial cleanup failed: {e}")
        sys.exit(1)
    try:
        # Clone the repository
        clone_repo(repo_url, clone_dir)

        # Get the latest commit hash of the repository
        repo_hash = get_latest_commit_hash(clone_dir)

        # Retrieve the plugin record and its hash
        plugin_record = get_plugin_and_hash(repo_url)

        if not plugin_record:
            # Add the plugin record if it doesn't exist
            add_plugin_record(plugin_name=repo_url, plugin_hash=repo_hash)

        # Compare the hash and only continue if the hash has changed
        existing_hash = plugin_record[0]
        if existing_hash != repo_hash:
            add_plugin_record(plugin_name=repo_url, plugin_hash=repo_hash)
            run_semgrep(clone_dir, output_file_name)
            repo_name = repo_url.split('/')[-1]
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            combine_results(results_dir, f"{repo_name}_{timestamp}.json")

    except Exception as e:
        print(f"An error occurred: {e}")
        print(e)
        sys.exit(1)
    finally:
        # Cleanup
        try:
            cleanup(clone_dir)
        except Exception as e:
            print(f"Cleanup failed: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python run_all.py <repo_url>")
        sys.exit(1)
    repo_url = sys.argv[1]
    main(repo_url)
