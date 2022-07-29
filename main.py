from src.databaseOperations import getSubscribers, db_notification
from src.telegramOperations import register_new_user, tg_notification
from src.emailOperations import *
from src.fermiCalendar import *
from src.utility import *

def deliver_notification(n):
    # This function delegates the operations to
    # be done when I decide to notify someone: 
    # send email, send messaage and store the 
    # notification
    email_notification(n)
    tg_notification(n)
    db_notification(n["id"], n["events"])

    return

def main(last_update_id):

    while True:
        ###           COLLECT SUBSCRIBERS DATA          ###
        subs = getSubscribers()
        
        ###           USER REGISTRATION EVENTS          ###
        pending_registration(subs)
        welcome_notification(subs)

        ###        TELEGRAM REGISTRATION EVENTS         ###
        last_update_id = register_new_user(subs, last_update_id)

        ###        COLLECT & SEND NOTIFICATIONS         ###
        notifications = collect_notifications(subs)
        for user in notifications:
            deliver_notification(user)

    return "merda."


if __name__ == "__main__":
    main(last_update_id=0)

'''

    >>> events sample
{'id': '5v2dkvq7mapnq7mp73610shqmn', 'subject': 'CLASSI 2ACH-2AME-2BCH-2CME-2DME - AULA 443 - CORSO RECUPERO MATEMATICA- PROF.MARCHI', 'desc': None, 'startDate': None, 'startDateTime': '2022-07-15T08:00:00+02:00', 'startTimeZone': 'Europe/Rome', 'endDate': None, 'endDateTime': '2022-07-15T10:00:00+02:00', 'endTimeZone': 'Europe/Rome'}
{'id': '54ftgsn23eig660jc0khu8cm68', 'subject': 'CLASSI 2AEL-2BEL-2DIN - AULA 443 - CORSO RECUPERO MATEMATICA- PROF.MARCHI', 'desc': None, 'startDate': None, 'startDateTime': '2022-07-15T10:00:00+02:00', 'startTimeZone': 'Europe/Rome', 'endDate': None, 'endDateTime': '2022-07-15T12:00:00+02:00', 'endTimeZone': 'Europe/Rome'}

    >>> sub sample
{'id': 7, 'name': 'Matteo', 'surname': 'Bini', 'email': 'mail@matteobini.me', 'telegram': 'BiniMatteo', 'tags': ['BINI', '4CIIN', 'OLIMPIADI', 'INFORMATICA'], 'n_not': 0}
{'id': 3, 'name': 'Ugo', 'surname': 'CgnmPrv', 'email': 'ugo3@matteobini.me', 'telegram': None, 'tags': None, 'n_not': None}

    >>> notifications 
[
    {
        'id': 10, 
        'name': 'Matteo', 
        'email': 'mail@matteobini.me', 
        'tg': 'BiniMatteo', 
        'events': 
        [
            {
                'id': '175kism1teadmku9if9q5kr969', 
                'subject': 'CLASSE 3AIIN - AULA 16 -CORSO RECUPERO INGLESE - PROF. MALAVASI MARIA', 
                'desc': None, 
                'startDate': None, 
                'startDateTime': '2022-07-19T12:00:00+02:00', 
                'startTimeZone': 'Europe/Rome', 
                'endDate': None, 
                'endDateTime': '2022-07-19T13:00:00+02:00', 
                'endTimeZone': 'Europe/Rome'
            }, 
            {
                'id': '6dm3upf29v1j784nqqc028am2f', 
                'subject': 'CLASSI 3AIIN - 3BIIN - AULA 28 - CORSO RECUPERO INFORMATICA - PROF. XHELILAJ', 
                'desc': None, 
                'startDate': None, 
                'startDateTime': '2022-07-20T10:00:00+02:00', 
                'startTimeZone': 'Europe/Rome', 
                'endDate': None, 
                'endDateTime': '2022-07-20T12:00:00+02:00', 
                'endTimeZone': 'Europe/Rome'
            },
            {
                'id': '40ig971tehasgqps56dk7bo2mo', 
                'subject': 'CLASSE 3AIIN - AULA 16 -CORSO RECUPERO INGLESE - PROF. MALAVASI MARIA', 
                'desc': None, 
                'startDate': None, 
                'startDateTime': '2022-07-21T12:00:00+02:00', 
                'startTimeZone': 'Europe/Rome', 
                'endDate': None, 
                'endDateTime': '2022-07-21T13:00:00+02:00', 
                'endTimeZone': 'Europe/Rome'
            }, 
            {
                'id': '40ig971tehasgqps56dk7bo2mo', 
                'subject': 'CLASSE 3AIIN - AULA 16 -CORSO RECUPERO INGLESE - PROF. MALAVASI MARIA', 
                'desc': None, 
                'startDate': None, 
                'startDateTime': '2022-07-21T12:00:00+02:00', 
                'startTimeZone': 'Europe/Rome', 
                'endDate': None, 
                'endDateTime': '2022-07-21T13:00:00+02:00', 
                'endTimeZone': 'Europe/Rome'
            }, 
            {
                'id': '40ig971tehasgqps56dk7bo2mo', 
                'subject': 'CLASSE 3AIIN - AULA 16 -CORSO RECUPERO INGLESE - PROF. MALAVASI MARIA', 
                'desc': None, 
                'startDate': None, 
                'startDateTime': '2022-07-21T12:00:00+02:00', 
                'startTimeZone': 'Europe/Rome', 
                'endDate': None, 
                'endDateTime': '2022-07-21T13:00:00+02:00', 
                'endTimeZone': 'Europe/Rome'
            }
        ]
    }
]

'''