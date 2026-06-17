from fastapi import FastAPI
import uvicorn

from app.models.book import Book

from app.routers.books import router as books_router

from app.routers.reviews import router as reviews_router


app = FastAPI()

app.include_router(books_router)
app.include_router(reviews_router)