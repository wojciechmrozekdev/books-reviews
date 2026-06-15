from fastapi import APIRouter, HTTPException, Depends

from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database.dependencies import get_db

from app.models.book import Book
from app.models.review import Review

from app.schemas.book import BookCreate, BookUpdate, BookResponse
from app.schemas.reviews import ReviewCreate, ReviewResponse

router = APIRouter(prefix="/books", tags=["Books"])


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
    
    stmt = select(Review).join(Book).where(Book.id == book_id)

    result = db.execute(stmt)
    return result.scalars().all()

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
async def get_books(db: Session = Depends(get_db)):
    stmt = select(Book)
    result = db.execute(stmt)
    return result.scalars().all()


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
    
    