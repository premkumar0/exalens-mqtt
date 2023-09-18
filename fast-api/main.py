import json
import os
from datetime import datetime, timedelta

import pymongo
import redis
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
# Mongodb settings
mongo_url = os.getenv("MONGODB_URI", "mongodb://admin:password@localhost:27017/")

# Redis Settings
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))


# MongoDB connection
mongo_client = pymongo.MongoClient(mongo_url)
mongo_db = mongo_client["mqtt_data"]
mongo_collection = mongo_db["sensor_readings"]

# Redis connection
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=0)


@app.post("/get_from_mongodb/")
async def get_from_mongodb(request: Request):
    item = await request.form()
    # Retrieve data from MongoDB based on the selection and time range
    selection = item["selection"]
    form_start_time = item["start_time"]
    form_end_time = item["end_time"]

    # Convert form timestamps to datetime objects
    start_time = datetime.fromisoformat(form_start_time)
    end_time = datetime.fromisoformat(form_end_time)

    # Adjust the end_time to be one second before the next minute
    end_time += timedelta(seconds=59)

    # Retrieve data from MongoDB based on the selection and adjusted time range
    query = {
        "sensor_id": selection,
        "timestamp": {"$gte": start_time.isoformat(), "$lte": end_time.isoformat()},
    }
    results = mongo_collection.find(query)
    data = []
    for record in results:
        data.append(
            {
                "id": record["_id"].__str__(),
                "sensonr_id": record["sensor_id"],
                "value": record["value"],
                "timestamp": record["timestamp"],
            }
        )
    if data:
        return {"data": data}
    else:
        return {"message": "No data found in MongoDB"}


@app.post("/get_from_redis/")
async def get_from_redis(request: Request):
    item = await request.form()
    # Retrieve data from Redis based on the selection and key
    selection = item["selection"]

    # Retrieve the data from Redis using the constructed key
    result = redis_client.lrange(selection, 0, -1)
    data = []
    for record in result:
        data.append(json.loads(record))
    if data:
        return {"data": data}
    else:
        return {"message": "No data found in Redis"}


@app.get("/")
async def homepage(request: Request):
    # Calculate default values (current time and one hour back)
    now = datetime.utcnow()
    one_hour_ago = now - timedelta(hours=1)

    # Format the default values as strings for the datetime-local input
    default_start_time = one_hour_ago.strftime("%Y-%m-%dT%H:%M")
    default_end_time = now.strftime("%Y-%m-%dT%H:%M")
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "default_start_time": default_start_time,
            "default_end_time": default_end_time,
        },
    )
