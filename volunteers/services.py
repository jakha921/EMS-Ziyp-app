from sqlalchemy import insert, select, update

from config.db import async_session
from exeptions import VolunteerAlreadyExistsException
from users.models import Users
from volunteers.models import Volunteers
from base.base_service import BaseServices


class VolunteerServices(BaseServices):
    model = Volunteers
    load_relations = [
        "users"
    ]

    @classmethod
    async def create(cls, **data):
        """Создать model"""
        db_model = select(cls.model.__table__.columns).filter_by(user_id=data['user_id'])
        result = await async_session().execute(db_model)
        model = result.mappings().first()
        if model:
            raise VolunteerAlreadyExistsException

        # change user field is volunteer to True
        async with async_session() as session:
            user = update(Users).where(Users.id == data['user_id']).values(is_volunteer=True)
            await session.execute(user)
            await session.commit()

        query = insert(cls.model).values(**data).returning(cls.model)
        async with async_session() as session:
            result = await session.execute(query)
            await session.commit()
            return result.mappings().first()[f'{(cls.model.__tablename__).capitalize()}']
