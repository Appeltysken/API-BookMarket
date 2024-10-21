from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import ForeignKey
from app.database import Base, int_pk, int_null_true, str_null_true
from app.entities.books.models import Book
from app.entities.users.models import User

class Review(Base):
    __tablename__ = 'reviews'
    
    id: Mapped[int_pk]
    text: Mapped[str_null_true | None]
    mark: Mapped[int]
    user_id: Mapped[int_null_true] = mapped_column(ForeignKey("users.id"), nullable=True)
    book_id: Mapped[int_null_true] = mapped_column(ForeignKey("books.id"), nullable=True)
    
    users: Mapped["User"] = relationship("User", back_populates="reviews")
    books: Mapped["Book"] = relationship("Book", back_populates="reviews")
    
    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "mark": self.mark,
            "user_id": self.user_id,
            "book_id": self.book_id
        }
        
    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id})"

    def __repr__(self):
        return str(self)