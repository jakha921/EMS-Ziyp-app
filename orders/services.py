from sqlalchemy import insert, select

from config.db import async_session
from exeptions import AlreadyExistsException
from orders.models import Orders
from base.base_service import BaseServices


class OrderServices(BaseServices):
    model = Orders

    @classmethod
    async def create(cls, **data):
        """Создать model"""
        is_unique = await cls.find_one_or_none(user_id=data.get('user_id', None),
                                               product_id=data.get('product_id', None))

        if is_unique:
            raise AlreadyExistsException(
                f"{(cls.model.__tablename__).capitalize()} to this user with this product already exists")

        query = insert(cls.model).values(**data).returning(cls.model)
        async with async_session() as session:
            result = await session.execute(query)
            await session.commit()
            return result.mappings().first()[f'{(cls.model.__tablename__).capitalize()}']

    @classmethod
    async def update(cls, id: int, **data):
        """Обновить model по id по id взять данные потльзователя и обновить их"""

        is_unique = await cls.find_one_or_none(user_id=data.get('user_id', None),
                                               product_id=data.get('product_id', None))

        if is_unique:
            raise AlreadyExistsException(
                f"{(cls.model.__tablename__).capitalize()} to this user with this product already exists")

        async with async_session() as session:
            db_model = select(cls.model).filter_by(id=id)
            result = await session.execute(db_model)
            model = result.scalars().first()

            for key, value in data.items():
                if value:
                    setattr(model, key, value)
            await session.commit()

            return model
