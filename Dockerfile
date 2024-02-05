# Use an official Python runtime as the base image
FROM python:3.8.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt /app/
COPY .env /app/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Create a startup script that runs the publisher, subscriber, and Dash app
CMD ["bash", "-c", "python3 manage.py runserver"]


