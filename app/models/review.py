from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.database import Base

from sqlalchemy import ForeignKey

class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True)

    rating: Mapped[int]
    content: Mapped[str]

    book_id: Mapped[int] = mapped_column(
        ForeignKey("books.id")
    )
    
    book: Mapped["Book"] = relationship(
    back_populates="reviews"
)

