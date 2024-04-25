FROM python:3.9

WORKDIR /app

# Install curl and other dependencies
RUN apt-get update && apt-get install -y curl

# Download kubectl, make it executable, and move it to /usr/local/bin
RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" && \
    chmod +x ./kubectl && \
    mv ./kubectl /usr/local/bin/kubectl

# Copy your scripts and JSON file
COPY firewall_updater.py .
COPY serviceaccount.json .

# Install Python dependencies
RUN pip install google-api-python-client google-auth

# Set environment variables (can also be done via configmaps in Kubernetes)
#ENV PROJECT=x
#ENV FIREWALL_NAME=x
#ENV TARGET_TAG=x
#ENV CREDENTIALS_FILE=x
#ENV RUN_INTERVAL=5m
#GOOGLE_APPLICATION_CREDENTIALS=/app/serviceaccount.json

# Run the script
CMD ["python", "firewall_updater.py"]

