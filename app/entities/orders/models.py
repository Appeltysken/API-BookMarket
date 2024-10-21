from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import ForeignKey,  text
from app.database import Base, int_pk, int_null_true
from app.entities.users.models import User
from typing import List
from app.entities.books.models import Book

class Order(Base):
    __tablename__ = 'orders'
    
    id: Mapped[int_pk]
    status: Mapped[str] = mapped_column(server_default=text("'Ожидает обработки'"))
    price: Mapped[int_null_true]
    user_id: Mapped[int_null_true] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    books_id: Mapped[int_null_true] = mapped_column(ForeignKey("books.id"), nullable=True)
    
    user: Mapped["User"] = relationship("User", back_populates="orders")
    books: Mapped[List["Book"]] = relationship("Book", back_populates="orders")
    
    def to_dict(self):
        return {
            "id": self.id,
            "status": self.status,
            "price": self.price,
            "user_id": self.user_id,
            "books_id": self.books_id
        }
        
    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id})"

    def __repr__(self):
        return str(self)