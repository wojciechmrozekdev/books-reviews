from sqlalchemy.orm import Session
from sqlalchemy import select, func

from app.models.book import Book
from app.models.review import Review

from app.services.book_service import get_book_or_raise
from app.services.review_service import NoReviewsError

class NoStatsDataError(Exception):
    pass


def get_book_avg_rating(db: Session, book_id: int):
    book = get_book_or_raise(db, book_id)

    stmt = (
        select(func.avg(Review.rating))
        .where(Review.book_id == book_id)
    )

    avg_rating = db.execute(stmt).scalar()

    if avg_rating is None:
        raise NoReviewsError()

    return {
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "year": book.year,
        "average_rating": float(avg_rating)
    }

def get_book_with_reviews(db: Session, book_id: int):
    book = get_book_or_raise(db, book_id)

    return book  # dzięki relationship SQLAlchemy + Pydantic

def count_reviews_for_book(db: Session, book_id: int) -> int:
    get_book_or_raise(db, book_id)

    stmt = (
        select(func.count(Review.id))
        .where(Review.book_id == book_id)
    )

    return db.execute(stmt).scalar()

def get_top_books_by_rating(db: Session, limit: int = 5):
    stmt = (
        select(
            Book,
            func.avg(Review.rating).label("avg_rating")
        )
        .join(Review, Review.book_id == Book.id)
        .group_by(Book.id)
        .order_by(func.avg(Review.rating).desc())
        .limit(limit)
    )

    result = db.execute(stmt).all()

    return [
        {
            "id": row.Book.id,
            "title": row.Book.title,
            "author": row.Book.author,
            "year": row.Book.year,
            "average_rating": round(float(row.avg_rating),2)
        }
        for row in result
    ]