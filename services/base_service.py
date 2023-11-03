from sqlalchemy import select, insert

from config.db import async_session


class BaseServices:
    model = None

    @classmethod
    async def find_by_id(cls, model_id: int):
        """Получить model по id"""
        async with async_session() as session:
            query = select(cls.model.__table__.columns).filter_by(id=model_id)
            result = await session.execute(query)
            # scalar_one_or_none() - возвращает один объект или None
            return result.mappings().one_or_none()

    @classmethod
    async def find_one_or_none(cls, **kwargs):
        """Получить один model по фильтру"""
        async with async_session() as session:
            query = select(cls.model.__table__.columns).filter_by(**kwargs)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def find_all(cls, **kwargs):
        """Получить все model по фильтру"""
        async with async_session() as session:
            query = select(cls.model.__table__.columns).filter_by(**kwargs)  # SELECT * FROM model WHERE kwargs
            result = await session.execute(query)
            # print(result.mappings().all())
            return result.mappings().all()

    @classmethod
    async def create(cls, **data):
        """Создать model"""
        async with async_session() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()
            return {
                'status': 'success',
            }
