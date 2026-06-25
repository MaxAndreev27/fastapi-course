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
    hashed_password = get_password_hash("secret")

    bind = op.get_bind()

    # 2. Інструкція для вставки нових користувачів (якщо база чиста)
    stmt_insert = sa.text("""
        INSERT OR IGNORE INTO user (username, email, hashed_password, disabled)
        VALUES (:username, :email, :hashed_password, :disabled)
    """)

    # 3. Інструкція для примусового оновлення пароля (якщо користувач уже був створений)
    stmt_update = sa.text("""
        UPDATE user 
        SET hashed_password = :hashed_password, email = :email, disabled = :disabled
        WHERE username = :username
    """)

    users_data = [
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
    ]

    # Виконуємо обидві операції для кожного користувача
    for user in users_data:
        bind.execute(stmt_insert, user)
        bind.execute(stmt_update, user)


def downgrade() -> None:
    # Очищення бази у разі відкату міграції
    op.execute("DELETE FROM user WHERE username = 'admin'")
    op.execute("DELETE FROM user WHERE username = 'editor'")
    op.execute("DELETE FROM user WHERE username = 'user'")
