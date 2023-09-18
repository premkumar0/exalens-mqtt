import json
import os

import paho.mqtt.client as mqtt
import pymongo
import redis

# MQTT Broker Settings
mqtt_broker_host = os.getenv("MQTT_BROKER_HOST", "localhost")
mqtt_broker_port = int(os.getenv("MQTT_BROKER_PORT", 1883))
mqtt_topic_temperature = "sensors/temperature"
mqtt_topic_humidity = "sensors/humidity"

# MongoDB Settings
mongodb_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
mongodb_database = "mqtt_data"  # Create or use an existing database
mongodb_collection = "sensor_readings"  # Create or use an existing collection

# Redis Settings
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))


# Callback when a message is received
def on_message(client, userdata, message):
    try:
        payload_str = message.payload.decode("utf-8")
        payload = json.loads(payload_str)
        store_message_in_mongodb(payload)
        print(f"Received and stored message: {payload}")
        if message.topic == mqtt_topic_temperature:
            # Push the reading to Redis
            redis_client.lpush("temperature", payload_str)
            # Trim the list to keep the last ten readings
            redis_client.ltrim("temperature", 0, 9)
        elif message.topic == mqtt_topic_humidity:
            # Push the reading to Redis
            redis_client.lpush("humidity", payload_str)
            # Trim the list to keep the last ten readings
            redis_client.ltrim("humidity", 0, 9)
    except Exception as e:
        print(f"Error processing message: {e}")


# Function to store the received message in MongoDB
def store_message_in_mongodb(payload):
    client = pymongo.MongoClient(mongodb_uri)
    db = client[mongodb_database]
    collection = db[mongodb_collection]
    collection.insert_one(payload)
    client.close()


# Redis settings
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=0)
# MQTT Client Setup
client = mqtt.Client()


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker")
        client.subscribe(mqtt_topic_temperature, 2)
        client.subscribe(mqtt_topic_humidity, 2)

    else:
        print("Connection failed")


client.on_connect = on_connect
client.on_message = on_message

# Connect to MQTT Broker
client.connect(mqtt_broker_host, mqtt_broker_port, 30)

# Start the MQTT subscriber
client.loop_forever()
