from sqlalchemy import insert, select, delete, update

from config.db import async_session
from exeptions import AlreadyExistsException, NotFoundException
from notification.firebase_notification import send_push_notification
from orders.models import Orders
from base.base_service import BaseServices
from products.models import Products
from users.models import Users


class OrderServices(BaseServices):
    model = Orders
    load_relations = [
        "users",
        "products"
    ]

    @classmethod
    async def create(cls, **data):
        """Создать model"""
        async with async_session() as session:
            is_unique = await session.execute(
                select(cls.model).filter_by(user_id=data.get('user_id'), product_id=data.get('product_id')))
            is_unique = is_unique.scalars().first()

            if is_unique:
                raise AlreadyExistsException(
                    "Order for this user and product already exists.")

            # get product price and update user balance
            product = await session.execute(
                select(Products).filter_by(id=data.get('product_id')))
            product_price = product.scalars().first().price

            user = await session.execute(
                select(Users).filter_by(id=data.get('user_id')))
            user = user.scalars().first()

            user_balance = user.balance

            print('event', product_price, 'user', user_balance)
            if user_balance < product_price:
                raise AlreadyExistsException(
                    "User balance is not enough for this product.")
            user_balance -= product_price
            # apply changes to user balance
            await session.execute(
                update(Users).where(Users.id == data.get('user_id')).values(balance=user_balance))

            print('user', user_balance)

            # send push notification
            await send_push_notification(
                token=user.device_token,
                title="Заказ",
                body=f"Ваш заказ успешно оформлен!\nC вашего баланса списано {product_price} YC"
            )

            query = insert(cls.model).values(**data).returning(cls.model)
            result = await session.execute(query)
            await session.commit()

            await session.commit()
            return result.mappings().first()[f'{(cls.model.__tablename__).capitalize()}']

    @classmethod
    async def delete(cls, **filter_by):
        async with async_session() as session:
            db_model = select(cls.model).filter_by(**filter_by)
            result = await session.execute(db_model)
            model = result.scalars().first()
            if not model:
                raise NotFoundException(f"{(cls.model.__tablename__).capitalize()} not found")

            # get product price and update user balance
            product = await session.execute(
                select(Products).filter_by(id=model.product_id))
            product_price = product.scalars().first().price
            user = await session.execute(
                select(Users).filter_by(id=model.user_id))
            user = user.scalars().first()

            user_balance = user.balance

            user_balance += product_price
            # apply changes to user balance
            await session.execute(
                update(Users).where(Users.id == model.user_id).values(balance=user_balance))

            # send push notification
            await send_push_notification(
                token=user.device_token,
                title="Заказ",
                body=f"Ваш заказ отменен!\nНа ваш баланс зачислено {product_price} YC"
            )

            query = delete(cls.model).filter_by(**filter_by).returning(cls.model)
            result = await session.execute(query)
            await session.commit()
            return result.mappings().first()[
                f'{(cls.model.__tablename__).capitalize()}' if cls.model.__tablename__ != 'faqs' else 'FAQs']
