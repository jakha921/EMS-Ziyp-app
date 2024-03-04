from sqlalchemy import select, text, insert
from config.db import async_session

from application_events.models import ApplicationEvents
from aws_media.services import change_url
from base.base_service import BaseServices
from events.models import Events
from exeptions import AlreadyExistsException
from notification.firebase_notification import send_push_notification
from users.models import Users


class ApplicationEventServices(BaseServices):
    model = ApplicationEvents
    load_relations = ["users", "events"]

    @classmethod
    async def create(cls, **data):
        """Создать model"""
        # try:
        async with async_session() as session:

            db_model = await session.execute(
                select(cls.model).filter_by(user_id=data.get('user_id'), event_id=data.get('event_id'))
            )
            db_model = db_model.scalars().first()

            if db_model:
                raise AlreadyExistsException(
                    "User already registered for this event")

            # get by id event and check if event is paid and user has enough balance
            if data.get('status') == 'pending':
                # SELECT * FROM events WHERE events.id = 1
                event = await session.execute(
                    select(Events).filter_by(id=data.get('event_id'))
                )
                event = event.scalars().first()

                if event.is_paid_event:
                    # get by id user and check if user has enough balance
                    user = await session.execute(
                        select(Users).filter_by(id=data.get('user_id'))
                    )
                    user = user.scalars().first()

                    if user.balance - event.price < 0:
                        raise AlreadyExistsException(
                            "User doesn't have enough balance")
                    else:
                        # update balance
                        user.balance -= event.price

            query = insert(cls.model).values(**data).returning(cls.model)
            result = await session.execute(query)
            await session.commit()

            model_name = cls.model.__tablename__.split('_')  # ['application', 'grands']
            model_name = [item.capitalize() for item in model_name]  # ['Application', 'Grands']
            model_name = ''.join(model_name)  # 'ApplicationGrands'

            return result.mappings().first()[f'{model_name}']

    @classmethod
    async def update(cls, id: int, **data):
        """Обновить model по id по id взять данные потльзователя и обновить их"""
        async with async_session() as session:
            db_model = await cls.find_one_or_none(user_id=data.get('user_id'), event_id=data.get('event_id'))
            if db_model:
                raise AlreadyExistsException(
                    "User already registered for this event")

            db_model = select(cls.model).filter_by(id=id)
            result = await session.execute(db_model)
            model = result.scalars().first()

            if data.get('status') == 'approved':
                # get by id event and update balance
                # SELECT * FROM events WHERE events.id = 1

                event = await session.execute(
                    select(Events).filter_by(id=model.event_id)
                )
                event = event.scalars().first()

                if event.scores > 0:
                    # get by id user and update balance
                    user = await session.execute(
                        select(Users).filter_by(id=model.user_id)
                    )
                    user = user.scalars().first()

                    # update balance
                    print('user', user.id)
                    print('user.balance', user.balance)
                    user.balance += event.scores
                    print('user.balance', user.balance)

                    # send notification
                    await send_push_notification(
                        token=user.device_token,
                        title="Поздравляем!",
                        body=f"Вы успешно прошли регистрацию на мероприятие {event.name_ru} и получили {event.scores} YC на баланс!"
                    )

            for key, value in data.items():
                if value:
                    setattr(model, key, value)
            await session.commit()

            return model
