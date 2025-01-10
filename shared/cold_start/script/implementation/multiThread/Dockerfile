# Select a base image
FROM mariadb:10.5.8

# Install Python 3 and Redis CLI
RUN apt-get update && \
    apt-get install -y python3 python3-pip redis-tools && \
    rm -rf /var/lib/apt/lists/*

# Copy the entrypoint script into the container
COPY entrypoint.py /usr/local/bin/entrypoint.py

# Copy any required config file
COPY app.conf /etc/myapp/config

# Set the entrypoint
ENTRYPOINT ["python3", "/usr/local/bin/entrypoint.py"]

