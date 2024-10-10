from sqlalchemy.future import select
from app.database import async_session_maker
from sqlalchemy import exc, update, delete

class BaseDAO:
    model = None
    
    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()
        
    @classmethod
    async def find_one_or_none_by_id(cls, data_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=data_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()
    
    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()
        
    @classmethod
    async def add(cls, **values):
        async with async_session_maker() as session:
            async with session.begin():
                new_instance = cls.model(**values)
                session.add(new_instance)
                try:
                    await session.commit()
                except exc.SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return new_instance

    @classmethod
    async def update(cls, filter_by: dict, update_values: dict):
        async with async_session_maker() as session:
            async with session.begin():
                try:
                    query = update(cls.model).where(
                        *[getattr(cls.model, k) == v for k, v in filter_by.items()]
                    ).values(**update_values).execution_options(synchronize_session="fetch")
                    
                    await session.execute(query)
                    await session.commit()
                    return True
                except exc.SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                    return False
                
    @classmethod
    async def delete(cls, **filter_by):
        async with async_session_maker() as session:
            async with session.begin():
                try:
                    # Удаляем запись, соответствующую фильтру
                    query = delete(cls.model).where(
                        *[getattr(cls.model, k) == v for k, v in filter_by.items()]
                    ).execution_options(synchronize_session="fetch")
                    
                    await session.execute(query)
                    await session.commit()
                    return True
                except exc.SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                    return False