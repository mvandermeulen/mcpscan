import subprocess

def run_semgrep(clone_dir, output_file):
    """Run semgrep on the cloned repository."""
    rule_files = [
        "semgrep_rules/extract_https_strings.yml",
        "semgrep_rules/extract_http_strings.yml",
        "semgrep_rules/detect_obfuscated_python.yml",
        "semgrep_rules/detect_obfuscated_javascript.yml",
        "semgrep_rules/detect_dangerous_code.yml"
    ]
    for rule_file in rule_files:
        subprocess.run(["semgrep", "--config", rule_file, clone_dir, "--json", "-o", output_file], check=True)

if __name__ == "__main__":
    clone_dir = "./working"
    output_file = "./working/results.json"
    run_semgrep(clone_dir, output_file)
