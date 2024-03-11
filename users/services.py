from datetime import datetime

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError

from aws_media.services import change_url
from config.db import async_session
from exeptions import NotFoundException, AlreadyExistsException
from notification.firebase_notification import send_push_notification
from users.models import Users
from base.base_service import BaseServices


class UserServices(BaseServices):
    model = Users
    load_relations = [
        "cities"
    ]

    @classmethod
    async def update(cls, id: int, **data):
        """Обновить model по id по id взять данные потльзователя и обновить их"""
        async with async_session() as session:
            db_model = select(cls.model).filter_by(id=id)
            result = await session.execute(db_model)
            model = result.scalars().first()

            # get image field name and change url to string
            image_field_name = None
            if hasattr(cls.model, 'image_urls'):
                image_field_name = 'image_urls'
            elif hasattr(cls.model, 'images'):
                image_field_name = 'images'
            elif hasattr(cls.model, 'avatar_url'):
                image_field_name = 'avatar_url'

            if image_field_name and data.get(image_field_name) is not None:
                data[image_field_name] = await change_url(data[image_field_name], to_list=False)
            elif image_field_name and data.get(image_field_name) is None:
                data[image_field_name] = ''

            # get all fields from model where value is None and collect them in list
            fields = [key for key, value in model.__dict__.items() if value is None]

            # remove device_token, deleted_at and avatar_url from fields
            fields = [field for field in fields if field not in ['device_token', 'deleted_at', 'avatar_url']]

            # remove from fields keys that if they are in values of data
            fields = [field for field in fields if not data.get(field)]

            for key, value in data.items():
                if value:
                    setattr(model, key, value)

            # if fields is empty then add 200 to balance
            print('fields', fields)
            print('model.is_completed_profile', model.is_completed_profile)
            print('-' * 10)
            print('is not fields and not model.is_completed_profile', not fields and not model.is_completed_profile)
            if not fields and not model.is_completed_profile:
                model.balance += 200
                model.is_completed_profile = True
                status = await send_push_notification(
                    token=model.device_token,
                    title="Поздравляем!",
                    body="Вы успешно прошли регистрацию и получили 200 YC на баланс!"
                )
            await session.commit()

            return model

    @classmethod
    async def delete(cls, **filter_by):
        async with async_session() as session:
            db_model = select(cls.model).filter_by(**filter_by)
            result = await session.execute(db_model)
            model = result.scalars().first()
            if model.deleted_at:
                raise NotFoundException(f"{(cls.model.__tablename__).capitalize()} not found")

            try:
                # query = delete(cls.model).filter_by(**filter_by).returning(cls.model)
                query = update(cls.model).where(cls.model.id == model.id).values(deleted_at=datetime.utcnow()).returning(
                    cls.model)
                result = await session.execute(query)
                await session.commit()
                return result.mappings().first()[
                    f'{(cls.model.__tablename__).capitalize()}' if cls.model.__tablename__ != 'faqs' else 'FAQs']
            except IntegrityError as e:
                await session.rollback()
                raise AlreadyExistsException("Deletion failed due to protected data integrity constraint.") from e
            except Exception as e:
                await session.rollback()
                print('e', e)
                raise AlreadyExistsException("Deletion failed due to an unexpected error.") from e

