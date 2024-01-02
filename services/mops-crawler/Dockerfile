# Use an official Python runtime as a base image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY ./requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app's source code from your host to your image filesystem.
COPY src/ /app/

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
