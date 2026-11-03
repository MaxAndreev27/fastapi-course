# FastAPI Course Application

A modern, production-ready backend application built with **FastAPI** and **SQLModel**. The project features robust JWT-based authentication, automated database migrations via **Alembic**, containerization with multi-stage **Docker** builds, persistent SQLite storage, and a complete **GitHub Actions CI/CD pipeline** targeting **Fly.io**.

## 🚀 Features

- **Robust Authentication & Authorization:** Secure OAuth2 password flow using Bearer tokens and secure password hashing.
- **Database & Migrations:** Integrated with **SQLModel** (SQLAlchemy + Pydantic) and **Alembic** for smooth database evolutionary tracks.
- **Data Persistence:** Ready for cloud deployment using a persistent volume mount for SQLite (`/data/database.sqlite3`).
- **Data Seeding:** Automatically seeds default administrative and regional roles (`admin`, `editor`, `user`) during initial migrations.
- **Multi-Stage Dockerization:** Highly optimized Docker images separating build environments from runtime to keep images lightweight and secure.
- **CI/CD Pipeline:** Fully automated workflow that enforces testing quality gates (`pytest` + `alembic` setup) before promoting code to production.

## 🛠️ Tech Stack

- **Language:** Python 3.12+
- **Package Manager:** uv
- **Framework:** FastAPI
- **ORM/Database Layer:** SQLModel / SQLAlchemy
- **Database:** SQLite (with WAL/persistence configuration)
- **Migrations:** Alembic
- **Configuration & Validation:** Pydantic / Pydantic Settings
- **Testing:** Pytest & FastAPI TestClient
- **Containerization:** Docker (Multi-stage slim build)
- **Cloud Hosting:** Fly.io
- **CI/CD:** GitHub Actions

---

## 💻 Local Development Setup

### 1. Prerequisites

Install [uv](https://docs.astral.sh/uv/). It will provision Python 3.12+ automatically if needed.

### 2. Clone and Environment Setup

Clone the repository and navigate into the project directory:

```bash
git clone <your-repository-url>
cd fastapi-course
```

### 3. Install Dependencies

```bash
uv sync
```

### 4. Configure and Run

Set `SECRET_KEY` (and optionally `DATABASE_URL`) in your environment or `.env` file, then:

```bash
uv run alembic upgrade head
uv run fastapi dev
uv run pytest
```
