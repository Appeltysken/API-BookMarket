from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import ForeignKey, DECIMAL
from app.database import Base, int_pk, str_null_true, int_null_true
from app.entities.users.models import User
from decimal import Decimal
from app.entities.authors.models import Author

class Book(Base):
    __tablename__ = 'books'
    
    
    id: Mapped[int_pk]
    name: Mapped[str]
    author_id: Mapped[int_null_true | None] = mapped_column(ForeignKey("authors.id"), default=None)
    genre: Mapped[str_null_true | None]
    publisher: Mapped[str_null_true]
    description: Mapped[str_null_true]
    price: Mapped[Decimal] = mapped_column(DECIMAL(precision=10, scale=2))
    book_picture: Mapped[str | None]
    user_id: Mapped[int_null_true] = mapped_column(ForeignKey("users.id"), nullable=True)
    
    
    orders: Mapped["Order"] = relationship("Order", back_populates="books")
    authors: Mapped["Author"] = relationship("Author", back_populates="books")
    users: Mapped["User"] = relationship("User", back_populates="books")
    reviews: Mapped["Review"] = relationship("Review", back_populates="books")
    
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "id_author": self.author_id,
            "genre": self.genre,
            "publisher": self.publisher,
            "description": self.description,
            "price": self.price,
            "book_picture": self.book_picture,
            "user_id": self.user_id
        }
        
    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id})"

    def __repr__(self):
        return str(self)