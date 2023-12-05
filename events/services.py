import math
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import or_, select
from sqlalchemy.orm import selectinload, outerjoin
from sqlalchemy.sql.functions import count, func

from aws_media.services import change_url
from config.db import async_session
from events.models import Events
from base.base_service import BaseServices


class EventServices(BaseServices):
    model = Events
    search_fields = ['name_ru', 'name_en', 'name_uz', 'description_ru', 'description_en', 'description_uz', 'address']
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
