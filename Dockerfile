# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Install tk dependencies
RUN apt-get update && apt-get install -y \
    tk-dev libx11-6 libx11-dev libxft2 libxss1 && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on (if applicable)
EXPOSE 5000

# Command to run the application
CMD ["python", "main.py"]
