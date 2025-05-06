# Use the official Python 3.12 slim image as the base image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /my-movies-api

# Copy the requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port 5000 for the application
EXPOSE 5000

# Copy the rest of the application files into the container
COPY . .

# Define the command to run the application using Gunicorn
CMD [ "gunicorn", "--bind" , "0.0.0.0:5000", "api.wsgi:app" ]