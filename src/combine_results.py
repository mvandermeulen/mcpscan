import os
import json

def combine_results(results_dir, combined_file):
    print(combined_file)
    """Combine all JSON results into a single file."""
    combined_data = []
    for filename in os.listdir(results_dir):
        if filename.endswith(".json"):
            if filename == "combined_results.json":
                continue
            with open(os.path.join(results_dir, filename), 'r') as f:
                data = json.load(f)
                rulename = filename.replace(".json", '')
                data['rulename'] = rulename
                combined_data.append(data)
    
    with open(f"{results_dir}/{combined_file}", 'w') as f:
        json.dump(combined_data, f, indent=2)

if __name__ == "__main__":
    results_dir = "./results"
    combined_file = "./results/combined_results.json"
    combine_results(results_dir, combined_file)
