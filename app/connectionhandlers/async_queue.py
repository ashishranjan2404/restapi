import logging
from asyncio import queues

logger = logging.getLogger(__name__)


def get_queue() -> queues.PriorityQueue:
    global async_queue
    return async_queue


def create():
    global async_queue
    logger.info('Creating Async Queue...')
    async_queue = queues.PriorityQueue()
