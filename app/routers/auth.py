from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from typing import Annotated

from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.services import auth_service
from app.schemas.user import UserCreate, UserLogin, Token, UserResponse

from  app.core.security import create_access_token, get_current_user

from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/")
async def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    return auth_service.create_user(db=db, user_data=user)

@router.post("/login", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm,  Depends()],
    db: Annotated[Session, Depends(get_db)]
):
    try:
        user = auth_service.authenticate_user(
            db,
            form_data.username,
            form_data.password
        )
        
        token = create_access_token(
            {
                "sub": str(user.id)
            }
        )

        return {
            "access_token": token,
            "token_type": "bearer"
        }

    except auth_service.InvalidCredentialsError:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )
        
@router.get("/me", response_model=UserResponse)
async def me(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return current_user