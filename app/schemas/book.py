from pydantic import BaseModel

class BookCreate(BaseModel):
    title: str
    author: str
    
class BookUpdate(BaseModel):
    title: str
    author: str
    
class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    
    model_config = {
        "from_attributes": True
    }