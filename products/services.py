from sqlalchemy import insert, select

from config.db import async_session
from exeptions import AlreadyExistsException, NotFoundException
from products.models import Products
from base.base_service import BaseServices


class ProductService(BaseServices):
    model = Products
    load_relations = [
        "categories"
    ]
    search_fields = [
        "name_ru",
        "name_en",
        "name_uz",
        "description_ru",
        "description_en",
        "description_uz",
    ]

    @classmethod
    async def create(cls, **data):
        """Создать model"""
        # try:
        name_ru = data.get('name_ru', None)
        if name_ru:
            db_model = await cls.find_one_or_none(name_ru=name_ru)
            if db_model:
                raise AlreadyExistsException(
                    f"{(cls.model.__tablename__).capitalize()} with {name_ru} already exists")

        if images := data.get('images', None):
            data['images'] = str(images)

        query = insert(cls.model).values(**data).returning(cls.model)
        async with async_session() as session:
            result = await session.execute(query)
            await session.commit()
            return result.mappings().first()[f'{(cls.model.__tablename__).capitalize()}']

    @classmethod
    async def update(cls, id: int, **data):
        """Обновить model по id по id взять данные потльзователя и обновить их"""
        async with async_session() as session:
            db_model = select(cls.model).filter_by(id=id)
            result = await session.execute(db_model)
            model = result.scalars().first()

            if not model:
                raise NotFoundException(f"{(cls.model.__tablename__).capitalize()} with id {id} not found")

            if images := data.get('images', None):
                data['images'] = str(images)

            for key, value in data.items():
                if value:
                    setattr(model, key, value)
            await session.commit()

            return model
