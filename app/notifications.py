from app import firebase_admin
from app import db
from app.models import User, FCMtokens
from firebase_admin import messaging


def send_to_all(title, messag):
    fcm = FCMtokens.query.all()
    rtokens = []
    for u in fcm:
        rtokens.append(fcm.fcm_token)
    
    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=title,
            body=messag
        ),
        
        tokens = rtokens
    )

    respons = messaging.send_multicast(message)
    print('RESPONSE:', respons)
    return str(respons.success_count)

def send_one(title, messag):
    message = messaging.Message(
        notification=messaging.Notification(
            title="CM4",
            body="Выход за пределы рабочей температуры!"
        ),
        
        token="f0of08wWRAmBgBB9aEg-az:APA91bG4GnI8DPLGUH2Sl4aWVf6_8QWUebMGE_rUJPQTl1QSIdDN4FCTf0hGE-PNt61K5UXTrJBV7qEkziUr-yp3-MlBYjSiQu6DwbD3uksmH04RgURksPfSmgSqqYsu3gB3lrAyf7XR",
    )   

    response = messaging.send(message)
    return response