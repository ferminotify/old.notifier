import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage

import os
from dotenv import load_dotenv

from datetime import datetime, time

from src.utility import *

class Email:

    def __init__(self):
        load_dotenv()
        EMAIL_PASSWORD = os.getenv('EMAIL_SERVICE_PASSWORD')
        PORT = 587
        self.client = smtplib.SMTP("smtp.zoho.eu", PORT)

        self.client.starttls()
        self.client.login("servizi@matteobini.me", EMAIL_PASSWORD)
        
        return

    def notifyAdmin(self, new_user):
        msg = EmailMessage()
        msg["Subject"] = "Nuovo iscritto Calendar Notifier"
        msg["From"] = "servizi@matteobini.me"
        msg["To"] = "servizi@matteobini.me"
        msg.set_content(f"Salve,\n{new_user} si e' iscritto.\n\nFermi Notifier Team")

        self.client.send_message(msg)

    def sendHTMLMail(self, receiver: str, subject: str, body: str, html_body: str):
        data = MIMEMultipart('alternative')
        data["Subject"] = subject
        data["From"] = "Eventi Calendario Giornaliero <servizi@matteobini.me>"
        data["To"] = receiver
        
        part1 = MIMEText(body, "plain")
        part2 = MIMEText(html_body, "html")
        data.attach(part1)
        data.attach(part2)
        
        self.client.sendmail("servizi@matteobini.me", receiver, data.as_string())

        return

    def closeConnection(self):
        self.client.quit()

        return

def send_email(email: dict):
    EM = Email()

    if email["isWelcome"]:
        EM.sendHTMLMail(
            email["Receiver"],
            "Registrazione completata a Fermi Notifier",
            "Registrazione completata. Visita servizi.matteobini.me/fermi-notifier . Per informazioni: servizi@matteobini.me",
            email["Body"]
        )
        EM.notifyAdmin(email["Receiver"])
        return EM.closeConnection()

    EM.sendHTMLMail(
        email["Receiver"],
        email["Subject"],
        email["Raw"],
        email["Body"]
    )
    EM.closeConnection()

    return 

def welcome_notification(subs):
    # Check for new users and send them the welcome
    # notification.

    for sub in subs:
        if sub["n_not"] == 0:
            email = {
                "Receiver": sub["email"],
                "Body": get_welcome_mail_body(sub["name"]),
                "isWelcome": True,
                "receiver_id": sub["id"]
            }
            send_email(email)
    
    return

def pending_registration(subs):
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
                "Subject": get_registration_mail_subject(sub["name"], verification_code),
                "Raw": get_registration_mail_raw(sub["name"], verification_code),
                "Body": get_registration_mail_body(sub["name"], verification_code),
            }

            send_email(email)
                        

    return


def last_minute_email(receiver: dict, event: dict):
    # Last minute email
    email = {
        "Receiver_id": receiver["id"],
        "Receiver": receiver["email"],
        "Uid": [event["id"]],
        "isWelcome": False
    }
    
    # last minute email
    email["Subject"] = get_last_minute_notification_mail_subject()
    email["Raw"] = get_last_minute_notification_mail_raw(receiver, event)
    email["Body"] = get_last_minute_notification_mail_body(receiver, event)
    
    send_email(email)
            

def schedule_email(notification: dict):
    email = {
        "Receiver_id": notification["id"],
        "Receiver": notification["email"],
        "Uid": [],
        "isWelcome": False
    }
    for event in notification["events"]:
        email["Uid"].append(event["id"])
        email["Subject"] = get_notification_mail_subject(notification)
        email["Raw"] = get_notification_mail_raw(notification)
        email["Body"] = get_notification_mail_body(notification)

    send_email(email)
    return

def email_notification(notification: dict):
    for event in notification["events"]:
        if event["startDate"] != None:
            eventTime = event["startDate"]
        else:
            eventTime = event["startDateTime"]

        eventToday = str(datetime.fromisoformat(eventTime))[:10] == str(datetime.today())[:10]
        isSchoolHour = datetime.now().time() > time(8,10)
        isDaily =  time(7,55) < datetime.now().time() < time(8,10)

        if eventToday:
            if isDaily:
                schedule_email(notification)
            elif isSchoolHour:
                receiver = {
                    "id": notification["id"],
                    "name": notification["name"],
                    "email": notification["email"]
                }
                last_minute_email(receiver, event)

    return
