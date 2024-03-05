from firebase_admin import messaging, credentials, initialize_app, exceptions

cred = credentials.Certificate("notification/ziyo-app-31b68-firebase-adminsdk-b5m2u-15606366ff.json")
initialize_app(cred)


async def send_push_notification(token: str, title: str, body: str):
    try:
        if token:
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body,
                ),
                token=token,
            )

            response = messaging.send(message)
            return {"response": response}
    except exceptions.InvalidArgumentError as e:
        # Handle the error here
        print("Caught InvalidArgumentError:", e)
