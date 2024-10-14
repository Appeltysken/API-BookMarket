from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, text
from app.database import Base, str_uniq, int_pk, str_null_true, int_null_true
from passlib.context import CryptContext
from typing import List
from app.roles.models import Role

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Вернуться потом к /articles/828328/, когда будешь делать
# другие сущности и нужно будет передать им значения в виде числа
# а возвращалось через Foreign Key название

class User(Base):
    __tablename__ = "users"

    id: Mapped[int_pk]
    username: Mapped[str_uniq]
    password: Mapped[str]
    Fname: Mapped[str]
    Lname: Mapped[str]
    sex: Mapped[str]
    email: Mapped[str_uniq]
    phone: Mapped[str_uniq]
    sell_history: Mapped[str_null_true]
    buy_history: Mapped[str_null_true]
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), default=1)

    orders: Mapped[List["Order"]] = relationship("Order", back_populates="user", cascade="all, delete-orphan")
    role: Mapped["Role"] = relationship("Role", back_populates="users")

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
            "password": self.password,
            "Fname": self.Fname,
            "Lname": self.Lname,
            "sex": self.sex,
            "email": self.email,
            "phone": self.phone,
            "sell_history": self.sell_history,
            "buy_history": self.buy_history,
            "role_id": self.role_id
        }