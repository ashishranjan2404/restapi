from asyncio import queues

from fastapi import APIRouter, Depends, HTTPException

from api.models import Task, StatusEnum
from connectionhandlers.async_queue import get_queue
from connectionhandlers.mongo import get_db, AsyncIOMotorClient
from connectionhandlers.redis import get_redis, aioredis

tasks = APIRouter()


@tasks.get("/")
async def get_task(
        db: AsyncIOMotorClient = Depends(get_db),
        async_queue: queues.PriorityQueue = Depends(get_queue)

):
    priority_task = await async_queue.get()
    task = await db.task.task_collection.find_one({"id": priority_task[1]})
    doc = {
        "status": StatusEnum.PROCESSING,
    }
    query = {
        "id": task["id"]
    }
    await db.task.task_collection.update_one(query, {'$set': doc})

    return str(task)


@tasks.post("/", response_model=Task, status_code=201)
async def create_item(
        task: Task,
        db: AsyncIOMotorClient = Depends(get_db),
        async_queue: queues.PriorityQueue = Depends(get_queue)

):
    await db.task.task_collection.insert_one(task.dict())
    priority = int(task.priority[1])
    await async_queue.put((priority, task.id))
    return task


@tasks.get("/{id}")
async def read_item(
        id: str,
        db: AsyncIOMotorClient = Depends(get_db)
):
    task = await db.task.task_collection.find_one({"id": id})
    if task is None:
        raise HTTPException(status_code=404, detail="Not found")
    return str(task)


@tasks.put("/{id}")
async def update_item(
        id: str,
        status: StatusEnum,
        db: AsyncIOMotorClient = Depends(get_db)
):
    doc = {"status": status}
    query = {"id": id}
    await db.task.task_collection.update_one(query, {'$set': doc})
    return {"status": status, "id": id}


async def averagetime(db, redis: aioredis.Redis):
    doc = {"status": StatusEnum.COMPLETED}
    agr = [{'$match': doc},
           {'$group': {'_id': 1, 'created': {'$avg': "$created"}}}]
    average = list(await db.task.task_collection.aggregate(agr))[0]['created']
    agr = [{'$match': doc},
           {'$group': {'_id': 1, 'last_modified': {'$avg': "$last_modified"}}}]
    average -= list(await db.task.task_collection.aggregate(agr))[0]['last_modified']
    await redis.set('average-time', average)
    return average


@tasks.get("/average_time")
async def update_item(db: AsyncIOMotorClient = Depends(get_db), redis: aioredis.Redis = Depends(get_redis)):
    cache = await redis.exists('average-time')
    if cache:
        return await redis.get('average-time', encoding='utf-8')
    return {'average_time': await averagetime(db, redis)}
