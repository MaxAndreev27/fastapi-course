from sqlmodel import Field, SQLModel


# Спільні поля для користувача (і для запитів, і для бази)
class UserBase(SQLModel):
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    disabled: bool = False


# Схема, яку надсилає клієнт при реєстрації (тут потрібен пароль)
class UserCreate(UserBase):
    password: str


# Схема, яку ми повертаємо клієнту (БЕЗ пароля із бази)
class UserPublic(UserBase):
    id: int | None = None


# Таблиця в базі даних
class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str


class UserUpdate(SQLModel):
    username: str | None = None
    email: str | None = None
    disabled: bool | None = None
    password: str | None = None
