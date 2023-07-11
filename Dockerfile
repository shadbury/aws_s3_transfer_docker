# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the required files to the container
COPY requirements.txt /app
COPY app.py /app
COPY src /app/src

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port on which the app will run (adjust if necessary)
EXPOSE 8000

# Set the entrypoint command
CMD ["python", "app.py"]