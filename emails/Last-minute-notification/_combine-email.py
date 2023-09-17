from random import choice

def get_event_color() -> str:
    # Returns a RBG color for event card in the emails

    colors = [
        "#1B5E20", "#FF6F00", "#1A237E", "#BF360C", "#01579B", "#33691E",
        "#880E4F", "#E65100", "#311B92", "#B71C1C", "#004D40", "#F57F17",
        "#0D47A1", "#827717", "#006064", "#4A148C", 
    ]

    return choice(colors)

# LAST MINUTE NOTIFICATION
def get_body(receiver: dict, events: list) -> str:
    body = ""

    with open("01.htm", encoding="utf8") as f:
        body += f.read()
    
    body += receiver["name"]

    with open("02.htm", encoding="utf8") as f:
        body += f.read()

    body += str(len(events))
    body += "</b> evento" if len(events) == 1 else "</b> eventi"

    with open("03.htm", encoding="utf8") as f:
        body += f.read()

    for i in events:
        card_color = get_event_color()

        with open("04.htm", encoding="utf8") as f:
            body += f.read()

        body += card_color

        with open("05.htm", encoding="utf8") as f:
            body += f.read()

        body += i["subject"]

        # if event has same start and end date/time (es. entrata posticipata)
        if i["startDate"] == i["endDate"] and i["startDateTime"] == i["endDateTime"]:
            with open("06b.htm", encoding="utf8") as f:
                body += f.read()
            body += i["startDateTime"][11:16] if i["startDateTime"] else "/".join(i["startDate"].split("-")[::-1])
        # if event has same start date but different end date/time
        else:
            with open("06a.htm", encoding="utf8") as f:
                body += f.read()
            body += i["startDateTime"][11:16] if i["startDateTime"] else "/".join(i["startDate"].split("-")[::-1])
            with open("06a1.htm", encoding="utf8") as f:
                body += f.read()
            body += i["endDateTime"][11:16] if i["endDateTime"] else "/".join(i["endDate"].split("-")[::-1])

        with open("07.htm", encoding="utf8") as f:
            body += f.read()
        
    with open("08.htm", encoding="utf8") as f:
            body += f.read()

    return body

events = [
    {
                'id': 'id2', 
                'subject': 'CLASSE 3CIIN - USCITA DIDATTICA - PROFF. {COGNOME}, {COGNOME}', 
                'desc': None, 
                'startDate': '2022-04-12', 
                'startDateTime': None, 
                'startTimeZone': 'Europe/Rome', 
                'endDate': '2022-04-12', 
                'endDateTime': None, 
                'endTimeZone': 'Europe/Rome'
    }
]

user = {
        "id": 'id',
        "name": "Kevin",
        "email": "email"
}

body = get_body(user, events)

with open("test.htm", "w", encoding="utf8") as f:
	f.write(body)
