#!/bin/bash

# Run the Docker container
docker run --rm -v "$(pwd)/results:/app/results" mcpscan python /app/run_all_repo.py "$@"
