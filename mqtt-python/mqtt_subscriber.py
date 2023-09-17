import paho.mqtt.client as mqtt
import pymongo
import json
import os

# MQTT Broker Settings
mqtt_broker_host = os.getenv("MQTT_BROKER_HOST", "localhost")
mqtt_broker_port = int(os.getenv("MQTT_BROKER_PORT", 1883))
mqtt_topic = "sensors/temperature"
mqtt_topic_humidity = "sensors/humidity"

# MongoDB Settings
mongodb_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
mongodb_database = "mqtt_data"  # Create or use an existing database
mongodb_collection = "sensor_readings"  # Create or use an existing collection


# Callback when a message is received
def on_message(client, userdata, message):
    try:
        payload = json.loads(message.payload.decode("utf-8"))
        store_message_in_mongodb(payload)
        print(f"Received and stored message: {payload}")
    except Exception as e:
        print(f"Error processing message: {e}")


# Function to store the received message in MongoDB
def store_message_in_mongodb(payload):
    client = pymongo.MongoClient(mongodb_uri)
    db = client[mongodb_database]
    collection = db[mongodb_collection]
    collection.insert_one(payload)
    client.close()


# MQTT Client Setup
client = mqtt.Client()


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker")
        client.subscribe(mqtt_topic)
        client.subscribe(mqtt_topic_humidity)

    else:
        print("Connection failed")


client.on_connect = on_connect
client.on_message = on_message

# Connect to MQTT Broker
client.connect(mqtt_broker_host, mqtt_broker_port, 30)

# Start the MQTT subscriber
client.loop_forever()
