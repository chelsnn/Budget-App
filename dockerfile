# # Use an official Python runtime as the base image
# FROM python:3.10-slim

# # Set the working directory inside the container
# WORKDIR /app

# # Copy the current directory contents into the container at /app
# COPY . /app

# # Update pip to the latest version

# RUN python -m pip install --upgrade pip

# RUN apt-get update && apt-get install -y \
#     build-essential \
#     libssl-dev \
#     libffi-dev \
#     curl \
#     python3-dev \
#     && rm -rf /var/lib/apt/lists/*

# RUN pip install --no-cache-dir Cython

# # Install any dependencies specified in requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt


# # Expose the port that your Flask app runs on
# EXPOSE 5000

# # Define environment variable for Flask
# ENV FLASK_APP=app.py

# # Command to run the application
# CMD ["flask", "run", "--host=0.0.0.0"]
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    python3-dev \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Cython globally
RUN pip install --no-cache-dir Cython

# Set the working directory
WORKDIR /app

# Copy application files
COPY . /app

# Install Python dependencies

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Run the application
CMD ["python", "app.py"]
