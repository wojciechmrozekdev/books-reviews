from fastapi import APIRouter, HTTPException, Depends

from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.models.review import Review

from app.schemas.reviews import ReviewUpdate

from app.services import review_service


router = APIRouter(prefix="/review", tags=["Rewiews"])



@router.put("/{id}")
async def edit_review(id: int, edited_review: ReviewUpdate, db: Session = Depends(get_db)):
    
    return review_service.edit_review(db, id, edited_review)

@router.delete("/{id}")
async def delete_review(id: int, db: Session = Depends(get_db)):

    return review_service.delete_review(db, id)