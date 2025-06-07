# Use an official Python runtime as the base image
FROM python:3.12-slim

# Set environment variables for development
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=47337
ENV DEBUG=true

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project code to the working directory
COPY . .

# Expose the port the app will run on
EXPOSE ${PORT}

# Command to run the application in debug mode
CMD ["python", "-u", "main.py"]
