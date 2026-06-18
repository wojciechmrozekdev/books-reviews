from pydantic import BaseModel
from app.schemas.reviews import ReviewResponse

class BookCreate(BaseModel):
    title: str
    author: str
    year: int
    
class BookUpdate(BaseModel):
    title: str
    author: str
    year: int
    
class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    year: int
    
    model_config = {
        "from_attributes": True
    }
    
class TopBookResponse(BaseModel):
    id: int
    title: str
    author: str
    year: int
    average_rating: float
    
    model_config = {
        "from_attributes": True
    }
    
class BookWithReviewsResponse(BaseModel):
    id: int
    title: str
    author: str
    year: int
    reviews: list[ReviewResponse]
    
    model_config = {
        "from_attributes": True
    }

class BookResponseAvgRating(BaseModel):
    id: int
    title: str
    author: str
    year: int
    average_rating: float
    
    model_config = {
        "from_attributes": True
    }