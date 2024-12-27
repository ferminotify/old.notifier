import os
import time
from dotenv import load_dotenv
import psycopg2
from src.logger import Logger
logger = Logger()

"""
Summary of all the operations involving the database.
"""

class NotifierDB():
    """This class is used to connect to the database and perform
    operations on it regarding telegram and emails.

    In production, only the operations needed to request data will be used.
    The insertion of data will be done on the website.

    All the methods in this class don't close the connection to the database,
    in fact there are present specific functions named exactly alike outside
    of the class, that close the connection.

    Attributes:
        connection (psycopg2.extensions.connection): connection to the database.
        cursor (psycopg2.extensions.cursor): cursor to the database.
    """

    def __init__(self):
        load_dotenv(override=True)
        # Inizializzatore della connessione
        HOSTNAME = os.getenv('HOSTNAME')
        DATABASE = os.getenv('DATABASE')
        USERNAME = os.getenv('USERNAME')
        PASSWORD = os.getenv('PASSWORD')
        PORT_ID = os.getenv('PORT_ID')

        try:
            self.connection = psycopg2.connect(
                host=HOSTNAME,
                dbname=DATABASE,
                user=USERNAME,
                password=PASSWORD,
                port=PORT_ID,
            )
            logger.debug("Database connection established.")
        except Exception as e:
            logger.error(f"Error connecting to the database: {e}")
            time.sleep(30)
            NotifierDB()

        self.cursor = self.connection.cursor()

    def close_connection(self) -> None:
        """Closes the connection to the database."""
        self.connection.close()
        logger.debug("Database connection closed.")
        return

    def get_subscribers(self) -> list[tuple]:
        """Returns a list of all the subscribers in the database as a list of 
        tuples.

        Returns:
            list: list of tuples containing all the subscribers.
        """
        self.cursor.execute(f"SELECT * FROM subscribers")
        fetched_subscribers = self.cursor.fetchall()
        self.connection.commit()
        logger.debug("Fetched all subscribers from the database.")

        all_users = []
        for i in fetched_subscribers:
            user = {}
            user["id"] = i[0]
            user["name"] = i[1]
            user["surname"] = i[2]
            user["email"] = i[3]
            user["telegram"] = i[5]
            user["tags"] = i[6]
            user["n_not"] = i[7]
            user["gender"] = i[8]
            user["n_pref"] = i[9]
            user["n_time"] = i[10]
            
            all_users.append(user)

        return all_users

    def get_all_sent_id(self) -> list[int]:
        """Gets all the ids of sent notifications to a user.

        Args:
            user_id (str): id of the user.

        Returns:
            list: list of ids of sent notifications to the user.
        """
        self.cursor.execute("SELECT * FROM sent;")
        response = self.cursor.fetchall()
        self.connection.commit()
        logger.debug("Fetched all sent notification IDs from the database.")

        return response

    def increment_notification_number(self, user_id: int) -> None:
        """Increment the number of notifications of a user.

        Args:
            user_id (int): id of the user.
        """
        self.cursor.execute(f"""
            UPDATE subscribers
                SET notifications = notifications + 1
            WHERE id = {user_id};
        """)
        self.connection.commit()
        logger.debug(f"Incremented notification number for user ID {user_id}.")
        
        return

    def update_telegram_id(self, user_email: str, telegram_id: any) -> None:
        """Set the telegram id of a user using its email.

        Args:
            user_email (str): email of the user.
            telegram_id (any): telegram id of the user.
        """
        self.cursor.execute(f"""
            UPDATE subscribers
                SET telegram = '{telegram_id}'
            WHERE subscribers.email = '{user_email}';
        """)
        self.connection.commit()
        logger.debug(f"Updated telegram ID for user with email {user_email}.")
        return

    def store_event(self, user_id: int, event_id: str) -> None:
        """Store the notification in the database.

        Args:
            user_id (int): id of the user.
            event_id (int): id of the event.
        """
        pattern = "INSERT INTO sent(sub_id, evt) VALUES (%s, %s)"
        self.cursor.execute(pattern, (user_id, event_id))
        self.connection.commit()
        logger.debug(f"Stored event ID {event_id} for user ID {user_id}.")
        
        return

    def get_tg_offset(self) -> str:
        """Gets the offset of the telegram bot.

        Returns:
            str: offset of the telegram bot.
        """
        self.cursor.execute(f"SELECT * FROM stuff")
        response = self.cursor.fetchall()
        self.connection.commit()
        logger.debug("Fetched telegram offset from the database.")
        offset = ""

        for i in response:
            if i[0] == "telegram_offset":
                offset = i[1]

        return offset

    def update_tg_offset(self, last_update_id: any) -> int:
        """Updates the offset of the telegram bot.

        Args:
            last_update_id (any): id of the last update.
        """
        self.cursor.execute(f"""
            UPDATE stuff
                SET value = '{last_update_id}'
            WHERE key = 'telegram_offset';""")
        self.connection.commit()
        logger.debug(f"Updated telegram offset to {last_update_id}.")
        
        return

