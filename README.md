# Repository Security Scanner

A Docker-based security scanning tool that analyzes Git repositories for potential security issues using multiple scanning tools:
- Semgrep for code pattern analysis
- npm audit for JavaScript/Node.js dependencies
- pip-audit for Python dependencies

## Features

- Automated repository cloning and scanning
- Multi-tool security analysis:
  - Static code analysis with Semgrep rules for:
    - Dangerous code patterns
    - Local file access
    - Network access
    - Obfuscated code
    - Process execution
    - HTTP/HTTPS strings
  - Dependency vulnerability scanning:
    - Python package vulnerabilities via pip-audit
    - JavaScript package vulnerabilities via npm audit
- Automatic project type detection (Python/JavaScript)
- Results aggregation and reporting in JSON format
- Docker containerization for isolated scanning
- Automatic cleanup of temporary files

## Prerequisites

- Docker installed and running
- Python 3.x (for running MCP-Get scanner)
- Internet connection for repository cloning and package list fetching

## Installation

1. Clone this repository
2. Build the Docker container:
```bash
./src/docker_build.sh
```

## Usage

### Scanning a Single Repository

```bash
./src/docker_run_one.sh <repository-url>
```

Example:
```bash
./src/docker_run_one.sh https://github.com/username/repository
```

### Scanning Multiple Repositories from MCP-Get

```bash
python3 src/docker_run_mcp_get.py
```

This will:
1. Fetch the package list from MCP-Get
2. Clone each repository
3. Run security scans
4. Save results to the `results` directory

## Output

Scan results are saved in the `results` directory with:
- Semgrep analysis results
- Package vulnerability scan results (pip-audit/npm audit)
- Results are in JSON format for easy parsing

## Project Structure

- `src/docker/semgrep_rules/` - Custom Semgrep rule definitions
- `src/docker/` - Core scanning logic and utilities
  - `package_scan.py` - Dependency vulnerability scanning
  - `cleanup.py` - Temporary file management
  - Other scanning utilities
- `results/` - Scan output directory (created during execution)

## Dependencies

This project relies on:

- Docker
- Python 3.x
- Semgrep (installed in Docker container)
- pip-audit (installed during scanning)
- npm (for JavaScript projects)
- Requests library for Python

## Third-Party Attributions

- [Semgrep](https://semgrep.dev/) - Static analysis tool (OSS License)
- [pip-audit](https://pypi.org/project/pip-audit/) - Python dependency scanner (Apache 2.0)
- [npm audit](https://docs.npmjs.com/cli/v8/commands/npm-audit) - Node.js dependency scanner
- [Requests](https://requests.readthedocs.io/) - HTTP library for Python (Apache 2.0)
- [MCP-Get](https://github.com/michaellatman/mcp-get) - Package list source

## License

[Add your license information here]

## Contributing

[Add contribution guidelines here]
