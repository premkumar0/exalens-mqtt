import json
import os
import random
import time
from datetime import datetime

import paho.mqtt.client as mqtt

# MQTT Broker Settings
mqtt_broker_host = os.getenv("MQTT_BROKER_HOST", "localhost")
mqtt_broker_port = int(os.getenv("MQTT_BROKER_PORT", 1883))
mqtt_topic_temperature = "sensors/temperature"
mqtt_topic_humidity = "sensors/humidity"

# List of unique sensor IDs
sensor_ids = ["sensor1", "sensor2", "sensor3"]


# Function to generate a random sensor reading
def generate_sensor_reading():
    sensor_id = random.choice(sensor_ids)
    value = round(random.uniform(0, 100), 2)  # Random reading between 0 and 100
    timestamp = datetime.now().isoformat()
    payload = {"sensor_id": sensor_id, "value": value, "timestamp": timestamp}
    return json.dumps(payload)


# MQTT Client Setup
client = mqtt.Client()


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker")
    else:
        print("Connection failed")


client.on_connect = on_connect

# Connect to MQTT Broker
client.connect(mqtt_broker_host, mqtt_broker_port, 30)

# Publish sensor readings at regular intervals
while True:
    sensor_reading = generate_sensor_reading()

    # Publish to Temperature Topic
    client.publish(mqtt_topic_temperature, sensor_reading)
    print(f"Published to {mqtt_topic_temperature}: {sensor_reading}")

    # Publish to Humidity Topic
    client.publish(mqtt_topic_humidity, sensor_reading)
    print(f"Published to {mqtt_topic_humidity}: {sensor_reading}")

    time.sleep(5)  # Adjust the interval as needed
