from src.databaseOperations import get_subscribers, store_notification
from src.emailOperations import pending_registration, welcome_notification, email_notification
from src.fermiCalendar import collect_notifications
from src.telegramOperations import register_new_telegram_user, tg_notification
from src.logger import Logger
logger = Logger()

import time
"""
Main.
"""


def deliver_notification(notification: dict) -> None:
    """This function delegates the notification delivery to the appropriate 
    functions.

    Such as:
    - Send email notification.
    - Send telegram notification.
    - Store the notification in the database.

    Args:
        notification (list): list of dictionaries containing all the 
        subscribers that need to be notified and
        the corresponding events.
    """
    if notification["n_pref"] == 3:
        email_notification(notification)
        tg_notification(notification)
        logger.info(f"Email and Telegram notification sent to {notification['email']}.")

    elif notification["n_pref"] == 2:
        email_notification(notification)
        logger.info(f"Email notification sent to {notification['email']}.")

    elif notification["n_pref"] == 1:
        tg_notification(notification)
        logger.info(f"Telegram notification sent to {notification['email']}.")

    elif notification["n_pref"] == 0:
        logger.info(f"No notification preference set for {notification['email']}.")

    store_notification(notification["id"], notification["events"])
    logger.info(f"Notification stored for user ID {notification['id']}.")
    return

def main():
    """Being the main function of the program, it will call all the other 
    functions.

    Such as:
    - Handling the pending registrations.
    - Collecting the notifications.
    - Deliver the notifications.
    """
    while True:
        # Collect all the subscribers data from the database
        logger.info("Collecting subscribers data...")
        subs = get_subscribers()

        logger.info("Handling pending registrations...")
        pending_registration(subs)  # Send the confirmation email
        logger.info("Sending welcome notifications...")
        welcome_notification(subs)  # Welcome the new users
        register_new_telegram_user(subs)

        # Collect all the new notifications
        logger.info("Collecting notifications...")
        notifications = collect_notifications(subs)
        logger.info(f"{len(notifications)} notifications collected.")
        for user in notifications:
            logger.info(f"Delivering notifications to {user['email']}...")
            deliver_notification(user)  # Deliver the notifications.
        time.sleep(600)
    return "fuck."


if __name__ == "__main__":
    main()
