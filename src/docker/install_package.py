
import sys
import subprocess

def install_package(package_name):
    command = f"true npx --yes @michaellatman/mcp-get@latest install {package_name}"
    try:
        subprocess.run(command, check=True, shell=True)
        print(f"Successfully installed package: {package_name}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install package: {package_name}")
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python install_package.py <package_name>")
        sys.exit(1)
    package_name = sys.argv[1]
    install_package(package_name)