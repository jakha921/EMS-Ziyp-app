import math

from fastapi import HTTPException
from sqlalchemy import insert, select, delete, update, or_
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.functions import count

from aws_media.services import change_url
from base.base_service import BaseServices
from config.db import async_session
from exeptions import AlreadyExistsException, NotFoundException
from notification.firebase_notification import send_push_notification
from orders.models import Orders
from products.models import Products
from users.models import Users


class OrderServices(BaseServices):
    model = Orders
    load_relations = [
        "users",
        "products"
    ]

    @classmethod
    async def find_all(cls, limit: int = None, offset: int = None, search: str = None, **filters):
        """Получить все model по фильтру"""
        try:
            async with async_session() as session:
                # Поиск по фильтру kwargs = {"id": 1, "name": "test"} -> WHERE id=1 AND name="test"

                kwargs = {key: value for key, value in filters.items() if value is not None}
                if 'deleted_at' in filters.keys():
                    kwargs['deleted_at'] = None

                query = select(cls.model).filter_by(**kwargs)
                length_query = select(count(cls.model.id)).filter_by(**kwargs)
                new_status = select(count(cls.model.id)).filter_by(order_status="new", **kwargs)

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
                if cls.model.__tablename__ not in ["application_grands", "application_events"]:
                    response = [item[
                                    f'{(cls.model.__tablename__).capitalize()}' if cls.model.__tablename__ != 'faqs' else 'FAQs']
                                for item in response]
                else:
                    model_name = cls.model.__tablename__.split('_')  # ['application', 'grands']
                    model_name = [item.capitalize() for item in model_name]  # ['Application', 'Grands']
                    model_name = ''.join(model_name)  # 'ApplicationGrands'
                    response = [item[f'{model_name}'] for item in response]

                # Подсчет количества записей
                result_count_items = (await session.execute(length_query)).scalar()
                result_count_new_status = (await session.execute(new_status)).scalar()

                # change url
                for item in response:
                    image_field_name = None
                    if hasattr(cls.model, 'image_urls'):
                        image_field_name = 'image_urls'
                    elif hasattr(cls.model, 'images'):
                        image_field_name = 'images'
                    elif hasattr(cls.model, 'avatar_url'):
                        image_field_name = 'avatar_url'
                    elif hasattr(cls.model, 'image_url'):
                        image_field_name = 'image_url'

                    if image_field_name and getattr(item, image_field_name) is not None:
                        updated_value = await change_url(getattr(item, image_field_name), True)
                        setattr(item, image_field_name, updated_value)
                    elif image_field_name and getattr(item, image_field_name) is None:
                        setattr(item, image_field_name, [])

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
                    "count_new_status": result_count_new_status,
                    "data": response.__dict__ if isinstance(response, dict) else response
                }
        except Exception as e:
            raise HTTPException(status_code=400, detail={
                "status": "error",
                "detail": f"{cls.model.__tablename__} not retrieved",
                "data": str(e) if str(e) else None
            })

    @classmethod
    async def create(cls, lang: str, **data):
        """Создать model"""
        async with async_session() as session:
            statuses = ['completed', 'canceled']
            # where status not in ('completed', 'canceled')

            is_unique = await session.execute(
                select(cls.model).filter_by(user_id=data.get('user_id'), product_id=data.get('product_id')).where(
                    cls.model.order_status.notin_(statuses))
            )

            is_unique = is_unique.scalars().first()
            print('is_unique', is_unique)

            if is_unique:
                raise AlreadyExistsException(
                    "Order for this user and product already exists." if lang == 'en' else
                    "Заказ для этого пользователя и продукта уже существует." if lang == 'ru' else
                    "Bu foydalanuvchi va mahsulot uchun buyurtma mavjud."

                )

            # get product price and update user balance
            product = await session.execute(
                select(Products).filter_by(id=data.get('product_id')))
            product = product.scalars().first()
            product_price = product.price
            quantity_product = product.quantity if product.quantity else 0

            # check if product is available
            if quantity_product == 0:
                raise AlreadyExistsException(
                    "Product is not available." if lang == 'en' else
                    "Продукт недоступен." if lang == 'ru' else
                    "Mahsulot mavjud emas."
                )

            if data.get('count'):
                if quantity_product - data.get('count') < 0:
                    raise AlreadyExistsException(
                        "Product is not available in this quantity." if lang == 'en' else
                        "Продукт недоступен в данном количестве." if lang == 'ru' else
                        "Mahsulot bu miqdorda mavjud emas."
                    )
                else:
                    quantity_product -= data.get('count')
                    await session.execute(
                        update(Products).where(Products.id == product.id).values(quantity=quantity_product))

            user = await session.execute(
                select(Users).filter_by(id=data.get('user_id')))
            user = user.scalars().first()

            user_balance = user.balance

            print('event', product_price, 'user', user_balance)
            if user_balance < product_price:
                raise AlreadyExistsException(
                    "User balance is not enough for this product." if lang == 'en' else
                    "Баланс пользователя недостаточен для этого продукта." if lang == 'ru' else
                    "Foydalanuvchi balansi ushbu mahsulot uchun yetarli emas."
                )
            user_balance -= product_price
            # apply changes to user balance
            await session.execute(
                update(Users).where(Users.id == data.get('user_id')).values(balance=user_balance))

            print('user', user_balance)

            # send push notification
            msg = {
                "ru": {
                    "title": "Заказ",
                    "body": f"Ваш заказ успешно оформлен!\nC вашего баланса списано {product_price} YC"
                },
                "en": {
                    "title": "Order",
                    "body": f"Your order has been successfully placed!\n{product_price} YC has been deducted from your balance"
                },
                "uz": {
                    "title": "Buyurtma",
                    "body": f"Sizning buyurtmangiz muvaffaqiyatli qabul qilindi!\nSizning balansingizdan {product_price} YC ayirib olinadi"
                }
            }

            text = msg.get(lang)

            await send_push_notification(
                token=user.device_token,
                title=text.get('title'),
                body=text.get('body')
            )

            query = insert(cls.model).values(**data).returning(cls.model)
            result = await session.execute(query)
            await session.commit()

            await session.commit()
            return result.mappings().first()[f'{(cls.model.__tablename__).capitalize()}']

    @classmethod
    async def delete(cls, lang: str, **filter_by):
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
            msg = {
                "ru": {
                    "title": "Заказ",
                    "body": f"Ваш заказ отменен!\nНа ваш баланс зачислено {product_price} YC"
                },
                "en": {
                    "title": "Order",
                    "body": f"Your order has been canceled!\n{product_price} YC has been credited to your balance"
                },
                "uz": {
                    "title": "Buyurtma",
                    "body": f"Sizning buyurtmangiz bekor qilindi!\nSizning balansingizga {product_price} YC qo'shildi"
                }
            }

            text = msg.get(lang)

            await send_push_notification(
                token=user.device_token,
                title=text.get('title'),
                body=text.get('body')
            )

            query = delete(cls.model).filter_by(**filter_by).returning(cls.model)
            result = await session.execute(query)
            await session.commit()
            return result.mappings().first()[
                f'{(cls.model.__tablename__).capitalize()}' if cls.model.__tablename__ != 'faqs' else 'FAQs']