def store_sent_event(user_id: int, event_id: str) -> None:
    """Store sent notifications in the database.

    Args:
        user_id (int): id of the user.
        event_id (str): id of the event.
    """
    DB = NotifierDB()
    DB.store_event(user_id, event_id)
    DB.close_connection()
    logger.info(f"Stored sent event ID {event_id} for user ID {user_id}.")

    return

def get_all_sent_id() -> list[int]:
    """Get the id of the sent notifications of a user.

    Args:
        user_id (int): id of the user.

    Returns:
        list: list of the id of the sent notifications of the user.
    """
    DB = NotifierDB()
    k = DB.get_all_sent_id()
    DB.close_connection()
    logger.info("Fetched all sent notification IDs.")

    return k

def increment_notification_number(user_id: int) -> None:
    """Increment the number of notifications of a user.

    Args:
        user_id (int): id of the user.
    """
    DB = NotifierDB()
    DB.increment_notification_number(user_id)
    DB.close_connection()
    logger.info(f"Incremented notification number for user ID {user_id}.")
    return

def get_subscribers() -> list[dict]:
    """Get the list of the subscribers.

    returns:
        list: list of the subscribers.
    """
    DB = NotifierDB()
    k = DB.get_subscribers()
    DB.close_connection()
    logger.info("Fetched all subscribers.")

    return k

def update_telegram_id(user_email: str, telegram_id: any) -> None:
    """Set the telegram id of a user using its email.

    Args:
        user_email (str): email of the user.
        telegram_id (str): telegram id of the user.
    """
    DB = NotifierDB()
    DB.update_telegram_id(user_email, telegram_id)
    DB.close_connection()
    logger.info(f"Updated telegram ID for user with email {user_email}.")
    return

def store_notification(user_id: int, notified_events: list[dict]) -> None:
    """For each notified event, store the notification in the database
    and increment the number of notifications.

    Args:
        user_id (any): id of the user.
        notified_events (list): list of the notified events.
    """
    for event in notified_events:
        store_sent_event(user_id, event["uid"])
        increment_notification_number(user_id)
    logger.info(f"Stored notifications for user ID {user_id}.")
    return

def update_tg_offset(last_update_id: any) -> None:
    """Update the offset of the telegram bot.

    Args:
        last_update_id (int): id of the last update.
    """    
    DB = NotifierDB()
    DB.update_tg_offset(last_update_id)
    DB.close_connection()
    logger.info(f"Updated telegram offset to {last_update_id}.")
    
    return 

def get_tg_offset() -> str:
    """Get the offset of the telegram bot.

    Returns:
        int: offset of the telegram bot.
    """
    DB = NotifierDB()
    offset = DB.get_tg_offset()
    DB.close_connection()
    logger.info("Fetched telegram offset.")

    if offset == '':
        return
    else:
        return offset
