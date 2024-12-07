import os
import json

def combine_results(results_dir, combined_file):
    """Combine all JSON results into a single file."""
    combined_data = []
    for filename in os.listdir(results_dir):
        if filename.endswith(".json"):
            if filename == "combined_results.json" or filename == combined_file:
                print(f"Skipping {filename}")
                continue
            print(filename)
            print(combined_file)
            with open(os.path.join(results_dir, filename), 'r') as f:
                data = json.load(f)
                rulename = filename.replace(".json", '')
                data['rulename'] = rulename
                combined_data.append(data)
    
    if not os.path.exists(f"{results_dir}/combined"):
        os.mkdir(f"{results_dir}/combined")
    
    with open(f"{results_dir}/combined/{combined_file}", 'w') as f:
        json.dump(combined_data, f, indent=2)

if __name__ == "__main__":
    results_dir = "./results"
    combined_file = "./results/combined_results.json"
    combine_results(results_dir, combined_file)
