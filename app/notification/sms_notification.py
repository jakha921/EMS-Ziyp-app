import requests
import json

from fastapi import APIRouter

from cron.tasks import cron_job

router = APIRouter(
    prefix="/notification",
)


@router.get("/send-sms")
async def send_sms(number: str = None,
                   text: str = None,
                   ):
    # URL and endpoint
    url = 'http://83.69.139.182:8080'

    login = 'ziyoforum'
    password = '8j9Y3vHrMxgV'
    # number = '998913339636'
    # text = 'Hello, world!'

    # Data to be sent
    data = {
        'login': login,
        'password': password,
        'data': json.dumps([{'phone': number, 'text': text}])
    }

    # Send POST request
    response = requests.post(url, data=data)

    # Print response
    print('sms response', response)
    return {'response': response.text, 'status': response.status_code}


@router.get("/send-push-notification")
async def send_push_notification(token: str = None,
                                 title: str = None,
                                 body: str = None,
                                 ):
    return await send_push_notification(token=token, title=title, body=body)


@router.post("/update-notification", summary="Отправить уведомление о событии")
async def update_notification():
    return await cron_job()


if __name__ == '__main__':
    send_sms()
