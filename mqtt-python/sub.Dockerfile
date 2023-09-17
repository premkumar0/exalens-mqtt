# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory to /mqtt-sub
WORKDIR /mqtt-sub

# Copy the current directory contents into the container at /mqtt-sub
COPY . /mqtt-sub

# Install any needed packages specified in requirements.txt (if you have any)
RUN pip install --no-cache-dir -r requirements.txt

# Define environment variables (optional)
ENV MQTT_BROKER_HOST="localhost"
ENV MQTT_BROKER_PORT=1883
ENV MONGODB_URI="mongodb://localhost:27017/"

# Run your MQTT subscriber script
CMD ["python", "mqtt_subscriber.py"]
