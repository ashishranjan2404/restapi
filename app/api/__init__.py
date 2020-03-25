from fastapi import APIRouter

from .tasks import tasks as task_router

router = APIRouter()

router.include_router(task_router, prefix="/tasks", tags=["tasks"])
