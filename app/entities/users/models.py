from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, text
from app.database import Base, str_uniq, int_pk, str_null_true, int_null_true, str_uniq_but_nullable
from passlib.context import CryptContext
from typing import List
from app.entities.roles.models import Role

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Вернуться потом к /articles/828328/, когда будешь делать
# другие сущности и нужно будет передать им значения в виде числа
# а возвращалось через Foreign Key название или пофиг

class User(Base):
    __tablename__ = "users"

    id: Mapped[int_pk]
    username: Mapped[str_uniq]
    password: Mapped[str]
    Fname: Mapped[str_null_true | None]
    Lname: Mapped[str_null_true | None]
    sex: Mapped[str]
    email: Mapped[str_uniq_but_nullable | None]
    phone: Mapped[str_uniq_but_nullable | None]
    sell_history: Mapped[str_null_true | None]
    buy_history: Mapped[str_null_true | None]
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), default=1)
    profile_picture: Mapped[str | None]

    orders: Mapped[List["Order"]] = relationship("Order", back_populates="user", cascade="all, delete-orphan")
    role: Mapped["Role"] = relationship("Role", back_populates="users")
    reviews: Mapped["Review"] = relationship("Review", back_populates="users")
    books: Mapped["Book"] = relationship("Book", back_populates="users")

    extend_existing = True
        
    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"first_name={self.Fname!r}, "
                f"last_name={self.Lname!r})")

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "Fname": self.Fname,
            "Lname": self.Lname,
            "sex": self.sex,
            "email": self.email,
            "phone": self.phone,
            "sell_history": self.sell_history,
            "buy_history": self.buy_history,
            "role_id": self.role_id,
            "profile_picture": self.profile_picture
        }