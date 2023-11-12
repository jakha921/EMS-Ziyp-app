from fastapi import HTTPException, status
from sqlalchemy import select, or_
from sqlalchemy.orm import selectinload, defer

from config.db import async_session
from users.models import Users
from base.base_service import BaseServices


class UserServices(BaseServices):
    model = Users

    @classmethod
    async def find_all(cls, limit: int = None, offset: int = None, search: str = None, **kwargs):
        """Получить все model по фильтру"""
        try:
            async with async_session() as session:
                query = select(cls.model.__table__.columns).filter_by(**kwargs)  # SELECT * FROM model WHERE kwargs

                # Поиск по полям
                if search and cls.search_fields:
                    query = query.where(
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
                    query = query.limit(limit).offset(offset)

                # Сортировка
                query = query.order_by(cls.model.id.desc())
                result = await session.execute(query)
                response = result.mappings().all()

                return {
                    "status": "success",
                    "detail": f"Get {cls.model.__tablename__} successfully",
                    "pagination": {
                        "total": len(response),
                        "limit": limit,
                        "offset": offset,
                        "has_next_page": True if len(response) == limit else False,
                        "has_previous_page": True if offset > 0 else False,
                        "current_page": offset + 1 if offset else 1,
                        "total_pages": len(response) // limit + 1 if len(response) % limit else len(response) // limit
                    } if limit and offset else None,
                    "data": response
                }
        except Exception as e:
            raise HTTPException(status_code=400, detail={
                "status": "error",
                "detail": f"Get {cls.model.__tablename__} error",
                "data": str(e) if str(e) else None
            })
