#!/bin/bash

# Run the Docker container
docker run --rm -v "$(pwd)/results:/app/results" semgrep-runner python /app/run_all.py "$@"
