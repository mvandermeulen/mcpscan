#!/bin/bash

# Build the Docker image
docker build -t semgrep-runner .

# Run the Docker container
docker run --rm -v "$(pwd)/results:/app/results" semgrep-runner python /app/run_all.py "$@"
#!/bin/bash

# Run the Docker container
docker run -it --rm --name my-running-app my-python-app
