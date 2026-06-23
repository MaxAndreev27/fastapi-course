from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, Path, Query, status
from pydantic import BaseModel

from app.api.dependencies import SettingsDep, get_settings
from app.api.v1.auth import router as auth_router
from app.api.v1.heroes import router as heroes_router
from app.api.v1.users import router as users_router
from app.core.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🤖 Запуск init_db()...")
    init_db()
    yield


app = FastAPI(title=get_settings().PROJECT_NAME, lifespan=lifespan)

# Підключаємо наші модулі авторизації та користувачів
app.include_router(auth_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
app.include_router(heroes_router, prefix="/api/v1")


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


@app.put("/items/{item_id}", status_code=status.HTTP_201_CREATED)
def update_item(item_id: int, item: Item) -> Item:
    # return {"item_name": item.name, "item_id": item_id}
    return item


@app.get("/info")
async def get_info(settings: SettingsDep):
    return {
        "project_name": settings.PROJECT_NAME,
        "debug": settings.DEBUG,
        "api_port": settings.API_PORT,
        "database_url": settings.DATABASE_URL,
    }
