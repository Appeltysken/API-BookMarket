from sqlalchemy.orm import Mapped, relationship, Session
from app.database import Base, int_pk, str_uniq
from sqlalchemy import text
from typing import List
from app.database import async_session_maker

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

async def init_roles():
    async with async_session_maker() as session:
        result = await session.execute(text("SELECT COUNT(*) FROM roles"))
        count = result.scalar_one_or_none()

        if count is None or count == 0:
            admin_role = Role(id=1, name="admin")
            user_role = Role(id=2, name="user")

            session.add_all([admin_role, user_role])
            await session.commit()
            print("INFO:     Необходимые роли успешно добавлены.")
        else:
            print("INFO:     Роли уже существуют.")