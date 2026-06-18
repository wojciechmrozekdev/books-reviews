from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Annotated

from sqlalchemy.orm import Session
from sqlalchemy import select, func

from app.database.dependencies import get_db

from app.schemas.book import BookCreate, BookUpdate, BookResponse, BookResponseAvgRating, BookWithReviewsResponse, TopBookResponse
from app.schemas.reviews import ReviewCreate, ReviewResponse

from app.services import book_service, review_service, stats_service

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("/top-rated", response_model=list[TopBookResponse])
async def get_top_books(
    limit: Annotated[int, Query(ge=1, le=100)] = 5,
    db: Session = Depends(get_db)
):
    return stats_service.get_top_books_by_rating(db, limit)
    
@router.get("/{id}/details", response_model=BookWithReviewsResponse)
async def get_book_with_reviews(id: int, db: Session = Depends(get_db)):
    try:
        return stats_service.get_book_with_reviews(db, id)
    
    except book_service.BookNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )
        
@router.get("/{id}/avg-rating", response_model=BookResponseAvgRating)
async def get_book_avg_rating(id: int, db: Session = Depends(get_db)):
    try:
        return stats_service.get_book_avg_rating(db, id)
    
    except book_service.BookNotFoundError:
        raise HTTPException(status_code=404, detail="Book not found")
    
    except review_service.NoReviewsError:
        raise HTTPException(status_code=404, detail="No reviews found")

@router.post("/{book_id}/review", response_model=ReviewResponse)
async def create_review(book_id: int, review: ReviewCreate, db: Session = Depends(get_db)):
    
    try: 
        return review_service.create_review(db, book_id, review)
    
    except book_service.BookNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

@router.get("/{book_id}/reviews", response_model=list[ReviewResponse])
async def get_reviews(book_id: int, db: Session = Depends(get_db)):
    
    try:
        return review_service.get_reviews(db, book_id)
    
    except book_service.BookNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    except review_service.ReviewNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Reviews not found"
        )

@router.post("/")
async def create_book(book: BookCreate, db: Session = Depends(get_db)):
   return book_service.create_book(db, book)

@router.get("/", response_model=list[BookResponse])
async def get_books(
    title: Annotated[str | None, Query(max_length=50)] = None,
    author: Annotated[str | None, Query(max_length=50)] = None,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
    sort: Annotated[str | None, Query()] = None,
    db: Session = Depends(get_db)
):
    
   return book_service.get_books(
       db=db,
       title=title,
       author=author,
       skip=skip,
       limit=limit,
       sort=sort
   )

@router.get("/{id}", response_model=BookResponse)
async def get_book(id: int, db: Session = Depends(get_db)):
    
    try:
        book = book_service.get_book(db, id)
        
    except book_service.BookNotFoundError:
        raise HTTPException(status_code=404, detail="Book not found")
    
    return book

@router.delete("/{id}", response_model=BookResponse)
async def delete_book(id: int, db: Session = Depends(get_db)):
    
    try:
        return book_service.delete_book(db, id)
    
    except book_service.BookNotFoundError:
        raise HTTPException(status_code=404, detail="Book not found")

@router.put("/{id}", response_model=BookResponse)
async def edit_book(id: int, edited_book: BookUpdate, db: Session = Depends(get_db)):
    
    try:
        return book_service.edit_book(db, id, edited_book)
    
    except book_service.BookNotFoundError:
        raise HTTPException(status_code=404, detail="Book not found")
    
    