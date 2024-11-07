from datetime import datetime, time
from random import choice

from src.logger import Logger
logger = Logger()

###############################################
#                                             #
#                                             #
#               GENERAL PURPOSE               #
#                                             #
#                                             #
###############################################

def is_event_today(event: dict) -> bool:
    # Check if the notification has to be sent now (considering the 
    # current time and the datetime of the event)
    
    if (not event["start.date"]) and (not event["start.dateTime"]):
        # In case there are no events today
        logger.debug("No events today.")
        return False

    if event["start.date"]:
        event_time = event["start.date"]
    else:
        event_time = event["start.dateTime"]
    event_is_today = str(datetime.fromisoformat(event_time))[:10] == str(datetime.today())[:10]
    is_notification_time = time(6,00) < datetime.now().time()

    logger.debug(f"Event is today: {event_is_today}, Notification time: {is_notification_time}")
    return (event_is_today and is_notification_time)

def get_event_color() -> str:
    # Returns a RBG color for event card in the emails

    colors = [
        "#1B5E20", "#FF6F00", "#1A237E", "#BF360C", "#01579B", "#33691E",
        "#880E4F", "#E65100", "#311B92", "#B71C1C", "#004D40", "#F57F17",
        "#0D47A1", "#827717", "#006064", "#4A148C", 
    ]

    color = choice(colors)
    logger.debug(f"Selected event color: {color}")
    return color

def get_pronominal_particle(gender) -> str:
    if gender == 'M':
        particle = 'o'
    elif gender == 'F':
        particle = 'a'
    else:
        particle = 'ǝ'
    logger.debug(f"Selected pronominal particle for gender {gender}: {particle}")
    return particle

def get_mail_raw() -> str:
    return "Ci sono nuovi eventi che ti coinvolgono sul calendario giornaliero"

###############################################
#                                             #
#                                             #
#                    EMAIL                    #
#                                             #
#                                             #
###############################################

###      ACCOUNT CONFIRMATION EMAIL      ###

def get_registration_mail_subject() -> str:
    subject = "Fermi Notify - Conferma la registrazione"
    return subject

def get_registration_mail_body(name: str, verification_code: str) -> str:
    body = ""
    try:

        with open("emails/Confirm-registration/01.htm") as f:
            body += f.read()

        body += name

        with open("emails/Confirm-registration/02.htm") as f:
            body += f.read()

        body += verification_code

        with open("emails/Confirm-registration/03.htm") as f:
            body += f.read()

        body += verification_code

        with open("emails/Confirm-registration/04.htm") as f:
            body += f.read()
        
        body += verification_code

        with open("emails/Confirm-registration/05.htm") as f:
            body += f.read()

        logger.debug(f"Generated registration mail body for {name}.")
    except Exception as e:
        logger.error(f"Error generating registration mail body: {e}")
    return body



###          WELCOME EMAIL         ###

def get_welcome_mail_subject() -> str:
    subject = "Fermi Notify - Welcome!"
    return subject

def get_welcome_mail_body(user: dict) -> str:
    body = ""
    try:
        with open("emails/Welcome/01.htm") as f:
            body += f.read()

        body += user["name"]

        with open("emails/Welcome/02.htm") as f:
            body += f.read()

        body += get_pronominal_particle(user["gender"])

        with open("emails/Welcome/03.htm") as f:
            body += f.read()

        body += get_pronominal_particle(user["gender"])
        
        with open("emails/Welcome/04.htm") as f:
            body += f.read()

        body += get_pronominal_particle(user["gender"])

        with open("emails/Welcome/05.htm") as f:
            body += f.read()
    except Exception as e:
        logger.error(f"Error generating welcome mail body: {e}")
    return body



###     DAILY NOTIFICATION EMAIL    ###

