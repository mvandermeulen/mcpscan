import subprocess

def run_semgrep(clone_dir, output_file):
    """Run semgrep on the cloned repository."""
    subprocess.run(["semgrep", "--config", "semgrep_rules/extract_https_strings.yml", clone_dir, "--json", "-o", output_file], check=True)

if __name__ == "__main__":
    clone_dir = "/path/to/clone/dir"  # Replace with actual clone directory
    output_file = "/path/to/output/results.json"  # Replace with desired output file path
    run_semgrep(clone_dir, output_file)
