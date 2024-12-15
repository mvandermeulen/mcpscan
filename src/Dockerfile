# Use an official Python runtime as a parent image
FROM node:latest

# Set environment variables
ENV VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3-pip \
    python-is-python3 \
    python3.11-venv \
    && rm -rf /var/lib/apt/lists/*

# Set up Python virtual environment
RUN python -m venv $VIRTUAL_ENV && \
    pip install --no-cache-dir uv

# Install Node.js dependencies
RUN npm install -g npm-audit

# Set the working directory
WORKDIR /app

# Copy and install Python requirements first (for better caching)
COPY docker/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt pip-audit

# Copy application code last (changes most frequently)
COPY docker/ .

# Run run_all.py when the container launches
CMD ["python3", "run_all.py"]
