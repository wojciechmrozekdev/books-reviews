from pydantic import BaseModel

class ReviewCreate(BaseModel):
    rating: int
    content: str
    
class ReviewUpdate(BaseModel):
    rating: int
    content: str
    
class ReviewResponse(BaseModel):
    id: int
    rating: int
    content: str