from fastapi import APIRouter, HTTPException
from app.schemas.book import BookCreate
from app.schemas.reviews import Review

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.models.book import Book
from app.schemas.book import BookCreate


router = APIRouter(prefix="/books", tags=["Books"])


@router.post("/")
async def create_book(book: BookCreate, db: Session = Depends(get_db)):
    new_book = Book(
        title = book.title,
        author = book.author
    )
    
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    
    return new_book

@router.get("/")
async def get_books(db: Session = Depends(get_db)):
    return db.query(Book).all()

@router.get("/{id}")
async def get_book(id: int, db: Session = Depends(get_db)):
    book = db.get(Book, id) # .get() method works only if one want to filter by primary keys, if one wants to do same more complex filtering, then you need to use .select() method
    
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    return book

