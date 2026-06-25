from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status
from sqlmodel import select

from app.api.dependencies import ActiveUserDep, SessionDep
from app.core.security import get_password_hash
from app.models.user import User, UserCreate, UserPublic, UserUpdate
from app.services.auth import get_user_by_username

router = APIRouter()


@router.get("/", response_model=list[UserPublic])
def read_users(
    session: SessionDep,
    current_user: ActiveUserDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):

    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users


@router.post(
    "/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED
)
def register_user(user_in: UserCreate, current_user: ActiveUserDep, db: SessionDep):
    """
    Реєстрація нового користувача з безпечним збереженням хэшу пароля в БД.
    """
    existing_user = get_user_by_username(db, username=user_in.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this username already exists.",
        )

    hashed_pwd = get_password_hash(user_in.password)

    db_user = User(
        username=user_in.username,
        email=user_in.email,
        disabled=user_in.disabled,
        hashed_password=hashed_pwd,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@router.get("/me/")
async def read_users_me(
    current_user: ActiveUserDep,
) -> User:
    return current_user


@router.get("/{user_id}", response_model=UserPublic)
def read_user(user_id: int, current_user: ActiveUserDep, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.patch("/{user_id}", response_model=UserPublic)
def update_user(
    user_id: int, user: UserUpdate, current_user: ActiveUserDep, session: SessionDep
):
    user_db = session.get(User, user_id)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    user_data = user.model_dump(exclude_unset=True)
    user_db.sqlmodel_update(user_data)
    session.add(user_db)
    session.commit()
    session.refresh(user_db)
    return user_db


@router.delete("/{user_id}")
def delete_user(user_id: int, current_user: ActiveUserDep, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    session.delete(user)
    session.commit()
    return {"ok": True}