def get_daily_notification_mail_subject(n_events: int) -> str:
    subject = f"Fermi Notify - Daily notification ({n_events} "
    subject += f"event{'i' if n_events > 1 else 'o'})"
    logger.debug(f"Generated daily notification mail subject: {subject}")
    return subject
    

def get_daily_notification_mail_body(receiver: dict, events: list) -> str:
    body = ""
    try:
        with open("emails/Daily-notification/01.htm") as f:
            body += f.read()
        
        body += receiver["name"]

        with open("emails/Daily-notification/02.htm") as f:
            body += f.read()

        body += "è previsto <b>" if len(events) == 1 else "sono previsti <b>"

        body += str(len(events))

        with open("emails/Daily-notification/03.htm") as f:
            body += f.read()

        body += "o" if len(events) == 1 else "i"

        with open("emails/Daily-notification/04.htm") as f:
            body += f.read()

        for i in events:
            card_color = get_event_color()

            with open("emails/Daily-notification/05.htm") as f:
                body += f.read()

            body += card_color

            with open("emails/Daily-notification/06.htm", encoding="utf8") as f:
                body += f.read()

            body += i["summary"]

            # if event has same start and end date/time (es. entrata posticipata)
            if i["start.date"] == i["end.date"] and i["start.dateTime"] == i["end.dateTime"]:
                with open("emails/Daily-notification/07b.htm", encoding="utf8") as f:
                    body += f.read()
                body += i["start.dateTime"][11:16] if i["start.dateTime"] else "/".join(i["start.date"].split("-")[::-1])
            # if event has same start date but different end date/time
            else:
                with open("emails/Daily-notification/07a.htm", encoding="utf8") as f:
                    body += f.read()
                body += i["start.dateTime"][11:16] if i["start.dateTime"] else "/".join(i["start.date"].split("-")[::-1])
                with open("emails/Daily-notification/07a1.htm", encoding="utf8") as f:
                    body += f.read()
                body += i["end.dateTime"][11:16] if i["end.dateTime"] else "/".join(i["end.date"].split("-")[::-1])

            with open("emails/Daily-notification/08.htm") as f:
                body += f.read()
            
        with open("emails/Daily-notification/09.htm") as f:
            body += f.read()

        logger.debug(f"Generated daily notification mail body for {receiver['name']}.")
    except Exception as e:
        logger.error(f"Error generating daily notification mail body: {e}")
    return body


###    LAST MINUTE EMAIL NOTIFICATION    ###

def get_last_minute_notification_mail_subject():
    subject = "Fermi Notify - Last minute notification"
    return subject

def get_last_minute_notification_mail_body(receiver: dict, events: list) -> str:
    body = ""
    try:
        with open("emails/Last-minute-notification/01.htm", encoding="utf8") as f:
            body += f.read()
        
        body += receiver["name"]

        with open("emails/Last-minute-notification/02.htm", encoding="utf8") as f:
            body += f.read()

        body += str(len(events))
        body += "</b> evento" if len(events) == 1 else "</b> eventi"

        with open("emails/Last-minute-notification/03.htm", encoding="utf8") as f:
            body += f.read()

        for i in events:
            card_color = get_event_color()

            with open("emails/Last-minute-notification/04.htm", encoding="utf8") as f:
                body += f.read()

            body += card_color

            with open("emails/Last-minute-notification/05.htm", encoding="utf8") as f:
                body += f.read()

            body += i["summary"]

            # if event has same start and end date/time (es. entrata posticipata)
            if i["start.date"] == i["end.date"] and i["start.dateTime"] == i["end.dateTime"]:
                with open("emails/Last-minute-notification/06b.htm", encoding="utf8") as f:
                    body += f.read()
                body += i["start.dateTime"][11:16] if i["start.dateTime"] else "/".join(i["start.date"].split("-")[::-1])
            # if event has same start date but different end date/time
            else:
                with open("emails/Last-minute-notification/06a.htm", encoding="utf8") as f:
                    body += f.read()
                body += i["start.dateTime"][11:16] if i["start.dateTime"] else "/".join(i["start.date"].split("-")[::-1])
                with open("emails/Last-minute-notification/06a1.htm", encoding="utf8") as f:
                    body += f.read()
                body += i["end.dateTime"][11:16] if i["end.dateTime"] else "/".join(i["end.date"].split("-")[::-1])

            with open("emails/Last-minute-notification/07.htm", encoding="utf8") as f:
                body += f.read()
            
        with open("emails/Last-minute-notification/08.htm", encoding="utf8") as f:
                body += f.read()

        logger.debug(f"Generated last minute notification mail body for {receiver['name']}.")
    except Exception as e:
        logger.error(f"Error generating last minute notification mail body: {e}")
    return body


