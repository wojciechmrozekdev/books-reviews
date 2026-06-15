from fastapi import FastAPI
import uvicorn

from app.database.database import engine, Base
from app.models.book import Book

from app.routers.books import router as books_router

from app.routers.reviews import router as reviews_router

print(Base.metadata.tables.keys())
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(books_router)
app.include_router(reviews_router)