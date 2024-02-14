import requests
import json

from fastapi import APIRouter

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

    print('data', data)

    # Send POST request
    response = requests.post(url, data=data)

    # Print response
    print(response.status_code)
    print(response.text)
    return {'response': response.text, 'status': response.status_code}


if __name__ == '__main__':
    send_sms()
