FROM python:3.13.13 AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
WORKDIR /app

# Створюємо віртуальне оточення
RUN python -m venv .venv

# Копіюємо файл залежностей та встановлюємо їх у .venv
COPY requirements.txt ./
RUN .venv/bin/pip install --no-cache-dir -r requirements.txt

# Фінальний мінімалістичний образ для запуску
FROM python:3.13.13-slim
WORKDIR /app

# Забираємо готові пакети з builder-стадії
COPY --from=builder /app/.venv .venv/
COPY . .

# CMD ["/app/.venv/bin/fastapi", "run"]
CMD ["sh", "-c", "/app/.venv/bin/alembic upgrade head && /app/.venv/bin/fastapi run"]