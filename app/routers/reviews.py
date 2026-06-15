from fastapi import APIRouter, HTTPException, Depends

from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database.dependencies import get_db

from app.models.review import Review

from app.schemas.reviews import ReviewResponse, ReviewUpdate

router = APIRouter(prefix="/review", tags=["Rewiews"])



# @router.put("/{id}")
# async def edit_review(id: int, edited_review: Review)