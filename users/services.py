from sqlalchemy import select

from aws_media.services import change_url
from config.db import async_session
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

            # remove device_token from fields keys
            fields = [field for field in fields if field != 'device_token']

            # remove from fields keys that if they are in values of data
            fields = [field for field in fields if not data.get(field)]

            for key, value in data.items():
                if value:
                    setattr(model, key, value)

            # if fields is empty then add 200 to balance
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
