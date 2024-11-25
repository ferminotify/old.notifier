from jinja2 import Environment, FileSystemLoader
import datetime

events = [
    {
                'id': 'id1', 
                'subject': 'AULA 609 (con tecnico) - Corso FUSION MOD.CAM - REF. PROF. {COGNOME}', 
                'desc': None, 
                'startDate': None, 
                'startDateTime': '2022-04-12T14:00:00+02:00', 
                'startTimeZone': 'Europe/Rome', 
                'endDate': None, 
                'endDateTime': '2022-04-12T17:00:00+02:00', 
                'endTimeZone': 'Europe/Rome'
    }
]

# Set up Jinja2 environment
env = Environment(loader=FileSystemLoader('email_templates'))

# Load the template
template = env.get_template('lastminute.min.html')

# Define data to render
data = {
    'name': 'Kevin',
    'gender': 'o',
    'n_events': f"{len(events)} nuovi eventi" if len(events) > 1 else f"{len(events)} nuovo evento",
    'events': events
}

# convert events date to dd-mm-yyyy and datetime to hh:mm
for event in data['events']:
    if event['startDate']:
        event['startDate'] = datetime.datetime.strptime(event['startDate'], '%Y-%m-%d').strftime('%d/%m/%Y')
    if event['endDate']:
        event['endDate'] = datetime.datetime.strptime(event['endDate'], '%Y-%m-%d').strftime('%d/%m/%Y')
    if event['startDateTime']:
        event['startDateTime'] = datetime.datetime.strptime(event['startDateTime'], '%Y-%m-%dT%H:%M:%S%z').strftime('%H:%M')
    if event['endDateTime']:
        event['endDateTime'] = datetime.datetime.strptime(event['endDateTime'], '%Y-%m-%dT%H:%M:%S%z').strftime('%H:%M')

# Render the template with data
output = template.render(data)

# Write the output to a file named test.html
with open('test.html', 'w', encoding='utf-8') as file:
    file.write(output)

print("Rendered HTML has been written to test.html")