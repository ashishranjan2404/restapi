from datetime import datetime
from enum import Enum
from uuid import uuid4

import pydantic


class Item(pydantic.BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None


class StatusEnum(str, Enum):
    IDLE = 'idle'
    PROCESSING = 'processing'
    COMPLETED = 'completed'
    FAILED = 'failed'


class Priority(str, Enum):
    p1 = 'p1'
    p2 = 'p2'
    p3 = 'p3'


class Task(pydantic.BaseModel):
    name: str = None
    submitter: str
    status: StatusEnum = StatusEnum.IDLE
    created: int = None
    last_modified: int = None
    id: str = None
    priority: Priority = Priority.p1

    @pydantic.validator('created', pre=True, always=True)
    def default_ts(cls, v):
        return v or (datetime.utcnow() - datetime(1970, 1, 1)).total_seconds()

    @pydantic.validator('id', pre=True, always=True)
    def set_id(cls, v):
        return v or str(uuid4())

    @pydantic.validator('last_modified', pre=True, always=True)
    def default_ts_modified(cls, v, *, values, **kwargs):
        return v or values['created']
