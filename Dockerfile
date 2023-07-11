FROM python:3.9

# Import missing GPG keys
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 40976EAF437D05B5 3B4FE6ACC0B21F32

# Install XQuartz and other dependencies
RUN echo "deb http://security.ubuntu.com/ubuntu xenial-security main" >> /etc/apt/sources.list \
    && apt-get update \
    && apt-get install -y x11-apps \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install other dependencies
RUN apt-get update && apt-get install -y <other-dependencies>

# Set up the app
WORKDIR /app
COPY . /app

# Install Python dependencies
RUN pip install -r requirements.txt

# Set the display environment variable
ENV DISPLAY=:0

# Set the entrypoint
ENTRYPOINT ["/app/app.py"]