###############################################
#                                             #
#                                             #
#                  TELEGRAM                   #
#                                             #
#                                             #
###############################################

def get_daily_notification_tg_message(receiver: dict, events: list) -> str:
    body = ""
    try:
        body += f"""Ciao {receiver["name"]}, ecco il tuo daily roundup:\n"""

        for _ in events:
            body += f"""\n· `{_["summary"]}`"""

            # if event has same start and end date/time (es. entrata posticipata)
            if _["start.date"] == _["end.date"] and _["start.dateTime"] == _["end.dateTime"]:
                if _["start.dateTime"] != None:
                    body += "\n· *Orario* 📅 "
                else:
                    body += "\n· *Data* 📅 "
                body += _["start.dateTime"][11:16] if _["start.dateTime"] else "/".join(_["start.date"].split("-")[::-1])
            # if event has same start date but different end date/time
            else:
                body += "\n· *Inizio* ⏰ "
                body += _["start.dateTime"][11:16] if _["start.dateTime"] else "/".join(_["start.date"].split("-")[::-1])
                body += "\n· *Fine* 🔚 "
                body += _["end.dateTime"][11:16] if _["end.dateTime"] else "/".join(_["end.date"].split("-")[::-1])
            
            body += "\n"
            
        body += "\nBuona giornata <3\n_Fermi Notify Team_\n"
        body += "master@ferminotify.me"
        logger.debug(f"Generated daily notification Telegram message for {receiver['name']}.")
    except Exception as e:
        logger.error(f"Error generating daily notification Telegram message: {e}")
    return body


def get_last_minute_message(receiver: dict, events: list) -> str:
    # header
    body = ""
    try:
        body +=  f"""Ciao {receiver["name"]},\nabbiamo trovato {len(events)} """
        body += f"event{'i' if len(events) > 1 else 'o'} dell'ultimo minuto:\n"

        for _ in events:
            body += f"""\n· `{_["summary"]}`"""

            # if event has same start and end date/time (es. entrata posticipata)
            if _["start.date"] == _["end.date"] and _["start.dateTime"] == _["end.dateTime"]:
                if _["start.dateTime"] != None:
                    body += "\n· *Orario* 📅 "
                else:
                    body += "\n· *Data* 📅 "
                body += _["start.dateTime"][11:16] if _["start.dateTime"] else "/".join(_["start.date"].split("-")[::-1])
            # if event has same start date but different end date/time
            else:
                body += "\n· *Inizio* ⏰ "
                body += _["start.dateTime"][11:16] if _["start.dateTime"] else "/".join(_["start.date"].split("-")[::-1])
                body += "\n· *Fine* 🔚 "
                body += _["end.dateTime"][11:16] if _["end.dateTime"] else "/".join(_["end.date"].split("-")[::-1])
            body += "\n"
        # footer
        body += f"""\nTi auguriamo buon proseguimento di giornata.\n"""
        body += f"""_Fermi Notify Team_ \nmaster@ferminotify.me"""
        
        logger.debug(f"Generated last minute Telegram message for {receiver['name']}.")
    except Exception as e:
        logger.error(f"Error generating last minute Telegram message: {e}")
    return body
