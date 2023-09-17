from random import choice

def get_event_color() -> str:
    # Returns a RBG color for event card in the emails

    colors = [
        "#1B5E20", "#FF6F00", "#1A237E", "#BF360C", "#01579B", "#33691E",
        "#880E4F", "#E65100", "#311B92", "#B71C1C", "#004D40", "#F57F17",
        "#0D47A1", "#827717", "#006064", "#4A148C", 
    ]

    return choice(colors)

def get_registration_mail_body(name: str, verification_code: str) -> str:
    body = ""

    with open("01.htm") as f:
        body += f.read()

    body += name

    with open("02.htm") as f:
        body += f.read()

    body += verification_code

    with open("03.htm") as f:
        body += f.read()

    body += verification_code

    with open("04.htm") as f:
        body += f.read()
    
    body += verification_code

    with open("05.htm") as f:
        body += f.read()

    return body

user = {
        "id": 'id',
        "name": "Kevin",
        "email": "email"
}

name = user['name']
verification_code = '123456'

body = get_registration_mail_body(name, verification_code)

with open("test.htm", "w") as f:
	f.write(body)
