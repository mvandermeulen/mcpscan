import os
import subprocess
import json
from datetime import datetime

def detect_project_type(working_dir):
    """
    Detect if the project is Python or JavaScript
    
    Args:
        working_dir (str): Directory to check
        
    Returns:
        str: 'python', 'javascript', or None
    """
    # Python project indicators
    python_files = [
        'requirements.txt',
        'pyproject.toml',
        'setup.py',
        'Pipfile',
        'setup.cfg',
        'environment.yml',
        'conda.yaml',
        'poetry.lock'
    ]
    
    # Check for any Python project indicators
    for file in python_files:
        if os.path.exists(os.path.join(working_dir, file)):
            return 'python'
            
    # JavaScript/Node.js project indicators
    js_files = [
        'package.json',
        'package-lock.json',
        'yarn.lock',
        'pnpm-lock.yaml',
        'bower.json',
        'npm-shrinkwrap.json'
    ]
    
    # Check for JavaScript project indicators
    for file in js_files:
        if os.path.exists(os.path.join(working_dir, file)):
            return 'javascript'
        
    return None

def scan(working_dir="./working", output_dir="./results"):
    """
    Scan a cloned repository for security vulnerabilities using appropriate tool
    
    Args:
        working_dir (str): Directory containing the cloned repository
        output_dir (str): Directory to save scan results
    
    Returns:
        str: Path to the output file containing scan results
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Detect project type
    project_type = detect_project_type(working_dir)
    if not project_type:
        print(f"No recognizable project files found in {working_dir}")
        return None
        
    # Generate unique filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    repo_name = os.path.basename(os.path.abspath(working_dir))
    output_file = os.path.join(output_dir, f"scan_{repo_name}_{timestamp}.json")
    
    try:
        if project_type == 'javascript':
            print("Detected JavaScript project, running npm audit...")
            result = subprocess.run(
                ["npm", "audit", "--json"],
                cwd=working_dir,
                capture_output=True,
                text=True,
                check=False
            )
        else:  # python
            print("Detected Python project, running pip-audit...")
            # Install pip-audit if not already installed
            subprocess.run(["pip", "install", "pip-audit"], check=True, capture_output=True)
            result = subprocess.run(
                ["pip-audit", "--format", "json"],
                cwd=working_dir,
                capture_output=True,
                text=True,
                check=False
            )
        
        # Save results
        with open(output_file, 'w') as f:
            if result.stdout:
                try:
                    json.dump(json.loads(result.stdout), f, indent=2)
                except json.JSONDecodeError:
                    # If output isn't JSON, save as-is in a JSON wrapper
                    json.dump({"output": result.stdout}, f, indent=2)
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
