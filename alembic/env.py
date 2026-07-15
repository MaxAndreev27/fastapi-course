import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from sqlmodel import SQLModel

from alembic import context

from app.models.user import User
from app.models.hero import Hero

config = context.config


# 1. Створюємо динамічну функцію отримання URL бази даних
def get_url() -> str:
    # 1. Спершу шукаємо у змінних оточення (для Fly.io)
    url = os.getenv("DATABASE_URL")
    if url:
        return url

    # 2. Якщо там немає, беремо з alembic.ini (для локальної розробки)
    alembic_url = config.get_main_option("sqlalchemy.url")
    if alembic_url:
        return alembic_url

    # 3. Якщо і там порожньо, повертаємо дефолтний шлях, щоб тип завжди був str
    return "sqlite:///./database.sqlite3"


if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = SQLModel.metadata


def run_migrations_offline() -> None:
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    # 2. Витягуємо параметри секції [alembic] та примусово перезаписуємо sqlalchemy.url
    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = get_url()

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
