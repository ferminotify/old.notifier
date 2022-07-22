from datetime import time

from src.databaseOperations import incrementNumNot, getSubscribers
from src.telegramOperations import register_new_user, tg_notification
from src.emailOperations import *
from src.fermiCalendar import *
from src.utility import *

def main(last_update_id):

    while True:
        subs = getSubscribers()
        notifications = collect_notifications(subs)

        welcome_notification(subs)
        last_update_id = register_new_user(subs, last_update_id)

        for n in notifications:
            email_notification(n)
            tg_notification(n)

    return "D'fuq"


if __name__ == "__main__":
    main(last_update_id=0)

'''

    >>> events sample
{'id': '5v2dkvq7mapnq7mp73610shqmn', 'subject': 'CLASSI 2ACH-2AME-2BCH-2CME-2DME - AULA 443 - CORSO RECUPERO MATEMATICA- PROF.MARCHI', 'desc': nan, 'startDate': nan, 'startDateTime': '2022-07-15T08:00:00+02:00', 'startTimeZone': 'Europe/Rome', 'endDate': nan, 'endDateTime': '2022-07-15T10:00:00+02:00', 'endTimeZone': 'Europe/Rome'}
{'id': '54ftgsn23eig660jc0khu8cm68', 'subject': 'CLASSI 2AEL-2BEL-2DIN - AULA 443 - CORSO RECUPERO MATEMATICA- PROF.MARCHI', 'desc': nan, 'startDate': nan, 'startDateTime': '2022-07-15T10:00:00+02:00', 'startTimeZone': 'Europe/Rome', 'endDate': nan, 'endDateTime': '2022-07-15T12:00:00+02:00', 'endTimeZone': 'Europe/Rome'}

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
                'desc': nan, 
                'startDate': nan, 
                'startDateTime': '2022-07-19T12:00:00+02:00', 
                'startTimeZone': 'Europe/Rome', 
                'endDate': nan, 
                'endDateTime': '2022-07-19T13:00:00+02:00', 
                'endTimeZone': 'Europe/Rome'
            }, 
            {
                'id': '6dm3upf29v1j784nqqc028am2f', 
                'subject': 'CLASSI 3AIIN - 3BIIN - AULA 28 - CORSO RECUPERO INFORMATICA - PROF. XHELILAJ', 
                'desc': nan, 
                'startDate': nan, 
                'startDateTime': '2022-07-20T10:00:00+02:00', 
                'startTimeZone': 'Europe/Rome', 
                'endDate': nan, 
                'endDateTime': '2022-07-20T12:00:00+02:00', 
                'endTimeZone': 'Europe/Rome'
            },
            {
                'id': '40ig971tehasgqps56dk7bo2mo', 
                'subject': 'CLASSE 3AIIN - AULA 16 -CORSO RECUPERO INGLESE - PROF. MALAVASI MARIA', 
                'desc': nan, 
                'startDate': nan, 
                'startDateTime': '2022-07-21T12:00:00+02:00', 
                'startTimeZone': 'Europe/Rome', 
                'endDate': nan, 
                'endDateTime': '2022-07-21T13:00:00+02:00', 
                'endTimeZone': 'Europe/Rome'
            }, 
            {
                'id': '40ig971tehasgqps56dk7bo2mo', 
                'subject': 'CLASSE 3AIIN - AULA 16 -CORSO RECUPERO INGLESE - PROF. MALAVASI MARIA', 
                'desc': nan, 
                'startDate': nan, 
                'startDateTime': '2022-07-21T12:00:00+02:00', 
                'startTimeZone': 'Europe/Rome', 
                'endDate': nan, 
                'endDateTime': '2022-07-21T13:00:00+02:00', 
                'endTimeZone': 'Europe/Rome'
            }, 
            {
                'id': '40ig971tehasgqps56dk7bo2mo', 
                'subject': 'CLASSE 3AIIN - AULA 16 -CORSO RECUPERO INGLESE - PROF. MALAVASI MARIA', 
                'desc': nan, 
                'startDate': nan, 
                'startDateTime': '2022-07-21T12:00:00+02:00', 
                'startTimeZone': 'Europe/Rome', 
                'endDate': nan, 
                'endDateTime': '2022-07-21T13:00:00+02:00', 
                'endTimeZone': 'Europe/Rome'
            }
        ]
    }
]

'''