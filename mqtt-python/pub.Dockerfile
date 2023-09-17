# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory to /mqtt-pub
WORKDIR /mqtt-pub

# Copy the current directory contents into the container at /mqtt-pub
COPY . /mqtt-pub

# Install any needed packages specified in requirements.txt (if you have any)
RUN pip install --no-cache-dir -r requirements.txt

# Define an environment variable for the MQTT broker IP address
ENV MQTT_BROKER_HOST="localhost"
ENV MQTT_BROKER_PORT=1883

# run the python mqtt client file
CMD ["python", "mqtt_publisher.py"]
