FROM python:3.9

WORKDIR /app

COPY firewall_updater.py .
COPY serviceaccount.json .

# Install dependencies
RUN pip install google-api-python-client

# Set environment variables (should set in configmap)
#ENV PROJECT=x
#ENV FIREWALL_NAME=x
#ENV TARGET_TAG=x
#ENV CREDENTIALS_FILE=x
#ENV RUN_INTERVAL=5m 

# Run the script
CMD ["python", "firewall_updater.py"]

