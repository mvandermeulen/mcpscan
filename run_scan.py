from semgrep import semgrep_main
import json
import sys

def run_semgrep(clone_dir, output_file):
    """Run semgrep on the cloned repository."""
    rule_files = [
        "semgrep_rules/extract_https_strings.yml",
        "semgrep_rules/extract_http_strings.yml",
        "semgrep_rules/detect_obfuscated_python.yml",
        "semgrep_rules/detect_obfuscated_javascript.yml",
        "semgrep_rules/detect_dangerous_code.yml"
    ]
    errors = []
    for rule_file in rule_files:
        try:
            semgrep_main.main(["--config", rule_file, clone_dir, "--json", "-o", output_file])
        except Exception as e:
            errors.append(f"Error running Semgrep with {rule_file}: {e}")

    if errors:
        with open(output_file, "a") as f:
            json.dump({"errors": errors}, f, indent=2)
        sys.exit(1)

if __name__ == "__main__":
    clone_dir = "./working"
    output_file = "./working/results.json"
    run_semgrep(clone_dir, output_file)
