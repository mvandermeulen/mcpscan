#!/bin/bash

# Build the Docker image
docker build -t semgrep-runner .

# Run the Docker container
docker run --rm -v "$(pwd)/results:/app/results" semgrep-runner "$@"
