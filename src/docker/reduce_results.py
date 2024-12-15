# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json
import logging
from log_config import setup_logging
from pathlib import Path

setup_logging()

def reduce_results(combined_file_path, output_dir="./results/reduced"):
    """
    Reduce combined results into a simplified format focusing on key findings.
    """
    logging.info(f"Reading combined results from {combined_file_path}")
    
    try:
        with open(combined_file_path, 'r') as f:
            combined_data = json.load(f)
    except Exception as e:
        logging.error(f"Error reading combined results: {str(e)}")
        raise

    # Create summary structure
    summary = {
        'total_findings': 0,
        'findings_by_rule': {},
        'all_matches': []
    }

    # Process each result
    for result in combined_data:
        rule_name = result.get('rulename', 'unknown')
        matches = result.get('matches', [])
        
        # Count findings per rule
        summary['findings_by_rule'][rule_name] = len(matches)
        summary['total_findings'] += len(matches)
        
        # Extract essential information from matches
        for match in matches:
            simplified_match = {
                'rule': rule_name,
                'path': match.get('path', ''),
                'line': match.get('start', {}).get('line', 0),
                'snippet': match.get('extra', {}).get('lines', ''),
                'message': match.get('extra', {}).get('message', '')
            }
            summary['all_matches'].append(simplified_match)

    # Create output directory if it doesn't exist
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save JSON summary
    json_path = output_dir / 'reduced_results.json'
    with open(json_path, 'w') as f:
        json.dump(summary, f, indent=2)

    # Create human-readable report
    txt_path = output_dir / 'summary_report.txt'
    with open(txt_path, 'w') as f:
        f.write(f"Security Scan Summary\n{'='*20}\n\n")
        f.write(f"Total Findings: {summary['total_findings']}\n\n")
        
        f.write("Findings by Rule:\n")
        for rule, count in summary['findings_by_rule'].items():
            f.write(f"- {rule}: {count} finding(s)\n")
        
        f.write("\nDetailed Findings:\n")
        for match in summary['all_matches']:
            f.write(f"\nRule: {match['rule']}\n")
            f.write(f"File: {match['path']} (line {match['line']})\n")
            f.write(f"Finding: {match['message']}\n")
            if match['snippet']:
                f.write(f"Code: {match['snippet']}\n")

    logging.info(f"Reduced results saved to {output_dir}")
    return summary

if __name__ == "__main__":
    reduce_results("./results/combined/combined_results.json")
