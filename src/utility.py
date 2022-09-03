from datetime import datetime, time
from random import choice

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
    
    if (not event["startDate"]) and (not event["startDateTime"]):
        # In case there are no events today
        return False

    if event["startDate"]:
        event_time = event["startDate"]
    else:
        event_time = event["startDateTime"]
    event_is_today = str(datetime.fromisoformat(event_time))[:10] \
                    == str(datetime.today())[:10]
    is_notification_time = time(7,55) < datetime.now().time()

    return (event_is_today and is_notification_time)

###############################################
#                                             #
#                                             #
#                    EMAIL                    #
#                                             #
#                                             #
###############################################

###      MESSAGGIO DI CONFERMA ACCOUNT      ###

def get_registration_mail_subject() -> str:
    return "L'ultimo passaggio! - Completamento registrazione Fermi Notifier"

def get_registration_mail_raw(verification_code: str) -> str:
    return f"Visita questo sito: \
        servizi.matteobini.me/users/register/confirmation/{verification_code}"

def get_registration_mail_body(name, verification_code):
    body = ""

    with open("emails/confirm_registration-1.html") as f:
        lines = f.read()
        body += lines

    body += name

    with open("emails/confirm_registration-2.html") as f:
        lines = f.read()
        body += lines

    body += verification_code

    with open("emails/confirm_registration-3.html") as f:
        lines = f.read()
        body += lines

    body += verification_code

    with open("emails/confirm_registration-4.html") as f:
        lines = f.read()
        body += lines
    
    return body



###          MESSAGGIO DI BENVENUTO         ###

def get_welcome_mail_body(user: dict):
    body = ""
    with open("emails/welcome-1.html") as f:
        lines = f.read()
        body += lines

    body += user

    with open("emails/welcome-2.html") as f:
        lines = f.read()
        body += lines

    return body



###     MESSAGGIO DI NOTIFICA QUOTIDIANO    ###

def get_notification_mail_subject(receiver: dict, events: list):
    body = ""

    body += f"""Hai {len(events)} nuovi eventi sul Calendario Giornaliero - Daily update"""
    
    return body

def get_notification_mail_raw():
    return "Ci sono nuovi eventi che ti coinvolgono sul calendario giornaliero"

def get_notification_mail_body(receiver: dict, events: list):
    body = ""
    with open("emails/daily_notification-1.html") as f:
        lines = f.read()
        body += lines
    
    body += receiver["name"]

    with open("emails/daily_notification-2.html") as f:
        lines = f.read()
        body += lines

    body += str(len(events))

    with open("emails/daily_notification-3.html") as f:
        lines = f.read()
        body += lines

    for _ in events:
        body += "\n<li>Evento "
        body += str(events.index(_) + 1)
        body += "</code><ul><li><b>Nome: </b><code>"
        body += _["subject"]
        body += "</code></li><li><b>Orario di inizio: </b> <code>"
        if _["startDate"] != None:
            body += f"""{_["startDate"][8:9]}-{_["startDate"][5:6]}-{_["startDate"][:4]}"""
        else:
            body += f"""{_["startDateTime"][11:16]}"""
        body += "</code></li><li><b>Orario di fine: </b> <code>"
        if _["endDate"] != None:
            body += f"""{_["endDate"][8:9]}-{_["endDate"][5:6]}-{_["endDate"][:4]}"""
        else:
            body += f"""{_["endDateTime"][11:16]}"""
        body += "</code></li></ul></li>"

    with open("emails/daily_notification-4.html") as f:
        lines = f.read()
        body += lines

    return body



###    MESSAGGIO DI NOTIFICA LAST MINUTE    ###

def get_last_minute_notification_mail_body(receiver: dict, events: list):
    body = ""
    
    with open("emails/last_minute_notification-1.html") as f:
        lines = f.read()
        body += lines
    
    body += receiver["name"]

    with open("emails/last_minute_notification-2.html") as f:
        lines = f.read()
        body += lines
    
    body += f"""{len(events)} eventi dell'ultimo minuto: """

    for _ in events:
        with open("emails/last_minute_notification-2bis.html") as f:
            lines = f.read()
            body += lines
        
        body += _["subject"]
        
        with open("emails/last_minute_notification-3.html") as f:
            lines = f.read()
            body += lines
        
        if _["startDate"] != None:
            body += f"""{_["startDate"][8:9]}-{_["startDate"][5:6]}-{_["startDate"][:4]}"""
        else:
            body += f"""{_["startDateTime"][11:16]}"""
        
        with open("emails/last_minute_notification-4.html") as f:
            lines = f.read()
            body += lines

        if _["endDate"] != None:
            body += f"""{_["endDate"][8:9]}-{_["endDate"][5:6]}-{_["endDate"][:4]}"""
        else:
            body += f"""{_["endDateTime"][11:16]}"""

        body += "</code></li></ul>"

    with open("emails/last_minute_notification-5.html") as f:
        lines = f.read()
        body += lines

    return body


def get_last_minute_notification_mail_subject():
    return "Nuovo evento dal calendario giornaliero! - Last minute update"


def get_last_minute_notification_mail_raw(receiver: dict, events: list):
    return f"""Ciao {receiver["name"]}.\nAbbiamo trovato un eventi dell'ultimo minuto. Ti auguriamo buon proseguimento di giornata.\n\nFermi Notifier Team.\nservizi@matteobini.me\nservizi.matteobini.me"""


###############################################
#                                             #
#                                             #
#                  TELEGRAM                   #
#                                             #
#                                             #
###############################################

def get_notification_tg_message(receiver: dict, events: list):
    body = ""
    body += f"""Ciao {receiver["name"]}, ecco il tuo daily roundup\n"""
    for _ in events:
        body += f"""Nome evento: `{_["subject"]}`\n"""
        body += "*Inizio*: "
        if _["startDate"] != None:
            body += f"""`{_["startDate"][8:9]}-{_["startDate"][5:6]}-{_["startDate"][:4]}`\n"""
        else:
            body += f"""`{_["startDateTime"][11:16]}`\n"""
        
        body += "*Fine*: "

        if _["endDate"] != None:
            body += f"""`{_["endDate"][8:9]}-{_["endDate"][5:6]}-{_["endDate"][:4]}`"""
        else:
            body += f"""`{_["endDateTime"][11:16]}`"""

    body += f"""\n\Buona giornata <3\nFermi Notifier Team.\nservizi@matteobini.me"""

    return body


def get_last_minute_message(receiver: dict, events: list):
    # header
    body =  f"""Ciao {receiver["name"]}.\nAbbiamo trovato {len(events)} eventi dell'ultimo minuto:\n"""

    for _ in events:
        body += f"""*Titolo*: `{_["subject"]}` \n"""
    
        # date/time begin
        if _["startDate"] != None:
            body += f"""*Inizio*: `{_["startDate"][8:]}-{_["startDate"][5:6]}-{_["startDate"][:3]}` \n"""
        else:
            body += f"""*Inizio*: `{_["startDateTime"][11:16]}` \n"""
        
        # date/time end
        if _["endDate"] != None:
            body += f"""*Fine*: `{_["endDate"][8:]}-{_["endDate"][5:6]}-{_["endDate"][:3]}` \n"""
        else:
            body += f"""*Fine*: `{_["endDateTime"][11:16]}` \n\n"""

    # footer
    body += f"""Ti auguriamo buon proseguimento di giornata.\n\n_Fermi Notifier Team._ \nservizi@matteobini.me"""
    return body
