from random import choice

def get_event_color() -> str:
    # Returns a RBG color for event card in the emails

    colors = [
        "#1B5E20", "#FF6F00", "#1A237E", "#BF360C", "#01579B", "#33691E",
        "#880E4F", "#E65100", "#311B92", "#B71C1C", "#004D40", "#F57F17",
        "#0D47A1", "#827717", "#006064", "#4A148C", 
    ]

    return choice(colors)

def get_daily_notification_mail_body(receiver: dict, events: list) -> str:
    

events = [
    {
                'id': '175kism1teadmku9if9q5kr969', 
                'subject': 'CLASSE 3AIIN - AULA 16 - CORSO RECUPERO INGLESE - PROF. MALAVASI MARIA', 
                'desc': None, 
                'startDate': None, 
                'startDateTime': '2022-07-19T12:00:00+02:00', 
                'startTimeZone': 'Europe/Rome', 
                'endDate': None, 
                'endDateTime': '2022-07-19T13:00:00+02:00', 
                'endTimeZone': 'Europe/Rome'
    },
    {
                'id': '175kism1teadmku9if9q5kr969', 
                'subject': 'CLASSE 4CIIN - AULA MAGNA - PROF. ZALDINI', 
                'desc': None, 
                'startDate': None, 
                'startDateTime': '2022-07-19T12:00:00+02:00', 
                'startTimeZone': 'Europe/Rome', 
                'endDate': None, 
                'endDateTime': '2022-07-19T13:00:00+02:00', 
                'endTimeZone': 'Europe/Rome'
    }
]

user = {
        "id": 'id',
        "name": "name",
        "email": "email"
}

body = get_daily_notification_mail_body(user, events)

with open("test.htm", "w") as f:
	f.write(body)
