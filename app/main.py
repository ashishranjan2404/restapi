from fastapi import FastAPI
from pydantic import BaseModel
import asyncio

app = FastAPI()


class (BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None


command = []


@app.get("/")
async def root():
    return "Hello World"


async def return_command():
    while not command:
        asyncio.sleep(.3)
    return command.pop(0)


@app.get("/get_command/")
async def get_command():
    res = asyncio.wait([return_command()])
    return {"command": res}


@app.get("/send_command/")
async def send_command_item():
    command.append("reboot")
    return {"command": ""}


@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item, q: str = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result
