# da riadattare.

import telepot
from dotenv import load_dotenv
import os
from random import randint
from datetime import datetime, time
from src.databaseOperations import updateTelegramId
from src.utility import * 

class Telegram:
    # Gestisce i rapporti con Telegram tramite le APIs

    def __init__(self):
        # Instaura la connessione configurando il bot
        
        load_dotenv()
        self.API_KEY = os.getenv('TELEGRAM_API_KEY')
        self.CHAT_ID = -1001512400920           # 3ciin chat id
        # self.CHAT_ID = 334908714              # matteo bini personal id
        
        self.bot=telepot.Bot(self.API_KEY)

    def chatNotification(self, message: dict):
        self.bot.sendMessage(message["receiver"], message["body"], parse_mode='MARKDOWN')
        return

    def user_welcome(self, telegram_id):
        self.chatNotification({ "receiver": telegram_id, "body": "Registrazione effettuata correttamente" })
    
    def register_new_user(self,last_update_id, subs):
        inboxMessages = self.bot.getUpdates(offset=last_update_id)
        for _ in inboxMessages:

            for i in subs:
                if _["message"]["text"] == i["telegram"]:
                    user_email = i["email"]
                    telegram_id = _["message"]["from"]["id"]

                    last_update_id = _["update_id"] if _["update_id"] > last_update_id else last_update_id

                    updateTelegramId(user_email, telegram_id)
                    self.user_welcome(telegram_id)

        return last_update_id

def schedule_message(notification: dict):
    message = {
        "receiver_id": notification["id"],
        "receiver": notification["telegram"],
        "uid": [],
        "isWelcome": False
    }

    for event in notification["events"]:
        message["uid"].append(event["id"])
        message["body"] = get_notification_tg_message(notification)
    
    TG = Telegram()
    TG.chatNotification(message)
    
    return


def last_minute_message(receiver: str, event: dict):
    message = {
        "receiver_id": receiver["id"],
        "receiver": receiver["tg"],
        "uid": [event["id"]],
        "isWelcome": False,
        "body": get_last_minute_message(receiver, event)
    }
    
    TG = Telegram()
    TG.chatNotification(message)
    
    return

def tg_notification(notification: dict):
    if str(notification["telegram"])[0] == '$':
        return

    for event in notification["events"]:
        if event["startDate"] != None:
            eventTime = event["startDate"]
        else:
            eventTime = event["startDateTime"]

        eventToday = str(datetime.fromisoformat(eventTime))[:9] == str(datetime.today())[:9]
        isSchoolHour = datetime.now().time() > time(8,10)
        isDaily =  time(7,55) < datetime.now().time() < time(8,10)

        if eventToday:
            if isDaily:
                schedule_message(notification)
                notification["events"].remove(event)
            elif isSchoolHour:
                receiver = {
                    "id": notification["id"],
                    "name": notification["name"],
                    "telegram": notification["tg"]
                }
                last_minute_message(receiver, event)
                notification["events"].remove(event)

    return

def register_new_user(subs, last_update_id):
    TG = Telegram()
    return TG.register_new_user(last_update_id, subs)
