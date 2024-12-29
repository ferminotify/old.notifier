from datetime import datetime, time, timedelta
import pytz
from copy import deepcopy

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

def is_event_today(event: dict, notification_day_before: bool, notification_time: time) -> bool:
    # Check if the notification has to be sent now (considering the 
    # current time and the datetime of the event)
    
    # Check if event is today
    if (not event["start.date"]) and (not event["start.dateTime"]):
        # In case there are no events today
        logger.debug("No events today.")
        return False

    if event["start.date"]:
        event_time = event["start.date"]
    else:
        event_time = event["start.dateTime"]
    event_is_today = str(datetime.fromisoformat(event_time))[:10] == str(datetime.today())[:10]

    # Check if I need to add the events of tomorrow
    event_is_tmrw = False
    if notification_day_before:
        event_is_tmrw = event_time[:10] == str(datetime.today() + timedelta(days=1))[:10]

    is_notification_time = datetime.now(pytz.timezone('Europe/Rome')).time() >= notification_time
    if notification_day_before:
        # se l'evento è di oggi allora invia last minute
        if event_is_today:
            is_notification_time = True
    
    logger.debug(f"{event['summary']} Add event to send list? Event is today: {event_is_today}, Event is tmrw: {event_is_tmrw}, Notification time: {is_notification_time}")

    return (event_is_today or event_is_tmrw) and is_notification_time

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


###          DAILY NOTIFICATION AND LAST MIN NOTIFICATION EMAIL         ###
def get_mail_notification_subject(n_events: int, is_daily: bool) -> str:
    if is_daily:
        subject = f"Daily notification ({n_events} "
        subject += f"event{'i' if n_events > 1 else 'o'})"
        logger.debug(f"Generated daily notification mail subject: {subject}")
        return subject
    else:
        return "Last minute notification"

def get_mail_notification_body(receiver: dict, events: list, is_daily: bool) -> str:
    body = ""
    try:

        # separate events of today and tomorrow
        events_tomorrow = []
        events_today = deepcopy(events)
        # move event from events to events_tomorrow if the event is tomorrow

        for event in events_today:
            if event.get('start.date') and datetime.strptime(event['start.date'], '%Y-%m-%d').date() == datetime.now().date() + timedelta(days=1):
                events_tomorrow.append(event)
                events_today.remove(event)
            elif event.get('start.dateTime') and datetime.strptime(event['start.dateTime'], '%Y-%m-%dT%H:%M:%S%z').date() == datetime.now().date() + timedelta(days=1):
                events_tomorrow.append(event)
                events_today.remove(event)

        giorns = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"]

        # data to render
        data = {
            'title': "Eventi previsti" if is_daily else "Nuovo evento",
            'greetings': "Ciao" if not is_daily else "Buongiorno" if datetime.now().hour < 12 else "Buon pomeriggio" if datetime.now().hour < 18 else "Buonasera",
            'name': receiver["name"],
            'gender': get_pronominal_particle(receiver["gender"]),
            'n_events': f"Sono previsti <b>{len(events)} eventi</b>" if len(events) > 1 else f"È previsto <b>{len(events)} evento</b>" if is_daily else f"Abbiamo trovato <b>{len(events)} nuovi eventi</b>" if len(events) > 1 else f"Abbiamo trovato <b>{len(events)} nuovo evento</b>",
            'events_today': events_today,
            'events_tomorrow': events_tomorrow,
            'date_today': f"{giorns[datetime.now().weekday()]} {datetime.now().strftime('%d/%m')}",
            'date_tomorrow': f"{giorns[(datetime.now() + timedelta(days=1)).weekday()]} {(datetime.now() + timedelta(days=1)).strftime('%d/%m')}",
        }

        # convert events date to dd-mm-yyyy and datetime to hh:mm
        for event in data['events_today'] + data['events_tomorrow']:
            if event.get('start.date'):
                event['start.date'] = datetime.strptime(event['start.date'], '%Y-%m-%d').strftime('%d/%m/%Y')
            if event.get('end.date'):
                event['end.date'] = datetime.strptime(event['end.date'], '%Y-%m-%d').strftime('%d/%m/%Y')
            if event.get('start.dateTime'):
                event['start.dateTime'] = datetime.strptime(event['start.dateTime'], '%Y-%m-%dT%H:%M:%S%z').strftime('%H:%M')
            if event.get('end.dateTime'):
                event['end.dateTime'] = datetime.strptime(event['end.dateTime'], '%Y-%m-%dT%H:%M:%S%z').strftime('%H:%M')

        template = env.get_template('mail_notification.min.html')
        body = template.render(data)

        logger.info(f"Generated notification mail body for {receiver['name']}.")
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

def get_tg_body(events: list) -> str:
    body = ""
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
    return body

def get_tg_message(receiver: dict, events: list, is_daily: bool) -> str:
    body = ""
    try:
        if is_daily:
            body += f"""Ciao {receiver["name"]}, ci sono degli eventi previsti:\n"""
        else:
            body += f"""Ciao {receiver["name"]},\nabbiamo trovato {len(events)} """
            body += f"event{'i' if len(events) > 1 else 'o'} dell'ultimo minuto:\n"

        # separate events of today and tomorrow
        events_tomorrow = []
        events_today = []

        for event in events:
            if event.get('start.date') and datetime.strptime(event['start.date'], '%Y-%m-%d').date() == datetime.now().date() + timedelta(days=1):
                events_tomorrow.append(event)
            elif event.get('start.dateTime') and datetime.strptime(event['start.dateTime'], '%Y-%m-%dT%H:%M:%S%z').date() == datetime.now().date() + timedelta(days=1):
                events_tomorrow.append(event)
            else:
                events_today.append(event)

        # convert events date to dd-mm-yyyy and datetime to hh:mm
        for event in events_today + events_tomorrow:
            if event.get('start.date'):
                event['start.date'] = datetime.strptime(event['start.date'], '%Y-%m-%d').strftime('%d/%m/%Y')
            if event.get('end.date'):
                event['end.date'] = datetime.strptime(event['end.date'], '%Y-%m-%d').strftime('%d/%m/%Y')
            if event.get('start.dateTime'):
                event['start.dateTime'] = datetime.strptime(event['start.dateTime'], '%Y-%m-%dT%H:%M:%S%z').strftime('%H:%M')
            if event.get('end.dateTime'):
                event['end.dateTime'] = datetime.strptime(event['end.dateTime'], '%Y-%m-%dT%H:%M:%S%z').strftime('%H:%M')

        giorns = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"]

        if len(events_today) > 0:
            body += f"\n*Oggi* {giorns[datetime.now().weekday()]} {datetime.now().strftime('%d/%m')}:\n"
            body += get_tg_body(events_today)

        if len(events_tomorrow) > 0:
            body += f"\n*Domani* {giorns[(datetime.now() + timedelta(days=1)).weekday()]} {(datetime.now() + timedelta(days=1)).strftime('%d/%m')}:\n"
            body += get_tg_body(events_tomorrow)
            
        if is_daily:
            body += "\nBuona giornata <3\n_Fermi Notify Team_\n"
        else:
            body += f"""\nTi auguriamo buon proseguimento di giornata.\n_Fermi Notify Team_\n"""
        body += "mail@fn.lkev.in"
        logger.debug(f"Generated daily notification Telegram message for {receiver['name']}.")
    except Exception as e:
        logger.error(f"Error generating daily notification Telegram message: {e}")
    return body