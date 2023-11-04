from sqlalchemy import select, insert, delete
from sqlalchemy.exc import SQLAlchemyError

from config.db import async_session
from exeptions import AlreadyExistsException, NotFoundException


class BaseServices:
    model = None

    @classmethod
    async def find_by_id(cls, model_id: int, mapping: bool = True):
        """Получить model по id"""
        async with async_session() as session:
            query = select(cls.model.__table__.columns).filter_by(id=model_id)
            result = await session.execute(query)
            # scalar_one_or_none() - возвращает один объект или None
            if mapping:
                return result.mappings().one_or_none()
            else:
                return result.scalars().one_or_none()

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
        # try:
        name_ru = data.get('name_ru', None)
        if name_ru:
            db_model = await cls.find_one_or_none(name_ru=name_ru)
            if db_model:
                raise AlreadyExistsException(
                    f"{(cls.model.__tablename__).capitalize()} with {name_ru} already exists")

        query = insert(cls.model).values(**data).returning(cls.model)
        async with async_session() as session:
            result = await session.execute(query)
            await session.commit()
            return result.mappings().first()[f'{(cls.model.__tablename__).capitalize()}']
        # except (SQLAlchemyError, Exception) as e:
        #     if isinstance(e, SQLAlchemyError):
        #         msg = "Database Exc: Cannot insert data into table"
        #     elif isinstance(e, Exception):
        #         msg = "Unknown Exc: Cannot insert data into table"
        #
        #     # logger.error(msg, extra={"table": cls.model.__tablename__}, exc_info=True)
        #     print('error', msg, e)
        #     return None

    @classmethod
    async def update(cls, id: int, **data):
        """Обновить model по id по id взять данные потльзователя и обновить их"""
        async with async_session() as session:
            db_model = select(cls.model).filter_by(id=id)
            result = await session.execute(db_model)
            model = result.scalars().first()

            for key, value in data.items():
                if value:
                    setattr(model, key, value)
            await session.commit()

            return model

    @classmethod
    async def delete(cls, **filter_by):
        async with async_session() as session:
            db_model = select(cls.model).filter_by(**filter_by)
            result = await session.execute(db_model)
            model = result.scalars().first()
            if not model:
                raise NotFoundException(f"{(cls.model.__tablename__).capitalize()} not found")

            query = delete(cls.model).filter_by(**filter_by).returning(cls.model)
            result = await session.execute(query)
            await session.commit()
            return result.mappings().first()[f'{(cls.model.__tablename__).capitalize()}']

    @classmethod
    async def add_bulk(cls, *data):
        # Для загрузки массива данных [{"id": 1}, {"id": 2}]
        # мы должны обрабатывать его через позиционные аргументы *args.
        try:
            query = insert(cls.model).values(*data).returning(cls.model.id)
            async with async_session() as session:
                result = await session.execute(query)
                await session.commit()
                return result.mappings().first()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc"
            elif isinstance(e, Exception):
                msg = "Unknown Exc"
            msg += ": Cannot bulk insert data into table"

            # logger.error(msg, extra={"table": cls.model.__tablename__}, exc_info=True)
            print('error', msg, e)

            return None
