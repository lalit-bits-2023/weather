# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install necessary dependencies
RUN apt-get update && \
    apt-get install -y python3-tk

# Set environment variable to use the host's display
ENV DISPLAY=host.docker.internal:0

# Create an application directory
WORKDIR /app

# Copy the Tkinter application to the container
COPY . .

# Run the Tkinter app
CMD ["python", "./main.py"]