import os
import subprocess

def detect_and_install(clone_dir):
    # Check for Python project
    if os.path.exists(os.path.join(clone_dir, 'requirements.txt')):
        print("Detected a Python project.")
        subprocess.run(['pip', 'install', 'pip-audit'], check=True)
        print("pip-audit installed.")
    # Check for JavaScript project
    elif os.path.exists(os.path.join(clone_dir, 'package.json')):
        print("Detected a JavaScript project.")
        subprocess.run(['npm', 'install', '-g', 'npm-audit'], check=True)
        print("npm-audit installed.")
    else:
        print("No recognizable project files found.")

if __name__ == "__main__":
    # Example usage
    detect_and_install('./working')
