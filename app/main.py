from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.routing import APIRoute

from app.api.dependencies import get_settings
from app.api.v1.router import v1_router
from app.core.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🤖 Запуск init_db()...")
    init_db()
    yield


def custom_generate_unique_id(route: APIRoute):
    # Беремо перший тег роутера та ім'я функції ендпоінту
    tag = route.tags[0] if route.tags else "default"
    return f"{tag}-{route.name}"


app = FastAPI(
    title=get_settings().PROJECT_NAME,
    lifespan=lifespan,
    generate_unique_id_function=custom_generate_unique_id,
)

app.include_router(v1_router, prefix="/api/v1")
