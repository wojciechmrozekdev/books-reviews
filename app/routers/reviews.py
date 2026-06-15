from fastapi import APIRouter, HTTPException, Depends

from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database.dependencies import get_db

from app.models.review import Review

from app.schemas.reviews import ReviewResponse, ReviewUpdate

router = APIRouter(prefix="/review", tags=["Rewiews"])



@router.put("/{id}")
async def edit_review(id: int, edited_review: ReviewUpdate, db: Session = Depends(get_db)):
    review = db.get(Review, id)
    
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    
    review.rating = edited_review.rating
    review.content = edited_review.content
    
    db.commit()
    db.refresh(review)
    
    return review

@router.delete("/{id}")
async def delete_review(id: int, db: Session = Depends(get_db)):
    review = db.get(Review, id)
    
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    
    db.delete(review)
    db.commit()
    
    return review