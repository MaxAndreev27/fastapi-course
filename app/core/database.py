from sqlmodel import SQLModel, create_engine

from app.core.config import settings

database_url = settings.DATABASE_URL

engine = create_engine(
    database_url,
    echo=True,
    connect_args={"check_same_thread": False},
)


def init_db():
    SQLModel.metadata.create_all(engine)
