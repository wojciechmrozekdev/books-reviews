from app.models.book import Book
from app.schemas.book import BookCreate

from sqlalchemy.orm import Session
from sqlalchemy import select, func

class BookNotFoundError(Exception):
    pass

def get_books(
    db: Session,
    title: str | None,
    author: str | None,
    skip: int,
    limit: int,
    sort: str
):
    stmt = select(Book)
    
    if author:
        stmt = stmt.where(
            Book.author.ilike(f"%{author}%")
        )

    if title:
        stmt = stmt.where(
            Book.title.ilike(f"%{title}%")
        )

    if sort == "title":
        stmt = stmt.order_by(Book.title)

    elif sort == "author":
        stmt = stmt.order_by(Book.author)

    elif sort == "id":
        stmt = stmt.order_by(Book.id)

    
    stmt = stmt.offset(skip).limit(limit)
    
    return db.execute(stmt).scalars().all()
    

def create_book(
    db: Session,
    book_data: BookCreate
):
    book = Book(
        title = book_data.title,
        author = book_data.author,
        year = book_data.year
    )
    
    db.add(book)
    db.commit()
    db.refresh(book)
    
    return book

def delete_book(
    db: Session,
    book_id: int
):
    book = db.get(Book, book_id)
    
    if book is None:
        raise BookNotFoundError()
    
    db.delete(book)
    db.commit()
    
    return book

def get_book(
    
):
    pass
    