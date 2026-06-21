from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.user import User
from app.schemas.user import UserCreate

from app.core.security import hash_password, verify_password


class InvalidCredentialsError(Exception):
    pass


def create_user(
    db: Session,
    user_data: UserCreate
):
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_password(user_data.password)
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


def authenticate_user(
    db: Session,
    email: str,
    password: str
):
    stmt = select(User).where(User.email == email)

    user = db.execute(stmt).scalar_one_or_none()

    if user is None:
        raise InvalidCredentialsError()

    if not verify_password(
        password,
        user.hashed_password
    ):
        raise InvalidCredentialsError()

    return user

