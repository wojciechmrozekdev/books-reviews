from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.database import Base


class Book(Base):
    __tablename__ = "books"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    author: Mapped[str]

    reviews: Mapped[list["Review"]] = relationship(
        back_populates="book"
    )
    