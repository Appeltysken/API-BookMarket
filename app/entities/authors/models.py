from sqlalchemy.orm import Mapped, relationship
from typing import List
from app.database import Base, int_pk, str_null_true

class Author(Base):
    __tablename__ = 'authors'
    
    id: Mapped[int_pk]
    name: Mapped[str_null_true]
    bio: Mapped[str_null_true]
    author_picture: Mapped[str | None]

    books: Mapped[List["Book"]] = relationship("Book", back_populates="authors")
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "bio": self.bio,
            "author_picture": self.author_picture
        }
        
    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id})"

    def __repr__(self):
        return str(self)