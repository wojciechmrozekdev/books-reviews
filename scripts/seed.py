from faker import Faker
import random

from app.database.database import SessionLocal
from app.models.book import Book
from app.models.review import Review

comments = [
    "Excellent book",
    "Very useful",
    "Highly recommended",
    "Not bad",
    "Could be better",
    "Amazing insights",
    "Must read",
    "Too repetitive"
]

fake = Faker()

db = SessionLocal()

# for _ in range(30):
#     book = Book(
#         title=fake.sentence(nb_words=3),
#         author=fake.name(),
#         year=fake.random_int(1950, 2025)
#     )

#     db.add(book)

from faker import Faker

from app.database.database import SessionLocal

from app.models.book import Book
from app.models.review import Review

fake = Faker()

db = SessionLocal()

books = db.query(Book).all()

for book in books:

    review_count = fake.random_int(min=0, max=5)

    for _ in range(review_count):

        review = Review(
            rating=fake.random_int(min=1, max=5),
            content=random.choice(comments),
            book_id=book.id
        )

        db.add(review)

db.commit()

print("Reviews added")
