#!/bin/bash

# Run the Docker container
#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
docker run --rm \
  -v "${SCRIPT_DIR}/results:/app/results" \
  mcpscan python /app/run_all_repo.py "$@"
