from typing import Annotated

from fastapi import FastAPI, Path, Query
from pydantic import BaseModel

from app.core.config import settings

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None


@app.get("/")
async def root():
    return {"Hello World"}


@app.get("/items/{item_id}")
async def read_item(
    item_id: Annotated[int, Path(title="The ID of the item to get")],
    q: Annotated[str | None, Query(max_length=50)] = None,
):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


@app.get("/info")
async def get_info():
    return {
        "project_name": settings.PROJECT_NAME,
        "debug": settings.DEBUG,
        "api_port": settings.API_PORT,
    }
