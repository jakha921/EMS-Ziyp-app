from sqlalchemy import select, text, insert, delete
from sqlalchemy.exc import IntegrityError

from config.db import async_session

from application_events.models import ApplicationEvents
from aws_media.services import change_url
from base.base_service import BaseServices
from events.models import Events
from exeptions import AlreadyExistsException, NotFoundException
from notification.firebase_notification import send_push_notification
from users.models import Users


class ApplicationEventServices(BaseServices):
    model = ApplicationEvents
    load_relations = ["users", "events"]

    @classmethod
    async def create(cls, lang: str, **data):
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

            user = await session.execute(
                select(Users).filter_by(id=data.get('user_id'))
            )
            user = user.scalars().first()

            # check exist place in event
            event = await session.execute(
                select(Events).filter_by(id=data.get('event_id'))
            )
            event = event.scalars().first()

            if not event.is_exist_free_places:
                raise AlreadyExistsException(
                    "No free places for this event")

            if event.place > 0:
                # update places
                event.place -= 1
                if event.place == 0:
                    event.is_exist_free_places = False

            # get by id event and check if event is paid and user has enough balance
            if data.get('status') == 'pending':
                if event.is_paid_event:
                    # get by id user and check if user has enough balance
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

            # send notification
            msg = {
                "ru": {
                    "title": "Успешно!",
                    "body": f"Вы успешно отправили заявку на мероприятие {event.name_ru}."
                },
                "uz": {
                    "title": "Muvaffaqiyatli!",
                    "body": f"Siz {event.name_uz} tabdbirga muvaffaqiyatli ariza yubordingiz."
                },
                "en": {
                    "title": "Successfully!",
                    "body": f"You have successfully sent an application for the event {event.name_en}."
                }
            }

            text = msg.get(lang)

            # send notification
            await send_push_notification(
                token=user.device_token,
                title=text.get('title'),
                body=text.get('body')
            )

            return result.mappings().first()[f'{model_name}']

    @classmethod
    async def update(cls, id: int, lang: str, **data):
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
                    msg = {
                        "ru": {
                            "title": "Поздравляем!",
                            "body": f"Вы успешно прошли регистрацию на мероприятие {event.name_ru} и получили {event.scores} YC на баланс!"
                        },
                        "uz": {
                            "title": "Tabriklaymiz!",
                            "body": f"Siz {event.name_uz} tadbiriga muvaffaqiyatli ro'yxatdan o'tdingiz va {event.scores} YC olgansiz!"
                        },
                        "en": {
                            "title": "Congratulations!",
                            "body": f"You have successfully registered for the event {event.name_en} and received {event.scores} YC on your balance!"
                        }
                    }

                    text = msg.get(lang)

                    # send notification
                    await send_push_notification(
                        token=user.device_token,
                        title=text.get('title'),
                        body=text.get('body')
                    )

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

            try:
                query = delete(cls.model).filter_by(**filter_by).returning(cls.model)
                result = await session.execute(query)

                # check exist place in event
                event = await session.execute(
                    select(Events).filter_by(id=model.event_id)
                )
                event = event.scalars().first()

                # update places
                event.place += 1
                if event.place > 0:
                    event.is_exist_free_places = True

                await session.commit()
                return result.mappings().first()['ApplicationEvents']
            except IntegrityError as e:
                await session.rollback()
                raise AlreadyExistsException("Deletion failed due to protected data integrity constraint.") from e
            except Exception as e:
                await session.rollback()
                print('error', e)
                raise AlreadyExistsException("Deletion failed due to an unexpected error.")
