# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json
import logging
import datetime
import os
from pathlib import Path
from log_config import setup_logging
from pathlib import Path

setup_logging()

def reduce_results(combined_file_path, output_dir="./results/reduced"):
    """
    Reduce combined results into a simplified format focusing on key findings.
    """
    logging.info(f"Starting reduction process for {combined_file_path}")
    
    if not os.path.exists(combined_file_path):
        error_msg = f"Combined results file not found: {combined_file_path}"
        logging.error(error_msg)
        raise FileNotFoundError(error_msg)
    
    # Extract server name from combined file path
    try:
        combined_filename = os.path.basename(combined_file_path)
        server_name = combined_filename.split('_')[0]
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        logging.info(f"Processing results for server: {server_name}")
    except Exception as e:
        error_msg = f"Error extracting server name from filename: {str(e)}"
        logging.error(error_msg)
        raise ValueError(error_msg)
    
    # Read combined results
    try:
        with open(combined_file_path, 'r') as f:
            combined_data = json.load(f)
        logging.info(f"Successfully loaded combined results data")
    except json.JSONDecodeError as e:
        error_msg = f"Invalid JSON in combined results: {str(e)}"
        logging.error(error_msg)
        raise
    except Exception as e:
        error_msg = f"Error reading combined results: {str(e)}"
        logging.error(error_msg)
        raise

    # Create summary structure
    summary = {
        'total_findings': 0,
        'findings_by_rule': {},
        'all_matches': []
    }

    # Process each result
    processed_count = 0
    error_count = 0
    
    try:
        if isinstance(combined_data, str):
            logging.info("Converting string data to JSON")
            combined_data = json.loads(combined_data)
            
        if not isinstance(combined_data, list):
            logging.info("Converting single result to list")
            combined_data = [combined_data]
            
        total_results = len(combined_data)
        logging.info(f"Processing {total_results} results")
        
        for index, result in enumerate(combined_data, 1):
            try:
                if not isinstance(result, dict):
                    logging.warning(f"Skipping invalid result format: {result}")
                    error_count += 1
                    continue
                
                logging.debug(f"Processing result {index}/{total_results}")
                rule_name = result.get('rulename', 'unknown')
                
                # Process the result based on rule type
                if rule_name == 'package_scan':
                    logging.debug("Processing package scan result")
                    try:
                        vulnerabilities = result.get('vulnerabilities', {})
                        metadata = result.get('metadata', {}).get('vulnerabilities', {})
                        
                        # Process vulnerabilities
                        for package_name, vuln_data in vulnerabilities.items():
                            simplified_match = {
                                'rule': rule_name,
                                'package': package_name,
                                'severity': vuln_data.get('severity', ''),
                                'is_direct': vuln_data.get('isDirect', False),
                                'via': vuln_data.get('via', []),
                                'effects': vuln_data.get('effects', []),
                                'version_range': vuln_data.get('range', ''),
                                'nodes': vuln_data.get('nodes', []),
                                'fix_available': vuln_data.get('fixAvailable', False),
                                'type': 'vulnerability'
                            }
                            summary['all_matches'].append(simplified_match)
                        
                        # Add metadata summary
                        summary['vulnerability_summary'] = {
                            'info': metadata.get('info', 0),
                            'low': metadata.get('low', 0),
                            'moderate': metadata.get('moderate', 0),
                            'high': metadata.get('high', 0),
                            'critical': metadata.get('critical', 0),
                            'total': metadata.get('total', 0)
                        }
                    except Exception as e:
                        logging.error(f"Error processing package scan result: {str(e)}")
                        error_count += 1
                else:
                    # Process other types of results
                    matches = result.get('matches', [])
                    summary['findings_by_rule'][rule_name] = len(matches)
                    summary['total_findings'] += len(matches)
                    
                    for match in matches:
                        try:
                            simplified_match = {
                                'rule': rule_name,
                                'path': match.get('path', ''),
                                'line': match.get('start', {}).get('line', 0),
                                'snippet': match.get('extra', {}).get('lines', ''),
                                'message': match.get('extra', {}).get('message', ''),
                                'type': 'finding'
                            }
                            summary['all_matches'].append(simplified_match)
                        except Exception as e:
                            logging.error(f"Error processing match: {str(e)}")
                            error_count += 1
                
                processed_count += 1
                
            except Exception as e:
                logging.error(f"Error processing result {index}: {str(e)}")
                error_count += 1
            
        rule_name = result.get('rulename', 'unknown')
        matches = result.get('matches', [])
        
        # Count findings per rule
        summary['findings_by_rule'][rule_name] = len(matches)
        summary['total_findings'] += len(matches)
        
        # Handle package scan results differently
        if rule_name == 'package_scan':
            vulnerabilities = result.get('vulnerabilities', {})
            for package_name, vuln_data in vulnerabilities.items():
                simplified_match = {
                    'rule': rule_name,
                    'package': package_name,
                    'severity': vuln_data.get('severity', ''),
                    'is_direct': vuln_data.get('isDirect', False),
                    'via': vuln_data.get('via', []),
                    'effects': vuln_data.get('effects', []),
                    'version_range': vuln_data.get('range', ''),
                    'nodes': vuln_data.get('nodes', []),
                    'fix_available': vuln_data.get('fixAvailable', False),
                    'type': 'vulnerability'
                }
                summary['all_matches'].append(simplified_match)
            
            # Add metadata summary
            metadata = result.get('metadata', {}).get('vulnerabilities', {})
            summary['vulnerability_summary'] = {
                'info': metadata.get('info', 0),
                'low': metadata.get('low', 0),
                'moderate': metadata.get('moderate', 0),
                'high': metadata.get('high', 0),
                'critical': metadata.get('critical', 0),
                'total': metadata.get('total', 0)
            }
        else:
            # Extract essential information from regular matches
            for match in matches:
                simplified_match = {
                    'rule': rule_name,
                    'path': match.get('path', ''),
                    'line': match.get('start', {}).get('line', 0),
                    'snippet': match.get('extra', {}).get('lines', ''),
                    'message': match.get('extra', {}).get('message', ''),
                    'type': 'finding'
                }
                summary['all_matches'].append(simplified_match)

        # Create output directory if it doesn't exist
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Save results
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Save JSON summary
        json_filename = f"{server_name}_{timestamp}_reduced.json"
        json_path = os.path.join(output_dir, json_filename)
        with open(json_path, 'w') as f:
            json.dump(summary, f, indent=2)
        logging.info(f"Saved JSON summary to {json_path}")
        
        # Save text report
        txt_filename = f"{server_name}_{timestamp}_summary.txt"
        txt_path = os.path.join(output_dir, txt_filename)
        with open(txt_path, 'w') as f:
            f.write("Security Scan Summary Report\n")
            f.write(f"Generated: {datetime.datetime.now()}\n\n")
            f.write(f"Total Results Processed: {processed_count}\n")
            f.write(f"Errors Encountered: {error_count}\n")
        logging.info(f"Saved text summary to {txt_path}")
        
        # Log completion statistics
        logging.info(f"Reduction complete: {processed_count} results processed, {error_count} errors")
        if error_count > 0:
            logging.warning(f"Encountered {error_count} errors during processing")
            
        return summary
        
    except Exception as e:
        error_msg = f"Error saving reduced results: {str(e)}"
        logging.error(error_msg)
        raise

    # Create human-readable report with server name and timestamp
    txt_filename = f"{server_name}_{timestamp}_summary.txt"
    txt_path = output_dir / txt_filename
    with open(txt_path, 'w') as f:
        f.write(f"Security Scan Summary\n{'='*20}\n\n")
        f.write(f"Total Findings: {summary['total_findings']}\n\n")
        
        f.write("Findings by Rule:\n")
        for rule, count in summary['findings_by_rule'].items():
            f.write(f"- {rule}: {count} finding(s)\n")
        
        f.write("\nDetailed Findings:\n")
        for match in summary['all_matches']:
            f.write(f"\nRule: {match['rule']}\n")
            if match['type'] == 'vulnerability':
                f.write(f"Package: {match['package']}\n")
                f.write(f"Severity: {match['severity']}\n")
                f.write(f"Direct Dependency: {match['is_direct']}\n")
                if match['via']:
                    f.write(f"Via: {', '.join(match['via'])}\n")
                if match['effects']:
                    f.write(f"Effects: {', '.join(match['effects'])}\n")
                f.write(f"Affected Versions: {match['version_range']}\n")
                f.write(f"Locations: {', '.join(match['nodes'])}\n")
                f.write(f"Fix Available: {match['fix_available']}\n")
            else:
                f.write(f"File: {match['path']} (line {match['line']})\n")
                f.write(f"Finding: {match['message']}\n")
                if match['snippet']:
                    f.write(f"Code: {match['snippet']}\n")

    logging.info(f"Reduced results saved to {output_dir}")
    return summary

if __name__ == "__main__":
    reduce_results("./results/combined/combined_results.json")
