from sqlalchemy.future import select
from app.database import async_session_maker
from sqlalchemy import exc, update, delete, exc
from fastapi import UploadFile, HTTPException
from starlette.responses import FileResponse
import os

class BaseDAO:
    model = None
    upload_folder = "uploads"
    
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
    async def update(cls, id: int, update_data: dict):
        async with async_session_maker() as session:
            async with session.begin():
                try:
                    query = (
                        update(cls.model)
                        .where(cls.model.id == id)
                        .values(**update_data)
                        .execution_options(synchronize_session="fetch")
                    )
                    
                    result = await session.execute(query)
                    await session.commit()

                    if result.rowcount == 0:
                        return False
                    
                    return True
                except exc.SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                
    @classmethod
    async def delete(cls, **filter_by):
        async with async_session_maker() as session:
            async with session.begin():
                try:
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
    
    @classmethod
    async def upload_image(cls, entity_name: str, entity_id: int, file: UploadFile, image_field: str, allowed_extensions=None, max_file_size_mb=5):
        if allowed_extensions is None:
            allowed_extensions = ["jpg", "jpeg", "png"]

        file_extension = file.filename.split(".")[-1].lower()
        if file_extension not in allowed_extensions:
            raise HTTPException(status_code=400, detail=f"Неподдерживаемый формат файла. Поддерживаются только: {', '.join(allowed_extensions)}.")

        file_data = await file.read()
        if len(file_data) > max_file_size_mb * 1024 * 1024:
            raise HTTPException(status_code=400, detail=f"Файл слишком большой. Максимум {max_file_size_mb}MB.")

        entity_folder = os.path.join(cls.upload_folder, entity_name.lower())
        os.makedirs(entity_folder, exist_ok=True)
        file_path = os.path.join(entity_folder, f"{entity_id}.{file_extension}")

        with open(file_path, "wb") as buffer:
            buffer.write(file_data)

        update_data = {image_field: file_path}
        await cls.update(entity_id, update_data)

        return {"message": "Изображение успешно загружено."}

    @classmethod
    async def get_image(cls, entity_name: str, entity_id: int, image_field: str):
        file_path = os.path.join(cls.upload_folder, entity_name.lower(), f"{entity_id}.jpg")
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Изображение не найдено")
        return FileResponse(file_path)

    @classmethod
    async def delete_image(cls, entity_name: str, entity_id: int, image_field: str):
        file_path = os.path.join(cls.upload_folder, entity_name.lower(), f"{entity_id}.jpg")
        if os.path.exists(file_path):
            os.remove(file_path)

        update_data = {image_field: None}
        await cls.update(entity_id, update_data)

        return {"message": "Изображение успешно удалено."}