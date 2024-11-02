# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install necessary dependencies
RUN apt-get update && \
    apt-get install -y python3-tk

# Copy dependency file
COPY requirements.txt ./

# Install Python packages
RUN pip3 install --no-cache-dir -r ./requirements.txt

# Set environment variable to use the host's display
ENV DISPLAY=host.docker.internal:0

# Create an application directory
WORKDIR /weather

# Set PYTHONPATH to include /app directory
ENV PYTHONPATH=/weather/app

# Copy the Tkinter application to the container
COPY . .

# Run the Tkinter app
CMD ["python", "app/main.py"]