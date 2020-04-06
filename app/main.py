# from api.kafka_consumers import tasks_consumer_callback
# from connectionhandlers import kafka_handler
import os

from fastapi import FastAPI

from api import router as api_router
from connectionhandlers import async_queue
from connectionhandlers import mongo
from connectionhandlers import redis

app = FastAPI(
    title=os.getenv("SERVICE_NAME", "webapi"),
    description="tasks",
    debug=os.getenv("DEBUG", False),
    version=os.getenv("VERSION", "1.0.0")
)

app.include_router(api_router)


@app.on_event("startup")
def startup_event():
    mongo.connect()
    redis.connect()
    async_queue.create()


@app.on_event("shutdown")
def shutdown_event():
    mongo.disconnect()
    redis.disconnect()
