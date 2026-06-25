from sqlmodel import Session, select

from app.core.security import DUMMY_HASH, verify_password
from app.models.user import User


def get_user_by_username(db: Session, username: str) -> User | None:
    """Шукає користувача в реальній базі даних за його username."""
    statement = select(User).where(User.username == username)
    return db.exec(statement).first()


def authenticate_user(db: Session, username: str, password: str) -> User | None:
    """
    Перевіряє пароль користувача.
    Повертає об'єкт User, якщо все добре, або False, якщо авторизація провалена.
    """
    # 1. Шукаємо користувача в реальній БД замість fake_db
    user = get_user_by_username(db, username)

    # 2. Якщо користувача немає — запускаємо фейкову перевірку (захист від Timing Attacks)
    if not user:
        verify_password(password, DUMMY_HASH)
        return None

    # 3. Перевіряємо реальний хеш пароля з бази даних
    if not verify_password(password, user.hashed_password):
        return None

    return user
