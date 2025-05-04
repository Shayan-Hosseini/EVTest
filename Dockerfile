# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install tk and additional dependencies for tkinter
RUN apt-get update && apt-get install -y \
    tk \
    libx11-6 \
    libxft2 \
    libxss1 \
    libxrender1 \
    libxtst6 \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on (if applicable)
EXPOSE 8000

# Command to run the application
CMD ["python", "main.py"]
