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
    is_notification_time = time(6,00) < datetime.now().time()

    return (event_is_today and is_notification_time)

def get_event_color() -> str:
    # Returns a RBG color for event card in the emails

    colors = [
        "#1B5E20", "#FF6F00", "#1A237E", "#BF360C", "#01579B", "#33691E",
        "#880E4F", "#E65100", "#311B92", "#B71C1C", "#004D40", "#F57F17",
        "#0D47A1", "#827717", "#006064", "#4A148C", 
    ]

    return choice(colors)

def get_pronominal_particle(gender) -> str:
    if gender == 'M':
        return 'o'
    elif gender == 'F':
        return 'a'
    else:
        return 'ǝ'

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
    return "Fermi Notify - Conferma la registrazione"

def get_registration_mail_body(name: str, verification_code: str) -> str:
    body = ""

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

    return body



###          WELCOME EMAIL         ###

def get_welcome_mail_subject() -> str:
    return "Fermi Notify - Welcome!"

def get_welcome_mail_body(user: dict) -> str:
    body = ""
    
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

    return body



###     DAILY NOTIFICATION EMAIL    ###

def get_daily_notification_mail_subject(n_events: int) -> str:
    subject = f"Fermi Notify - Daily notification ({n_events} "
    subject += f"event{'i' if n_events > 1 else 'o'})"
    return subject
    

def get_daily_notification_mail_body(receiver: dict, events: list) -> str:
    body = ""

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

        body += i["subject"]

        # if event has same start and end date/time (es. entrata posticipata)
        if i["startDate"] == i["endDate"] and i["startDateTime"] == i["endDateTime"]:
            with open("emails/Daily-notification/07b.htm", encoding="utf8") as f:
                body += f.read()
            body += i["startDateTime"][11:16] if i["startDateTime"] else "/".join(i["startDate"].split("-")[::-1])
        # if event has same start date but different end date/time
        else:
            with open("emails/Daily-notification/07a.htm", encoding="utf8") as f:
                body += f.read()
            body += i["startDateTime"][11:16] if i["startDateTime"] else "/".join(i["startDate"].split("-")[::-1])
            with open("emails/Daily-notification/07a1.htm", encoding="utf8") as f:
                body += f.read()
            body += i["endDateTime"][11:16] if i["endDateTime"] else "/".join(i["endDate"].split("-")[::-1])

        with open("emails/Daily-notification/08.htm") as f:
            body += f.read()
        
    with open("emails/Daily-notification/09.htm") as f:
        body += f.read()

    return body


###    LAST MINUTE EMAIL NOTIFICATION    ###

def get_last_minute_notification_mail_subject():
    return "Fermi Notify - Last minute notification"

def get_last_minute_notification_mail_body(receiver: dict, events: list) -> str:
    body = ""

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

        body += i["subject"]

        # if event has same start and end date/time (es. entrata posticipata)
        if i["startDate"] == i["endDate"] and i["startDateTime"] == i["endDateTime"]:
            with open("emails/Last-minute-notification/06b.htm", encoding="utf8") as f:
                body += f.read()
            body += i["startDateTime"][11:16] if i["startDateTime"] else "/".join(i["startDate"].split("-")[::-1])
        # if event has same start date but different end date/time
        else:
            with open("emails/Last-minute-notification/06a.htm", encoding="utf8") as f:
                body += f.read()
            body += i["startDateTime"][11:16] if i["startDateTime"] else "/".join(i["startDate"].split("-")[::-1])
            with open("emails/Last-minute-notification/06a1.htm", encoding="utf8") as f:
                body += f.read()
            body += i["endDateTime"][11:16] if i["endDateTime"] else "/".join(i["endDate"].split("-")[::-1])

        with open("emails/Last-minute-notification/07.htm", encoding="utf8") as f:
            body += f.read()
        
    with open("emails/Last-minute-notification/08.htm", encoding="utf8") as f:
            body += f.read()

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

    body += f"""Ciao {receiver["name"]}, ecco il tuo daily roundup:\n"""

    for _ in events:
        body += f"""\n· `{_["subject"]}`"""

        # if event has same start and end date/time (es. entrata posticipata)
        if _["startDate"] == _["endDate"] and _["startDateTime"] == _["endDateTime"]:
            if _["startDateTime"] != None:
                body += "\n· *Orario* 📅 "
            else:
                body += "\n· *Data* 📅 "
            body += _["startDateTime"][11:16] if _["startDateTime"] else "/".join(_["startDate"].split("-")[::-1])
        # if event has same start date but different end date/time
        else:
            body += "\n· *Inizio* ⏰ "
            body += _["startDateTime"][11:16] if _["startDateTime"] else "/".join(_["startDate"].split("-")[::-1])
            body += "\n· *Fine* 🔚 "
            body += _["endDateTime"][11:16] if _["endDateTime"] else "/".join(_["endDate"].split("-")[::-1])
        
        body += "\n"
        
    body += "\nBuona giornata <3\n_Fermi Notify Team_\n"
    body += "master@ferminotify.me"

    return body


def get_last_minute_message(receiver: dict, events: list) -> str:
    # header
    body =  f"""Ciao {receiver["name"]},\nabbiamo trovato {len(events)} """
    body += f"event{'i' if len(events) > 1 else 'o'} dell'ultimo minuto:\n"

    for _ in events:
        body += f"""\n· `{_["subject"]}`"""

        # if event has same start and end date/time (es. entrata posticipata)
        if _["startDate"] == _["endDate"] and _["startDateTime"] == _["endDateTime"]:
            if _["startDateTime"] != None:
                body += "\n· *Orario* 📅 "
            else:
                body += "\n· *Data* 📅 "
            body += _["startDateTime"][11:16] if _["startDateTime"] else "/".join(_["startDate"].split("-")[::-1])
        # if event has same start date but different end date/time
        else:
            body += "\n· *Inizio* ⏰ "
            body += _["startDateTime"][11:16] if _["startDateTime"] else "/".join(_["startDate"].split("-")[::-1])
            body += "\n· *Fine* 🔚 "
            body += _["endDateTime"][11:16] if _["endDateTime"] else "/".join(_["endDate"].split("-")[::-1])
        body += "\n"
    # footer
    body += f"""\nTi auguriamo buon proseguimento di giornata.\n"""
    body += f"""_Fermi Notify Team_ \nmaster@ferminotify.me"""
    return body
