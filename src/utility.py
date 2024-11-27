from datetime import datetime, time

from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('src/email_templates'))

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
    subject = "Conferma la registrazione"
    return subject

def get_registration_mail_body(name: str, verification_code: str, gender: str) -> str:
    body = ""
    try:

        template = env.get_template('confirm.min.html')

        data = {
            'name': name,
            'verification_code': verification_code,
            'gender': get_pronominal_particle(gender)
        }

        body = template.render(data)

        logger.debug(f"Generated registration mail body for {name}.")
    except Exception as e:
        logger.error(f"Error generating registration mail body: {e}")
    return body



###          WELCOME EMAIL         ###

def get_welcome_mail_subject() -> str:
    subject = "Welcome!"
    return subject

def get_welcome_mail_body(user: dict) -> str:
    body = ""
    try:
            template = env.get_template('welcome.min.html')
            data = {
                'name': user["name"],
                'gender': get_pronominal_particle(user["gender"])
            }
            body = template.render(data)
    except Exception as e:
        logger.error(f"Error generating welcome mail body: {e}")
    return body



###     DAILY NOTIFICATION EMAIL    ###

def get_daily_notification_mail_subject(n_events: int) -> str:
    subject = f"Daily notification ({n_events} "
    subject += f"event{'i' if n_events > 1 else 'o'})"
    logger.debug(f"Generated daily notification mail subject: {subject}")
    return subject
    

def get_daily_notification_mail_body(receiver: dict, events: list) -> str:
    body = ""
    try:
        data = {
            'name': receiver["name"],
            'gender': get_pronominal_particle(receiver["gender"]),
            'n_events': f"{len(events)} eventi" if len(events) > 1 else f"{len(events)} evento",
            'events': events
        }
        template = env.get_template('daily.min.html')
        body = template.render(data)

        logger.debug(f"Generated daily notification mail body for {receiver['name']}.")
    except Exception as e:
        logger.error(f"Error generating daily notification mail body: {e}")
    return body


###    LAST MINUTE EMAIL NOTIFICATION    ###

def get_last_minute_notification_mail_subject():
    subject = "Last minute notification"
    return subject

def get_last_minute_notification_mail_body(receiver: dict, events: list) -> str:
    body = ""
    try:
        # Initialize the data dictionary
        data = {
            'name': receiver["name"],
            'gender': get_pronominal_particle(receiver["gender"]),
            'n_events': f"{len(events)} nuovi eventi" if len(events) > 1 else f"{len(events)} nuovo evento",
            'events': events
        }

        # Render the template with the data
        template = env.get_template('lastminute.min.html')
        body = template.render(data)

        logger.info(f"Generated last minute notification mail body for {receiver['name']}.")
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
                body += _["start.dateTime"] if _["start.dateTime"] else _["start.date"]
            # if event has same start date but different end date/time
            else:
                body += "\n· *Inizio* ⏰ "
                body += _["start.dateTime"] if _["start.dateTime"] else _["start.date"]
                body += "\n· *Fine* 🔚 "
                body += _["end.dateTime"] if _["end.dateTime"] else _["end.date"]
            
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
                body += _["start.dateTime"] if _["start.dateTime"] else _["start.date"]
            # if event has same start date but different end date/time
            else:
                body += "\n· *Inizio* ⏰ "
                body += _["start.dateTime"] if _["start.dateTime"] else _["start.date"]
                body += "\n· *Fine* 🔚 "
                body += _["end.dateTime"] if _["end.dateTime"] else _["end.date"]
            body += "\n"
        # footer
        body += f"""\nTi auguriamo buon proseguimento di giornata.\n"""
        body += f"""_Fermi Notify Team_ \nmaster@ferminotify.me"""
        
        logger.debug(f"Generated last minute Telegram message for {receiver['name']}.")
    except Exception as e:
        logger.error(f"Error generating last minute Telegram message: {e}")
    return body
