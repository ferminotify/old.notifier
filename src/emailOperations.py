import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage
import os
from dotenv import load_dotenv
from datetime import datetime, time
from src.utility import *
from src.databaseOperations import increment_notification_number


###############################################
#                                             #
#                                             #
#               GENERAL PURPOSE               #
#                                             #
#                                             #
###############################################

class Email:

    def __init__(self):
        load_dotenv()
        EMAIL_PASSWORD = os.getenv('EMAIL_SERVICE_PASSWORD')
        PORT = os.getenv('EMAIL_SERVICE_PORT')
        URL = os.getenv('EMAIL_SERVICE_URL')
        self.client = smtplib.SMTP(URL, PORT)

        self.client.starttls()
        self.client.login("servizi@matteobini.me", EMAIL_PASSWORD)
        
        return


    def notifyAdmin(self, new_user: str) -> None:
        msg = EmailMessage()
        msg["Subject"] = "Nuovo iscritto Calendar Notifier"
        msg["From"] = "Fermi Notifier Team <servizi@matteobini.me>"
        msg["To"] = "servizi@matteobini.me"
        msg.set_content(f"Salve,\n{new_user} si e' iscritto.\n\n\
                            Fermi Notifier Team")
        self.client.send_message(msg)
        
        return


    def sendHTMLMail(self, receiver: str, subject: str, 
                        body: str, html_body: str) -> None:
        data = MIMEMultipart('alternative')
        data["Subject"] = subject
        data["From"] = "Fermi Notifier Team <servizi@matteobini.me>"
        data["To"] = receiver
        
        part1 = MIMEText(body, "plain")
        part2 = MIMEText(html_body, "html")
        data.attach(part1)
        data.attach(part2)
        
        self.client.sendmail("servizi@matteobini.me", receiver, 
                                data.as_string())

        return


    def closeConnection(self) -> None:
        self.client.quit()

        return

def send_email(email: dict) -> None:
    EM = Email()

    if email["isWelcome"]:
        EM.notifyAdmin(email["Receiver"])

    EM.sendHTMLMail(
        email["Receiver"], email["Subject"],
        email["Raw"], email["Body"]
    )
    EM.closeConnection()

    return 



###############################################
#                                             #
#                                             #
#           USER REGISTRATION EMAILs          #
#                                             #
#                                             #
###############################################

def pending_registration(subs: list[dict]) -> None:
    # Check if there are users not yet fully registered 
    # (missing email confirmation)
    for sub in subs:
        if sub["n_not"] == -2:
            verification_code = sub["telegram"]

            email = {
                "Receiver_id": sub["id"],
                "Receiver": sub["email"],
                "Uid": ["conferma_registrazione"],
                "isWelcome": False,
                "Subject": get_registration_mail_subject(),
                "Raw": get_mail_raw(),
                "Body": get_registration_mail_body(sub["name"], 
                                                    verification_code),
            }

            send_email(email)
            increment_notification_number(sub["id"])

    return

def welcome_notification(subs: list[dict]) -> None:
    # Check for new users and send them the welcome notification.

    for sub in subs:
        # If the number of notifications is == 0 I have to send the welcome 
        # notification (because the user has just been properly registered)
        if sub["n_not"] == 0: 
            email = {
                "Receiver_id": sub["id"],
                "Receiver": sub["email"],
                "Subject": get_welcome_mail_subject(),
                "Raw": get_mail_raw(),
                "Body": get_welcome_mail_body(sub["name"]),
                "isWelcome": True,
                "receiver_id": sub["id"]
            }
            send_email(email)
            increment_notification_number(sub["id"])
    
    return



###############################################
#                                             #
#                                             #
#           USER NOTIFICATION EMAILs          #
#                                             #
#                                             #
###############################################

def daily_email(receiver: dict, events: list[dict]) -> None:
    # Set up email for daily roundup notification

    email = {
        "Receiver_id": receiver["id"],
        "Receiver": receiver["email"],
        "Uid": [],
        "isWelcome": False,
        "Subject": get_daily_notification_mail_subject(len(events)),
        "Raw": get_mail_raw(),
        "Body": get_daily_notification_mail_body(receiver, events)
    }

    for event in events:
        # Adding up the ids of all events that I 
        email["Uid"].append(event["id"])
        
    send_email(email)
    return


def last_minute_email(receiver: dict, events: list[dict]) -> None:

    # Set up email for last minute notification
    email = {
        "Receiver_id": receiver["id"],
        "Receiver": receiver["email"],
        "Uid": [],
        "isWelcome": False,
        "Subject": get_last_minute_notification_mail_subject(),
        "Raw": get_mail_raw(),
        "Body": get_last_minute_notification_mail_body(receiver, events)
    }

    for _ in events:
        email["Uid"].append(_["id"])

    send_email(email)
    return


def email_notification(notification: dict) -> None:
    # Check if I have to send the notification now

    # Get and check the current time slot
    isSchoolHour = datetime.now().time() > time(8,10)
    isDaily =  time(7,55) < datetime.now().time() < time(8,10)

    receiver = {
        "id": notification["id"],
        "name": notification["name"],
        "email": notification["email"]
    }

    if isDaily:
        daily_email(receiver, notification["events"])
    
    elif isSchoolHour:
        last_minute_email(receiver, notification["events"])

    return
