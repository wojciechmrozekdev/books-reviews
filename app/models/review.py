from pydantic import BaseModel

class Review(BaseModel):
    rating: int
    content: str