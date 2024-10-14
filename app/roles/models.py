from sqlalchemy.orm import Mapped, relationship
from app.database import Base, int_pk, str_uniq
from typing import List

class Role(Base):
    __tablename__ = "roles"
    
    id: Mapped[int_pk]
    name: Mapped[str_uniq]
    
    users: Mapped[List["User"]] = relationship("User", back_populates="role")
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }
        
    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id})"

    def __repr__(self):
        return str(self)