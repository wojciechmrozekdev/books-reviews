from datetime import datetime, timedelta, UTC

from typing import Annotated
from app.database.dependencies import get_db

from sqlalchemy.orm import Session

import jwt
from jwt import InvalidTokenError

from pwdlib import PasswordHash

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException

from app.models.user import User

password_hash = PasswordHash.recommended()

SECRET_KEY = "super_secret_key"  # później przeniesiesz do .env
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None
) -> str:
    to_encode = data.copy()

    expire = datetime.now(UTC) + (
        expires_delta or timedelta(minutes=30)
    )

    to_encode.update(
        {
            "exp": expire
        }
    )

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    print(encoded_jwt)
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )

    return payload

def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)]
):
    try:
        payload = decode_access_token(token)

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        user = db.get(User, int(user_id))

        if user is None:
            raise HTTPException(
                status_code=401,
                detail="User not found"
            )

        return user

    except InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )