from fastapi import APIRouter, HTTPException, Depends, Query

from sqlalchemy.orm import Session
from sqlalchemy import select, func

from app.database.dependencies import get_db

from app.models.book import Book
from app.models.review import Review

from app.schemas.book import BookCreate, BookUpdate, BookResponse, BookResponseAvgRating
from app.schemas.reviews import ReviewCreate, ReviewResponse

from typing import Annotated

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("/{id}/avg-rating", response_model=BookResponseAvgRating)
async def get_book_avg_rating(id: int, db: Session = Depends(get_db)):
    book = db.get(Book, id)

    if book is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )
    
    stmt = select(func.avg(Review.rating)).where(Review.book_id == id)
    avg_rating = db.execute(stmt).scalar()
    
    book_avg_rating = BookResponseAvgRating(
        id = book.id,
        title = book.title,
        author = book.author,
        average_rating = avg_rating
    )
    
    return book_avg_rating
    
@router.get("/title", response_model=list[BookResponse])
async def get_books_by_title(title: str, db: Session = Depends(get_db)):
    stmt = select(Book).where(Book.title.ilike(f"%{title}%"))
    return db.execute(stmt).scalars().all()

@router.get("/author", response_model=list[BookResponse])
async def get_books_by_author(author: str, db: Session = Depends(get_db)):
    stmt = select(Book).where(Book.author.ilike(f"%{author}%"))
    return db.execute(stmt).scalars().all()

@router.post("/{book_id}/review", response_model=ReviewResponse)
async def create_review(book_id: int, review: ReviewCreate, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)

    if book is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )
    
    new_review = Review(
        rating = review.rating,
        content = review.content,
        book_id = book_id
    )
    
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    
    return new_review

@router.get("/{book_id}/reviews", response_model=list[ReviewResponse])
async def get_reviews(book_id: int, db: Session = Depends(get_db)):
    
    stmt = select(Review).where(Review.book_id == book_id)

    result = db.execute(stmt)
    reviews = result.scalars().all()
    
    # for review in reviews:
    #     print(review.rating)
    #     print(review.content)
    #     print("----------")
    
    return reviews

@router.post("/", response_model=BookResponse)
async def create_book(book: BookCreate, db: Session = Depends(get_db)):
    new_book = Book(
        title = book.title,
        author = book.author
    )
    
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    
    return new_book

@router.get("/", response_model=list[BookResponse])
async def get_books(
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
    db: Session = Depends(get_db)
):
    
    stmt = (
        select(Book)
        .offset(skip)
        .limit(limit)
    )
    
    return db.execute(stmt).scalars().all()


@router.get("/{id}", response_model=BookResponse)
async def get_book(id: int, db: Session = Depends(get_db)):
    book = db.get(Book, id) 
    
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    return book

@router.delete("/{id}", response_model=BookResponse)
async def delete_book(id: int, db: Session = Depends(get_db)):
    book = db.get(Book, id)
    
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    db.delete(book)
    db.commit()
    
    return book

@router.put("/{id}", response_model=BookResponse)
async def edit_book(id: int, edited_book: BookUpdate, db: Session = Depends(get_db)):
    book = db.get(Book, id)
    
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    book.title = edited_book.title
    book.author = edited_book.author
    
    db.commit()
    db.refresh(book)
    
    return book
    
    