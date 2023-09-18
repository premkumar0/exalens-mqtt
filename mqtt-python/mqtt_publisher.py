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


# Function to generate a random sensor reading
def generrate_temperature():
    sensor_id = "temp_sensor_001"
    value = round(random.uniform(30, 50), 2)  # Random reading between 0 and 100
    timestamp = datetime.now().isoformat()
    payload = {"sensor_id": sensor_id, "value": value, "timestamp": timestamp}
    return json.dumps(payload)


# Function to generate a random sensor reading
def generrate_humidity():
    sensor_id = "humd_sensor_001"
    value = round(random.uniform(40, 80), 2)  # Random reading between 0 and 100
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
    temp_readings = generrate_temperature()
    humd_readings = generrate_humidity()

    # Publish to Temperature Topic
    client.publish(mqtt_topic_temperature, temp_readings)
    print(f"Published to {mqtt_topic_temperature}: {temp_readings}")

    # Publish to Humidity Topic
    client.publish(mqtt_topic_humidity, humd_readings)
    print(f"Published to {mqtt_topic_humidity}: {humd_readings}")

    time.sleep(5)  # Adjust the interval as needed
