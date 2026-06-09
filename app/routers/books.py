from fastapi import APIRouter, HTTPException
from app.models.book import Book
from app.models.review import Review
from app.routers.reviews import reviews

router = APIRouter(prefix="/books", tags=["Books"])


books = {
    1: {"title": "Deep Work", "author": "Cal Newport"},
    2: {"title": "Atomic Habits", "author": "James Clear"},
    3: {"title": "The Pragmatic Programmer", "author": "Andrew Hunt"},
    4: {"title": "Clean Code", "author": "Robert C. Martin"},
    5: {"title": "Design Patterns", "author": "Erich Gamma"},
    6: {"title": "Thinking, Fast and Slow", "author": "Daniel Kahneman"},
    7: {"title": "The Psychology of Money", "author": "Morgan Housel"},
    8: {"title": "Zero to One", "author": "Peter Thiel"},
    9: {"title": "Sapiens", "author": "Yuval Noah Harari"},
    10: {"title": "The Lean Startup", "author": "Eric Ries"},
}

def find_max_review_id():
    max_id = 0
    for book_reviews in reviews.values():
        for review in book_reviews:
            if review["id"] > max_id:
                max_id = review["id"]
    return max_id



@router.post("/{book_id}/reviews")
async def add_review(book_id: int, review: Review):
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Book not found")
    
    if book_id not in reviews:
        reviews[book_id] = []
    new_review = {"id": find_max_review_id() + 1, "rating": review.rating, "content": review.content}
    reviews[book_id].append(new_review)
    return reviews[book_id]

@router.get("/{book_id}/reviews")
async def get_reviews(book_id: int):
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Book not found")
    return reviews.get(book_id)



@router.get("/")
async def get_books(skip: int = 0, limit: int = None): # limit refears to how many books should be returned
    if limit:
        return list(books.items())[skip : skip+limit]
    return list(books.items())[skip:]

@router.get("/{id}")
async def get_book(id: int):
    if id not in books:
        raise HTTPException(status_code=404, detail="Book not found")
    return {id: books[id]}

@router.post("/")
async def add_book(new_book: Book):
    id = max(books.keys()) + 1
    books[id] = new_book.model_dump()
    return new_book

@router.put("/{id}")
async def edit_book(id: int, book: Book):
    if id not in books.keys():
        raise HTTPException(status_code=404, detail="Book not found")
    edited_book = book.model_dump()
    books[id] = edited_book
    return {id: edited_book}
    

# @router.put("/books/{id}")
# async def add_opinion(id: int, opinion: Annotated[str, Query(max_length=50)] = "chujowa"): # opinion can reach up to 50 characters and has a default value of "chujowa"
#     book = books[id]
#     book_with_opinion = {**book, "opinion": opinion}
#     books[id] = book_with_opinion
#     return book_with_opinion
    
@router.delete("/{id}")
async def remove_book(id: int):
    if id not in books.keys():
        raise HTTPException(status_code=404, detail="Book not found")
    books.pop(id)
    return books