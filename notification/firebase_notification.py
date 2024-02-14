from firebase_admin import messaging, credentials, initialize_app

cred = credentials.Certificate("./ziyo-app-firebase-adminsdk-o5x20-92b88000ae.json")
initialize_app(cred)


async def send_push_notification(token: str, title: str, body: str):
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=token,
    )

    response = messaging.send(message)
    return {"response": response, 'status': response.status}
