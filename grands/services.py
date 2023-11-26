import math

from fastapi import HTTPException
from sqlalchemy import select, func, or_
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.functions import count

from config.db import async_session
from grands.models import Grands
from base.base_service import BaseServices


class GrandsServices(BaseServices):
    model = Grands
    search_fields = [
        "name_ru",
        "name_en",
        "name_uz",
        "description_ru",
        "description_en",
        "description_uz",
    ]

    @classmethod
    async def find_all(cls, limit: int = None, offset: int = None, search: str = None, **kwargs):
        """Получить все model по фильтру"""
        try:
            async with async_session() as session:
                # Поиск по фильтру kwargs = {"id": 1, "name": "test"} -> WHERE id=1 AND name="test"
                kwargs = {key: value for key, value in kwargs.items() if value is not None}
                query = select(cls.model, func.count(cls.model.application_grands).label('count_applications')). \
                    outerjoin(cls.model.application_grands). \
                    group_by(cls.model.id)
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
                response = [
                    {
                        **item[f'{(cls.model.__tablename__).capitalize()}'].__dict__,
                        'count_applications': item['count_applications']
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
