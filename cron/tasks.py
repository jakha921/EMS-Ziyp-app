from datetime import datetime

from aiocron import crontab
import asyncio

from application_events.services import ApplicationEventServices
from notification.firebase_notification import send_push_notification
from notification.services import NotificationServices
from users.services import UserServices


# Define your cron job function
async def cron_job():
    # Do something asynchronously
    print('-' * 10)
    print("Cron job running...", datetime.now(), '\n')

    # get all notifications where datetime_to_send is less than now
    notifications = await NotificationServices.get_datetime_to_send_less_than_now()
    print('notification', notifications)

    for notification in notifications:

        # get all users from application events where application event = notification.event_id
        application_events = await ApplicationEventServices.find_all(event_id=notification.event_id)
        print('application_events', application_events)

        # get user from application events
        # for application_event in application_events['data']:
        #     user = await UserServices.find_one_or_none(id=application_event.user_id)
        #     users.append(user)

        user_ids = [application_event.user_id for application_event in application_events['data']]
        users = await UserServices.get_by_ids(user_ids)

        # send push notification to users
        print('users', users)
        for user in users:
            foo = await send_push_notification(
                token=user.device_token,
                title=notification.title_ru if user.lang == 'ru' else notification.title_uz if user.lang == 'uz' else notification.title_en,
                body=notification.body_ru if user.lang == 'ru' else notification.body_uz if user.lang == 'uz' else notification.body_en
            )
            print('send_push_notification', user.phone, foo)

        # delete notification
        await NotificationServices.delete(id=notification.id)

    print("Cron job finished...", datetime.now())
    print('-' * 10, '\n\n')


# Schedule your cron job function to run every 1 minute
cron_job_runner = crontab('*/1 * * * *', cron_job)
