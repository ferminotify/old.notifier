from datetime import datetime

###############################################
#                                             #
#                                             #
#                    EMAIL                    #
#                                             #
#                                             #
###############################################

###      MESSAGGIO DI CONFERMA ACCOUNT      ###

def get_registration_mail_subject(name, verification_code):
    return "L'ultimo passaggio! - Completamento registrazione Fermi Notifier"

def get_registration_mail_raw(name, verification_code):
    body = f"Visita questo sito: https://servizi.matteobini.me/users/register/confirmation/{verification_code}"
    
    return body

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

###          MESSAGGIO DI NOTIFICA          ###

def get_notification_mail_subject(notification: dict):
    body = ""

    body += f"""Hai {len(notification["events"])} nuovi eventi sul Calendario Giornaliero - Daily update"""
    
    return body


def get_notification_mail_raw(notification: dict):
    return "Ci sono nuovi eventi che ti coinvolgono sul calendario giornaliero"


def get_notification_mail_body(notification: dict):
    body = ""
    with open("emails/daily_notification-1.html") as f:
        lines = f.read()
        body += lines
    
    body += notification["name"]

    with open("emails/daily_notification-2.html") as f:
        lines = f.read()
        body += lines

    body += str(len(notification["events"]))

    with open("emails/daily_notification-3.html") as f:
        lines = f.read()
        body += lines

    for _ in notification["events"]:
        body += "\n<li>Evento "
        body += str(notification["events"].index(_) + 1)
        body += "</code><ul><li><b>Nome:</b><code>"
        body += _["subject"]
        body += "</code></li><li><b>Orario di inizio:</b> <code>"
        if _["startDate"] != None:
            body += f"""{_["startDate"][8:9]}-{_["startDate"][5:6]}-{_["startDate"][:4]}"""
        else:
            body += f"""{_["startDateTime"][11:16]}"""
        body += "</code></li><li><b>Orario di fine:</b> <code>"
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

def get_last_minute_notification_mail_body(receiver: dict, event: dict):
    body = ""
    
    with open("emails/last_minute_notification-1.html") as f:
        lines = f.read()
        body += lines
    
    body += receiver["name"]

    with open("emails/last_minute_notification-2.html") as f:
        lines = f.read()
        body += lines
    
    body += event["subject"]

    with open("emails/last_minute_notification-3.html") as f:
        lines = f.read()
        body += lines
    
    if event["startDate"] != None:
        body += f"""{event["startDate"][8:9]}-{event["startDate"][5:6]}-{event["startDate"][:4]}"""
    else:
        body += f"""{event["startDateTime"][11:16]}"""
    
    with open("emails/last_minute_notification-4.html") as f:
        lines = f.read()
        body += lines

    if event["endDate"] != None:
        body += f"""{event["endDate"][8:9]}-{event["endDate"][5:6]}-{event["endDate"][:4]}"""
    else:
        body += f"""{event["endDateTime"][11:16]}"""

    with open("emails/last_minute_notification-5.html") as f:
        lines = f.read()
        body += lines

    return body


def get_last_minute_notification_mail_subject():
    return "Nuovo evento dal calendario giornaliero! - Last minute update"


def get_last_minute_notification_mail_raw(receiver: dict, event: dict):
    return f"""Ciao {receiver["name"]}.\nAbbiamo trovato un evento all'ultimo minuto:\n{event["subject"]}\nInizio: {event["startDateTime"]} / {event["startDate"]}\nFine: {event["endDateTime"]} / {event["endDate"]}\n. Ti auguriamo buon proseguimento di giornata.\n\nFermi Notifier Team.\nservizi@matteobini.me\nservizi.matteobini.me"""


###############################################
#                                             #
#                                             #
#                  TELEGRAM                   #
#                                             #
#                                             #
###############################################

def get_notification_tg_message(notification: dict):
    body = ""
    body += f"""Ciao {notification["name"]}, ecco il tuo daily roundup\n"""
    for _ in notification["events"]:
        body += f"""Nome evento: {_["subject"]}\n"""
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

    body += f"""\n\Buona giornata <3\nFermi Notifier Team.\nservizi@matteobini.me"""

    return



def get_last_minute_message(receiver: dict, event: dict):
    return f"""Ciao {receiver["name"]}.\nAbbiamo trovato un evento all'ultimo minuto:\n{event["subject"]}\nInizio: {event["startDateTime"]} / {event["startDate"]}\nFine: {event["endDateTime"]} / {event["endDate"]}\n. Ti auguriamo buon proseguimento di giornata.\n\nFermi Notifier Team.\nservizi@matteobini.me"""
