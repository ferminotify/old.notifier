import os
from datetime import datetime, time
from dotenv import load_dotenv
import telepot
from urllib3.exceptions import ReadTimeoutError
from time import sleep
import pytz
from datetime import timedelta

from src.utility import is_event_today
from src.logger import Logger
from src.databaseOperations import get_tg_offset, update_tg_offset, update_telegram_id
from src.utility import get_tg_message

logger = Logger()

"""
Summary of all the operations involving Telegram.
"""

###############################################
#                                             #
#                                             #
#               GENERAL PURPOSE               #
#                                             #
#                                             #
###############################################

class Telegram:
    """
    Class methods for the telegram operations.

    Such as:
    - Sending a notification to a chat
    - Sending a welcome message to a user
    - Registering a new user

    Attributes:
        API_KEY (str): The telegram API key.
        bot (telepot.Bot): The telegram bot.
    """

    def __init__(self):
        load_dotenv()
        self.API_KEY = os.getenv('TELEGRAM_API_KEY')
        self.bot = telepot.Bot(self.API_KEY)
        logger.debug("Telegram bot initialized with API key.")

    def chat_notification(self, message: dict) -> None:
        """Sends a notification to the chat through the bot.

        Args:
            message (dict): A dictionary containing the receiver's id and the message to be sent.
        """
        try:
            self.bot.sendMessage(
                message["receiver"], 
                message["body"], 
                parse_mode='MARKDOWN'
            )
            logger.info(f"Notification sent to {message['receiver']}.")
        except Exception as e:
            logger.error(f"Failed to send notification: {e}")

    def user_welcome(self, telegram_id: str) -> None:
        """Sends a welcome confirmation message to the user to notify him
        that the connection between the account id and the service
        has been established with success.

        Args:
            telegram_id (str): The user's telegram id.
        """
        self.chat_notification(message = {
            "receiver": telegram_id, 
            "body": "Registrazione effettuata correttamente. \nAbilita la notifica via telegram nella tua dashboard (https://fn.lkev.in/dashboard / https://ferminotify.sirico.dev/dashboard)" 
        })
        logger.info(f"Welcome message sent to {telegram_id}.")

    def safe_get_updates(self):
        retries = 3
        
        for i in range(retries):
            try:
                logger.debug(f"Attempt {i+1} to get updates.")
                updates = self.bot.getUpdates(offset=get_tg_offset())
                logger.debug("Successfully retrieved updates.")
                return updates
            except ReadTimeoutError:
                logger.warning(f"ReadTimeoutError on attempt {i+1}.")
                if i < retries - 1:
                    sleep(2 ** i)  # Exponential backoff
                    logger.debug(f"Retrying after {2 ** i} seconds.")
                else:
                    logger.error("Max retries reached. Raising exception.")
                    raise

    def register_new_telegram_user(self, subs: list[dict]) -> None:
        """Associates a telegram account to a subscriber of the service
        using a unique id.

        The id is received in the inbox of the telegram bot and if
        it is present in the database, the user is registered.

        Args:
            subs (list): A list of dictionaries containing the user's info.
        """
        try:
            inbox_messages = self.safe_get_updates()
        except Exception as e:
            logger.error(f"Error getting updates: {e}")
            return
        # inbox_messages = self.bot.getUpdates(offset=get_tg_offset())
        for message in inbox_messages:
            for sub in subs:
                # The next lines I check if I got messages from any
                # new user or some stranger (first 2 lines to check 
                # if I didn't get messages from groups, last one 
                # check for the message that i got from my new user)
                if "my_chat_member" not in message.keys():
                    try:
                        if ("new_chat_participant" not in message["message"]) and \
                            ("left_chat_participant" not in message["message"]) and \
                            ("document" not in message["message"].keys()):
                            if message["message"]["text"] == sub["telegram"]:
                                user_email = sub["email"]
                                telegram_id = message["message"]["from"]["id"]

                                update_tg_offset(message["update_id"])
                                update_telegram_id(user_email, telegram_id)
                                self.user_welcome(telegram_id)
                                logger.info(f"User {user_email} registered with telegram ID {telegram_id}.")
                    except Exception as e:
                        logger.error(f"Error processing message: {e}")
                        logger.error(f"Message causing error: {message}")

###############################################
#                                             #
#                                             #
#           HANDLE USER REGISTRATION          #
#                                             #
#                                             #
###############################################

def register_new_telegram_user(subs: list[dict]) -> None:
    """Associates a telegram account to a subscriber of the service.

    Args:
        subs (list): A list of dictionaries containing the user's info.
    """
    TG = Telegram()
    TG.register_new_telegram_user(subs)
    logger.info("New telegram user registration process completed.")

###############################################
#                                             #
#                                             #
#         USER NOTIFICATION MESSAGES          #
#                                             #
#                                             #
###############################################

def tg_notification(notification: dict) -> None:
    """Selects when to send the notification.

    The notification can be sent either daily or last minute.

    Args:
        notification (dict): dictionary containing all the events that a 
        subscriber need to be notified.
    """
    
    if str(notification["telegram"])[0] == 'X':
        # Exit the function when the user did not connect telegram.
        logger.info("User did not connect telegram. Exiting notification function.")
        return

    user = {
        "id": notification["id"],
        "name": notification["name"],
        "telegram": notification["telegram"],
        "n_time": notification["n_time"],
        "n_day": notification["n_day"]
    }
    message = {
        "receiver_id": user["id"],
        "receiver": user["telegram"],
    }

    # capire se daily o last min

    # convert user["n_time"] datetime.time to datetime object to add minutes
    user_datetime = datetime.combine(datetime.today(), user["n_time"])

    # daily notification time is between user n_time and n_time + 15 minutes
    is_dailynotification_time = user_datetime.time() <= datetime.now(pytz.timezone('Europe/Rome')).time() <= (user_datetime + timedelta(minutes=15)).time()
    is_lastminnotification_time = datetime.now(pytz.timezone('Europe/Rome')).time() > user_datetime.time()

    if user["n_day"]:
        # se l'evento è di oggi allora invia last minute
        # filtra gli eventi e lascia solo quelli di oggi
        today_not = [i for i in notification["events"] if is_event_today(i, True, user["n_time"])]
        # se è vuoto allora non inviare la mail, altrimenti invia last minute
        is_lastminnotification_time_send_today = len(today_not) > 0


    if is_dailynotification_time:
        message["body"] = get_tg_message(user, notification["events"], True)
        logger.info("Daily notification time. Preparing daily notification tg message.")
        TG = Telegram()
        TG.chat_notification(message)
        logger.info(f"Notification sent to user {user['id']}.")
    elif is_lastminnotification_time:
        message["body"] = get_tg_message(user, notification["events"], False)
        logger.info("Preparing last minute notification tg message.")
        TG = Telegram()
        TG.chat_notification(message)
        logger.info(f"Notification sent to user {user['id']}.")
    elif is_lastminnotification_time_send_today:
        message["body"] = get_tg_message(user, today_not, False)
        logger.info("Preparing last minute notification tg message.")
        TG = Telegram()
        TG.chat_notification(message)
        logger.info(f"Notification sent to user {user['id']}.")

    return