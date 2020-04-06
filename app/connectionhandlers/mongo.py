import logging
import os

from motor.motor_asyncio import AsyncIOMotorClient

logger = logging.getLogger(__name__)


def get_db() -> AsyncIOMotorClient:
    global client
    return client


def connect():
    global client
    logger.info('AwesomeDB connection opening...')
    client = AsyncIOMotorClient(os.getenv('MONGODB_URL',
                                          "mongodb://awesomedb:27017/task"))


def disconnect():
    global client
    logger.info('AwesomeDB connection closing...')
    client.close()
