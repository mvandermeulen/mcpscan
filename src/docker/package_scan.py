import os
import subprocess
import json
from datetime import datetime

def scan(working_dir="./working", output_dir="./results"):
    """
    Scan a cloned repository for npm package security vulnerabilities and save results
    
    Args:
        working_dir (str): Directory containing the cloned repository
        output_dir (str): Directory to save scan results
    
    Returns:
        str: Path to the output file containing scan results
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Check if package.json exists
    if not os.path.exists(os.path.join(working_dir, 'package.json')):
        print(f"No package.json found in {working_dir}")
        return None

    # Generate unique filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    repo_name = os.path.basename(os.path.abspath(working_dir))
    output_file = os.path.join(output_dir, f"scan_{repo_name}_{timestamp}.json")
    
    # Run npm audit in the working directory
    try:
        result = subprocess.run(
            ["npm", "audit", "--json"],
            cwd=working_dir,
            capture_output=True,
            text=True,
            check=False  # Don't raise exception on audit findings
        )
        
        # Save results
        with open(output_file, 'w') as f:
            if result.stdout:
                json.dump(json.loads(result.stdout), f, indent=2)
            else:
                json.dump({"error": result.stderr}, f, indent=2)
                
        print(f"Scan completed. Results saved to: {output_file}")
        return output_file
        
    except subprocess.CalledProcessError as e:
        print(f"Error scanning repository in {working_dir}: {str(e)}")
        return None

if __name__ == "__main__":
    import sys
    working_dir = sys.argv[1] if len(sys.argv) > 1 else "./working"
    scan(working_dir)
