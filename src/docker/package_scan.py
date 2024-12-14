import os
import subprocess
import json
from datetime import datetime

def scan(package_name, output_dir="./results"):
    """
    Scan a package for security vulnerabilities and save results
    
    Args:
        package_name (str): Name of the package to scan
        output_dir (str): Directory to save scan results
    
    Returns:
        str: Path to the output file containing scan results
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate unique filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output_file = os.path.join(output_dir, f"scan_{package_name}_{timestamp}.json")
    
    # Run npm audit
    try:
        result = subprocess.run(
            ["npm", "audit", "--json", package_name],
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
        print(f"Error scanning package {package_name}: {str(e)}")
        return None

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python package_scan.py <package_name>")
        sys.exit(1)
    scan(sys.argv[1])
