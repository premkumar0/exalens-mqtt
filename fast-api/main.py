from fastapi import FastAPI, Form
from pydantic import BaseModel
import pymongo
import redis
import os

app = FastAPI()

# Mongodb settings
mongo_url = os.getenv("MONGODB_URl", "mongodb://localhost:27017/")

# Redis Settings
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))


# MongoDB connection
mongo_client = pymongo.MongoClient(mongo_url)
mongo_db = mongo_client["mqtt_data"]
mongo_collection = mongo_db["sensor_readings"]

# Redis connection
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=0)


class MongoDBItem(BaseModel):
    key: str = Form(...)


class RedisItem(BaseModel):
    key: str = Form(...)


@app.post("/get_from_mongodb/")
async def get_from_mongodb(item: MongoDBItem):
    # Retrieve data from MongoDB
    result = mongo_collection.find_one({"key": item.key})
    if result:
        return result
    else:
        return {"message": "Item not found in MongoDB"}


@app.post("/get_from_redis/")
async def get_from_redis(item: RedisItem):
    # Retrieve data from Redis
    result = redis_client.get(item.key)
    if result:
        return {"value": result.decode("utf-8")}
    else:
        return {"message": "Item not found in Redis"}
