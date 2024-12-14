# Repository Security Scanner

A Docker-based security scanning tool that analyzes Git repositories for potential security issues using Semgrep rules. This tool can scan individual repositories or process multiple repositories from package lists.

## Features

- Automated repository cloning and scanning
- Custom Semgrep rule sets for detecting:
  - Dangerous code patterns
  - Local file access
  - Network access
  - Obfuscated code
  - Process execution
  - HTTP/HTTPS strings
- Results aggregation and reporting
- Docker containerization for isolated scanning

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

This will fetch and scan all repositories listed in the MCP-Get package list.

### Building the Docker Container

```bash
./src/docker_build.sh
```

## Project Structure

- `src/docker/semgrep_rules/` - Custom Semgrep rule definitions
- `src/docker/` - Core scanning logic and utilities
- Results are stored in a `results` directory by default

## Dependencies

This project relies on:

- Docker
- Python 3.x
- Semgrep (installed in Docker container)
- Requests library for Python

## Third-Party Attributions

- [Semgrep](https://semgrep.dev/) - Static analysis tool (OSS License)
- [Requests](https://requests.readthedocs.io/) - HTTP library for Python (Apache 2.0)
- [MCP-Get](https://github.com/michaellatman/mcp-get) - Package list source

## License

[Add your license information here]
