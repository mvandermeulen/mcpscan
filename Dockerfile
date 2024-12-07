# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install git
RUN apt-get update && apt-get install -y git

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Copy the src directory contents into the container at /app/src
COPY src/ /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run run_all.py when the container launches
CMD ["python", "run_all.py"]
