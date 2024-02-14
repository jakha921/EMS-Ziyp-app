import math
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import or_, select, insert
from sqlalchemy.orm import selectinload, outerjoin
from sqlalchemy.sql.functions import count, func

from aws_media.services import change_url
from config.db import async_session
from events.models import Events
from base.base_service import BaseServices


class EventServices(BaseServices):
    model = Events
    search_fields = ['name_ru', 'name_en', 'name_uz', 'description_ru', 'description_en', 'description_uz',
                     'address_ru', 'address_en', 'address_uz']
    load_relations = ['cities']

    @classmethod
    async def find_all(cls, new_event: bool = None, limit: int = None, offset: int = None, search: str = None,
                       **kwargs):
        """Получить все model по фильтру"""
        try:
            async with (async_session() as session):
                # add count of applications event if application_events is not empty else 0
                query = select(cls.model, func.count(cls.model.application_events).label('count_applications')). \
                    outerjoin(cls.model.application_events). \
                    group_by(cls.model.id)

                length_query = select(count(cls.model.id))

                if kwargs.get('is_paid_event') is not None:
                    query = query.where(cls.model.is_paid_event == kwargs.get('is_paid_event'))
                    length_query = length_query.where(cls.model.is_paid_event == kwargs.get('is_paid_event'))

                # Фильтр по дате
                if new_event is not None:
                    now = datetime.utcnow()
                    query = query.where(cls.model.start_date >= now) if new_event else query.where(
                        cls.model.start_date < now)
                    length_query = length_query.where(cls.model.start_date >= now) if new_event else length_query.where(
                        cls.model.start_date < now)

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

                # response = [item[f'{(cls.model.__tablename__).capitalize()}'] for item in response]

                # convert response to dict
                table_name = f'{(cls.model.__tablename__).capitalize()}'
                response = [
                    {
                        **item[table_name].__dict__,
                        'count_applications': item['count_applications']
                    } for item in response
                ]

                # change url
                response = [
                    {
                        **item,
                        'image_urls': await change_url(item['image_urls'], True)
                    } for item in response
                ]

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

        # get image field name and change url to string
        image_field_name = None
        if hasattr(cls.model, 'image_urls'):
            image_field_name = 'image_urls'
        elif hasattr(cls.model, 'images'):
            image_field_name = 'images'
        elif hasattr(cls.model, 'avatar_url'):
            image_field_name = 'avatar_url'
        elif hasattr(cls.model, 'image_url'):
            image_field_name = 'image_url'

        print('image_field_name', image_field_name)
        if image_field_name and data.get(image_field_name) is not None:
            data[image_field_name] = await change_url(data[image_field_name], to_list=False)
        elif image_field_name and data.get(image_field_name) is None:
            data[image_field_name] = ''

        query = insert(cls.model).values(**data).returning(cls.model)
        async with async_session() as session:
            result = await session.execute(query)
            await session.commit()
            print('name model', cls.model.__tablename__)
            if cls.model.__tablename__ not in ['application_grands',
                                               'application_event']:
                return result.mappings().first()[
                    f'{(cls.model.__tablename__).capitalize()}' if cls.model.__tablename__ != 'faqs' else 'FAQs']
            else:
                model_name = cls.model.__tablename__.split('_')  # ['application', 'grands']
                model_name = [item.capitalize() for item in model_name]  # ['Application', 'Grands']
                model_name = ''.join(model_name)  # 'ApplicationGrands'

                # change url to list
                if image_field_name and result.mappings().first()[f'{model_name}'].get(image_field_name) is not None:
                    updated_value = await change_url(result.mappings().first()[f'{model_name}'].get(image_field_name),
                                                     True)
                    result.mappings().first()[f'{model_name}'][image_field_name] = updated_value
                elif image_field_name and result.mappings().first()[f'{model_name}'].get(image_field_name) is None:
                    result.mappings().first()[f'{model_name}'][image_field_name] = []

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
