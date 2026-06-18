from sqlalchemy.orm import Session
from sqlalchemy import select

from app.services.book_service import get_book_or_raise

from app.models.review import Review

from app.schemas.reviews import ReviewUpdate, ReviewCreate

class ReviewNotFoundError(Exception):
    pass

class NoReviewsError(Exception):
    pass


def create_review(
    db: Session,
    book_id: int,
    review: ReviewCreate
):
    book = get_book_or_raise(db, book_id)
    
    new_review = Review(
        rating = review.rating,
        content = review.content,
        book_id = book_id
    )
    
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    
    return new_review

def get_reviews(
    db: Session,
    book_id: int
):
    stmt = select(Review).where(Review.book_id == book_id)
    
    result = db.execute(stmt).scalars().all()
    
    if not result:
        raise NoReviewsError()
    
    return result

def edit_review(db: Session, id: int, edited_review: ReviewUpdate):
    review = db.get(Review, id)

    if review is None:
        raise ReviewNotFoundError()

    review.rating = edited_review.rating
    review.content = edited_review.content
    
    return review

def delete_review(db: Session, id: int):
    review = db.get(Review, id)

    if review is None:
        raise ReviewNotFoundError()

    db.delete(review)
    db.commit()
    return review