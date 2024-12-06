import os
import json

def combine_results(results_dir, combined_file):
    """Combine all JSON results into a single file."""
    combined_data = []
    for filename in os.listdir(results_dir):
        if filename.endswith(".json"):
            with open(os.path.join(results_dir, filename), 'r') as f:
                data = json.load(f)
                combined_data.append(data)
    
    with open(combined_file, 'w') as f:
        json.dump(combined_data, f, indent=2)

if __name__ == "__main__":
    results_dir = "./results"
    combined_file = "./results/combined_results.json"
    combine_results(results_dir, combined_file)
