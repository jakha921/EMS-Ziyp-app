from sqlalchemy import insert, select

from config.db import async_session
from exeptions import VolunteerAlreadyExistsException
from volunteers.models import Volunteers
from base.base_service import BaseServices


class VolunteerServices(BaseServices):
    model = Volunteers

    @classmethod
    async def create(cls, **data):
        """Создать model"""
        db_model = select(cls.model.__table__.columns).filter_by(user_id=data['user_id'])
        result = await async_session().execute(db_model)
        model = result.mappings().first()
        if model:
            raise VolunteerAlreadyExistsException

        query = insert(cls.model).values(**data).returning(cls.model)
        async with async_session() as session:
            result = await session.execute(query)
            await session.commit()
            return result.mappings().first()[f'{(cls.model.__tablename__).capitalize()}']
