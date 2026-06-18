from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate

from sqlalchemy.orm import Session
from sqlalchemy import select, func

class BookNotFoundError(Exception):
    pass

class NoReviewsError(Exception):
    pass


def get_book_or_raise(db: Session, id: int) -> Book:
    book = db.get(Book, id)
    if not book:
        raise BookNotFoundError()
    return book


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

def get_books(
    db: Session,
    title: str | None,
    author: str | None,
    skip: int,
    limit: int,
    sort: str | None
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
    
def get_book(
    db: Session,
    id: int
):
    book = get_book_or_raise(db, id)

    return book   
    
def delete_book(
    db: Session,
    book_id: int
):
    book = get_book_or_raise(db, book_id)
    
    db.delete(book)
    db.commit()
    
    return book

def edit_book(
    db: Session,
    id: int, 
    edited_book: BookUpdate
):
    book = get_book_or_raise(db, id)
    
    book.title = edited_book.title
    book.author = edited_book.author
    book.year = edited_book.year
    
    db.commit()
    db.refresh(book)
    
    return book
