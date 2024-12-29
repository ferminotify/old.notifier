from jinja2 import Environment, FileSystemLoader
from datetime import datetime, timedelta

events = [
    {
        'uid': 'id2', 
        'summary': 'CLASSE 5CIIN - USCITA ANTICIPATA', 
        'description': None, 
        'start.date': None, 
        'start.dateTime': '2024-12-27T13:00:00+02:00', 
        'start.timeZone': 'Europe/Rome', 
        'end.date': None, 
        'end.dateTime': '2022-04-13T13:00:00+02:00', 
        'end.timeZone': 'Europe/Rome',
    },
    {
        'uid': 'id1', 
        'summary': 'AULA 609 (con tecnico) - Corso FUSION MOD.CAM - REF. PROF. {COGNOME}', 
        'description': None, 
        'start.date': None, 
        'start.dateTime': '2024-12-28T14:00:00+02:00', 
        'start.timeZone': 'Europe/Rome', 
        'end.date': None, 
        'end.dateTime': '2022-04-12T17:00:00+02:00', 
        'end.timeZone': 'Europe/Rome',
    },
    {
        'uid': '2412270118',
        'summary': 'TEST 2',
        'description': '',
        'start.date': '',
        'start.dateTime': '2024-12-27T08:00:00+02:00',
        'start.timeZone': '',
        'end.date': '',
        'end.dateTime': '2024-12-27T09:00:00+02:00',
        'end.timeZone': ''
    }
    
]

# Set up Jinja2 environment
env = Environment(loader=FileSystemLoader('email_templates'))

# Load the template
template = env.get_template('mail_notification.min.html')

# sort events: today first and sort by start asc and startDateTime first and then by endDateTime
events.sort(key=lambda x: (x.get('start.date') or x.get('start.dateTime')))
print("Sorted: ")
for event in events:
    print(event.get('uid'))

# create a list of events of tomorrow
events_tomorrow = []
# move event from events to events_tomorrow if the event is tomorrow
for event in events:
    if event.get('start.date') and datetime.strptime(event['start.date'], '%Y-%m-%d').date() == datetime.now().date() + timedelta(days=1):
        events_tomorrow.append(event)
        events.remove(event)
    elif event.get('start.dateTime') and datetime.strptime(event['start.dateTime'], '%Y-%m-%dT%H:%M:%S%z').date() == datetime.now().date() + timedelta(days=1):
        events_tomorrow.append(event)
        events.remove(event)
print("Events tomorrow: ")
for event in events_tomorrow:
    print("\t" + event.get('uid'))
print("Events today: ")
for event in events:
    print("\t" + event.get('uid'))

# Define data to render
is_daily = True
giorns = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"]
data = {
    'title': "Eventi previsti" if is_daily else "Nuovo evento",
    'greetings': "Ciao" if not is_daily else "Buongiorno" if datetime.now().hour < 12 else "Buon pomeriggio" if datetime.now().hour < 18 else "Buonasera",
    'name': 'Kevin',
    'gender': 'o',
    'n_events': f"{len(events) + len(events_tomorrow)} nuovi eventi" if len(events) + len(events_tomorrow) > 1 else f"{len(events) + len(events_tomorrow)} nuovo evento",
    'events_today': events,
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

# Render the template with data
output = template.render(data)

# Write the output to a file named test.html
with open('test.html', 'w', encoding='utf-8') as file:
    file.write(output)

print("Rendered HTML has been written to test.html")