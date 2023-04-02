from app import firebase_admin
from app import db
from app.models import User
from firebase_admin import messaging


def send_notifications_to_all(title, messag):
    users = User.query.all()
    rtokens = []
    for u in users:
        if u.fcmtoken is not None:
            rtokens.append(u.fcmtoken)
    
    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title="CM4",
            body="Выход за пределы рабочей температуры!"
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