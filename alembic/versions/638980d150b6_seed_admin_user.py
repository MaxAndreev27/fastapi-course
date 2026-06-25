"""seed admin user

Revision ID: 638980d150b6
Revises: 46e99e31e85e
Create Date: 2026-06-25 15:05:17.859109

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op
from app.core.security import get_password_hash

# revision identifiers, used by Alembic.
revision: str = "638980d150b6"
down_revision: Union[str, Sequence[str], None] = "46e99e31e85e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Створюємо безпечний хеш пароля під час виконання міграції
    # Обов'язково зміни пароль 'admin_password' на свій або зчитуй з env змінних!
    hashed_password = get_password_hash("secret")

    # 2. Описуємо структуру таблиці на рівні SQLAlchemy Core (щоб не залежити від змін у SQLModel-класах у майбутньому)
    user_table = sa.table(
        "user",
        sa.column("id", sa.Integer),
        sa.column("username", sa.String),
        sa.column("email", sa.String),
        sa.column("hashed_password", sa.String),
        sa.column("disabled", sa.Boolean),
    )

    # 3. Вставляємо запис адміна в БД
    op.bulk_insert(
        user_table,
        [
            {
                "username": "admin",
                "email": "admin@mail.com",
                "hashed_password": hashed_password,
                "disabled": False,
            },
            {
                "username": "editor",
                "email": "editor@mail.com",
                "hashed_password": hashed_password,
                "disabled": False,
            },
            {
                "username": "user",
                "email": "user@mail.com",
                "hashed_password": hashed_password,
                "disabled": False,
            },
        ],
    )


def downgrade() -> None:
    # Очищення бази у разі відкату міграції
    op.execute("DELETE FROM user WHERE username = 'admin'")
    op.execute("DELETE FROM user WHERE username = 'editor'")
    op.execute("DELETE FROM user WHERE username = 'user'")
