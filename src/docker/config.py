import os

# Base directories
BASE_DIR = os.getenv('MCPSCAN_BASE_DIR', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WORKING_DIR = os.getenv('MCPSCAN_WORKING_DIR', os.path.join(BASE_DIR, 'working'))
RESULTS_DIR = os.getenv('MCPSCAN_RESULTS_DIR', os.path.join(BASE_DIR, 'results'))

# Derived paths
COMBINED_DIR = os.path.join(RESULTS_DIR, 'combined')
RULES_DIR = os.path.join(BASE_DIR, 'docker', 'semgrep_rules')

# Ensure directories exist
os.makedirs(WORKING_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(COMBINED_DIR, exist_ok=True)
