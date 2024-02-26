# syntax=docker/dockerfile:1.2
FROM python:latest
# put you docker configuration here

# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Make port 80 available to the world outside this container
EXPOSE 80

# Run the command to start uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]