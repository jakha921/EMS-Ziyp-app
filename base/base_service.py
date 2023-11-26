import math

from fastapi import HTTPException
from sqlalchemy import select, insert, delete, or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.functions import count

from config.db import async_session
from exeptions import AlreadyExistsException, NotFoundException


class BaseServices:
    model = None
    search_fields = []
    load_relations = []

    @classmethod
    async def find_by_id(cls, model_id: int, mapping: bool = False):
        """Получить model по id"""
        async with async_session() as session:
            query = select(cls.model).filter_by(id=model_id)

            if cls.load_relations:
                for relation in cls.load_relations:
                    query = query.options(selectinload(getattr(cls.model, relation)))

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
            query = select(cls.model).filter_by(**kwargs)

            if cls.load_relations:
                for relation in cls.load_relations:
                    query = query.options(selectinload(getattr(cls.model, relation)))

            result = await session.execute(query)
            return result.scalars().one_or_none()

    @classmethod
    async def find_all(cls, limit: int = None, offset: int = None, search: str = None, **kwargs):
        """Получить все model по фильтру"""
        try:
            async with async_session() as session:
                # Поиск по фильтру kwargs = {"id": 1, "name": "test"} -> WHERE id=1 AND name="test"
                kwargs = {key: value for key, value in kwargs.items() if value is not None}
                query = select(cls.model).filter_by(**kwargs)
                length_query = select(count(cls.model.id)).filter_by(**kwargs)

                # Поиск по полям
                if search and cls.search_fields:
                    query = query.where(
                        or_(
                            *[getattr(cls.model, field).ilike(f'%{search}%') for field in cls.search_fields]
                        )
                    )
                    length_query = length_query.where(
                        or_(
                            *[getattr(cls.model, field).ilike(f'%{search}%') for field in cls.search_fields]
                        )
                    )

                # Загрузка связей
                if cls.load_relations:
                    for relation in cls.load_relations:
                        query = query.options(selectinload(getattr(cls.model, relation)))

                # Пагинация
                if limit and offset:
                    query = query.offset((offset - 1) * limit).limit(limit)

                # Сортировка
                query = query.order_by(cls.model.id.desc())
                result = await session.execute(query)
                response = result.mappings().all()

                # Преобразование в список
                if cls.model.__tablename__ not in ["application_grands", "application_events"]:
                    response = [item[f'{(cls.model.__tablename__).capitalize()}'] for item in response]
                else:
                    model_name = cls.model.__tablename__.split('_')  # ['application', 'grands']
                    model_name = [item.capitalize() for item in model_name]  # ['Application', 'Grands']
                    model_name = ''.join(model_name)  # 'ApplicationGrands'
                    response = [item[f'{model_name}'] for item in response]

                # Подсчет количества записей
                result_count_items = (await session.execute(length_query)).scalar()

                return {
                    "status": "success",
                    "detail": f"Get {cls.model.__tablename__} successfully",
                    "pagination": {
                        "total_pages": math.ceil(result_count_items / limit),
                        "current_page": offset,
                        "total_items": result_count_items,
                        "has_next_page": True if offset < math.ceil(result_count_items / limit) else False,
                        "has_previous_page": True if offset > 1 else False,
                    } if limit and offset else None,
                    "data": response
                }
        except Exception as e:
            raise HTTPException(status_code=400, detail={
                "status": "error",
                "detail": f"{cls.model.__tablename__} not retrieved",
                "data": str(e) if str(e) else None
            })

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
            print('name model', cls.model.__tablename__)
            if cls.model.__tablename__ not in ['application_grands',
                                               'application_event']:
                return result.mappings().first()[f'{(cls.model.__tablename__).capitalize()}']
            else:
                model_name = cls.model.__tablename__.split('_')  # ['application', 'grands']
                model_name = [item.capitalize() for item in model_name]  # ['Application', 'Grands']
                model_name = ''.join(model_name)  # 'ApplicationGrands'
                return result.mappings().first()[f'{model_name}']
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
