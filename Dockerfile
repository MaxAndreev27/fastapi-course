FROM python:3.12-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:0.13 /uv /usr/local/bin/uv

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never
WORKDIR /app

# Встановлюємо залежності з uv.lock у .venv (без коду проєкту та dev-групи)
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# Фінальний мінімалістичний образ для запуску
FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
WORKDIR /app

# Забираємо готові пакети з builder-стадії
COPY --from=builder /app/.venv .venv/
COPY . .

CMD ["sh", "-c", "/app/.venv/bin/alembic upgrade head && /app/.venv/bin/fastapi run"]
