FROM python:3.9

# Install required dependencies
RUN apt-get update && apt-get install -y \
    tk \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the application files to the container
COPY . /app

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the environment variable for X11 forwarding
ENV DISPLAY=:0

# Run the application
CMD [ "python", "app.py" ]