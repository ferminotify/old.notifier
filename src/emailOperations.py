import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage
import os
from dotenv import load_dotenv
from src.utility import *
from src.databaseOperations import increment_notification_number
import imaplib
from datetime import datetime, time
import pytz
from src.logger import Logger
logger = Logger()
###############################################
#                                             #
#                                             #
#               GENERAL PURPOSE               #
#                                             #
#                                             #
###############################################

EMAIL_SENDER_INDEX = 0
class Email:

    sender_emails = [
        "master@fn.lkev.in",
    ]

    def __init__(self):
        global EMAIL_SENDER_INDEX
        load_dotenv()
        EMAIL_SERVICE_PASSWORD = os.getenv('EMAIL_SERVICE_PASSWORD')
        EMAIL_SERVICE_PORT = os.getenv('EMAIL_SERVICE_PORT')
        EMAIL_SERVICE_URL = os.getenv('EMAIL_SERVICE_URL')
        self.client = smtplib.SMTP(EMAIL_SERVICE_URL, EMAIL_SERVICE_PORT)
        self.client.starttls()
        self.client.login(self.sender_emails[EMAIL_SENDER_INDEX], EMAIL_SERVICE_PASSWORD)
        logger.debug("SMTP client initialized and started TLS.")

        return

    def __update_sender_index(self) -> None:
        global EMAIL_SENDER_INDEX
        EMAIL_SENDER_INDEX = 0

        """
        if EMAIL_SENDER_INDEX == 2:
            EMAIL_SENDER_INDEX = 0
        else:
            EMAIL_SENDER_INDEX += 1
        """

    def notify_admin(self, new_user: str) -> None:
        msg = EmailMessage()
        msg["Subject"] = "Nuovo iscritto Calendar Notifier"
        msg["From"] = \
            f"Fermi Notify Team <{self.sender_emails[EMAIL_SENDER_INDEX]}>"
        msg["To"] = "team@ferminotify.me"
        msg.set_content(f"Salve,\n{new_user} si e' iscritto.\n\n\
                            Fermi Notify Team")
        self.client.send_message(msg)
        logger.debug(f"Notification email sent to admin for new user: {new_user}.")
        self.__update_sender_index()
        self.save_mail(msg)
        
        return


    def sendHTMLMail(self, receiver: str, subject: str, 
                        body: str, html_body: str) -> None:
        global EMAIL_SENDER_INDEX
        data = MIMEMultipart('alternative')
        data["Subject"] = subject
        data["From"] = \
            f"Fermi Notify Team <{self.sender_emails[EMAIL_SENDER_INDEX]}>"
        data["To"] = receiver
        
        part1 = MIMEText(body, "plain")
        part2 = MIMEText(html_body, "html")
        data.attach(part1)
        data.attach(part2)
        
        self.client.sendmail(self.sender_emails[EMAIL_SENDER_INDEX], receiver,
                                data.as_string())
        logger.debug(f"HTML email sent to {receiver} with subject: {subject}.")

        self.__update_sender_index()
        self.save_mail(data)

        return
    
    def save_mail(self, msg) -> bool:
        try:
            imap_user = self.sender_emails[EMAIL_SENDER_INDEX]
            imap_password = os.getenv('EMAIL_SERVICE_PASSWORD')
            imap_server = os.getenv('EMAIL_SERVICE_URL')
            
            # Convert the message to bytes for IMAP appending
            email_bytes = msg.as_bytes()
            
            # Connect to IMAP and log in
            with imaplib.IMAP4_SSL(imap_server) as imap:
                imap.login(imap_user, imap_password)
                
                # Select the Sent folder. Adjust the folder name if needed (e.g., "Sent Items" or "[Gmail]/Sent Mail")
                sent_folder = "Sent"
                imap.select(sent_folder)

                # Make datetime object timezone-aware
                aware_datetime = datetime.now(pytz.utc)

                # Append the email to the Sent folder
                imap.append(sent_folder, '', imaplib.Time2Internaldate(aware_datetime), email_bytes)
                logger.debug("Email appended to Sent folder successfully.")

            return True
        except Exception as e:
            logger.error(f"Error saving email to IMAP: {e}")
            return False


    def closeConnection(self) -> None:
        self.client.quit()
        logger.debug("SMTP client connection closed.")
        return

def send_email(email: dict) -> None:
    EM = Email()
    logger.info(f"Sending email to {email['Receiver']} with subject: {email['Subject']}.")

    EM.sendHTMLMail(
        email["Receiver"], email["Subject"],
        email["Raw"], email["Body"]
    )
    EM.closeConnection()

    return 


def notify_admin(new_user: str) -> None:
    EM = Email()
    logger.info(f"Notifying admin about new user: {new_user}.")

    EM.notify_admin(new_user)
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
                "Subject": get_registration_mail_subject(),
                "Raw": get_mail_raw(),
                "Body": get_registration_mail_body(sub["name"], 
                                                    verification_code),
            }
            logger.info(f"Sending pending registration email to {sub['email']}.")
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
                "Body": get_welcome_mail_body(sub),
                "receiver_id": sub["id"]
            }
            logger.info(f"Sending welcome notification email to {sub['email']}.")
            send_email(email)
            increment_notification_number(sub["id"])
            notify_admin(email["Receiver"])
    
    return



###############################################
#                                             #
#                                             #
#           USER NOTIFICATION EMAIL           #
#                                             #
#                                             #
###############################################

def email_notification(notification: dict) -> None:
    # Check if I have to send the notification now

    user = {
        "id": notification["id"],
        "name": notification["name"],
        "email": notification["email"]
    }
    email = {
        "Receiver_id": user["id"],
        "Receiver": user["email"],
        "Raw": get_mail_raw(),
        "Uid": [i["uid"] for i in notification["events"]],
    }

    is_dailynotification_time =  time(6, 0) < datetime.now().time() < time(6, 15)
    has_school_started = datetime.now().time() > time(6, 15)

    if is_dailynotification_time:
        email["Subject"] = get_daily_notification_mail_subject(
                                                len(notification["events"]))
        email["Body"] = get_daily_notification_mail_body(user, 
                                                        notification["events"])
    
    elif has_school_started:
        email["Subject"] = get_last_minute_notification_mail_subject()
        email["Body"] = get_last_minute_notification_mail_body(user, 
                                                        notification["events"])

    logger.info(f"Sending notification email to {user['email']} with subject: {email['Subject']}.")
    send_email(email)   

    return
