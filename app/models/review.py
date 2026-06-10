from sqlalchemy.orm import Mapped, mapped_column
from app.database.database import Base

class Review(Base):
    __tablename__ = "reviews"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    rating: Mapped[int]
    content: Mapped[str]