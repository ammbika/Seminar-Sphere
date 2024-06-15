from flask import Flask, render_template, request, url_for, redirect, session
import json
import uuid
from datetime import datetime

app= Flask(__name__)
app.secret_key = 'gfy3o48046Gc7&^$hdjs'

def parse_time(time_str):
    try:
        return datetime.strptime(time_str, '%H:%M').time()
    except ValueError:
        return None

def validate_event_data(title, start_date, end_date, start_time, end_time, location,participants, description):
    if not title or not location or not description:
        return False, "Event name, location, and description cannot be empty."

    try:
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        return False, "Invalid date or time format."
    
    try:
        start_time_obj = parse_time(start_time)
        end_time_obj = parse_time(end_time)
        if not start_time_obj or not end_time_obj:
            raise ValueError("Invalid time format")
    except ValueError:
        return False, "Invalid time format."

    if start_date_obj > end_date_obj:
        return False, "Start date cannot be after end date."
    if end_time_obj <= start_time_obj:
        return False, "End time must be after start time."
    
    try:
        participants = int(participants)
        if participants < 1:
            return False, "Number of participants must be at least 1."
    except ValueError:
        return False, "Invalid number of participants."

    return True, ""

@app.route('/')
def index():
    try:
        with open('events.json', 'r') as f:
            events = json.load(f)
    except FileNotFoundError:
        events = []
    except json.decoder.JSONDecodeError:
        events = []
    return render_template('home.html', events=events)

with open('credentials.json') as f:
    credentials = json.load(f)

ADMIN_USERNAME = credentials['username']
ADMIN_PASSWORD = credentials['password']
failure_message = None

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        username= request.form['username']
        password= request.form['password']

        if username!=ADMIN_USERNAME or password!= ADMIN_PASSWORD:
            return render_template('login.html', failure_message="Invalid credentials.")
        
        session['loggedIn'] = True
        return redirect(url_for('admin'))
    
    return render_template('login.html')
    
@app.route('/admin')
def admin():
    if 'loggedIn' in session:
        try:
            with open('events.json', 'r') as f:
                events = json.load(f)
        except FileNotFoundError:
            events = []
        except json.decoder.JSONDecodeError:
            events = []
        return render_template('admin.html', events=events)
    return redirect(url_for('login'))


@app.route('/logout', methods=['GET',"POST"])
def logout():
    if request.method=='POST':
        session.pop('loggedIn', None)
        return redirect(url_for('index'))
    return render_template('logout.html')
    
@app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    failure_message = None

    if 'loggedIn' in session:
        if request.method == 'POST':
            title = request.form['title']
            start_date = request.form['start_date']
            end_date = request.form['end_date']
            start_time = request.form['start_time']
            end_time = request.form['end_time']
            location = request.form['location']
            participants = request.form['participants']
            description = request.form['description']
            id = str(uuid.uuid4())

            is_valid, error_message = validate_event_data(title, start_date, end_date, start_time, end_time, location,participants, description)
            if not is_valid:
                return render_template('createEvent.html', failure_message=error_message)

            event = {
                'title': title,
                'start_date': start_date,
                'end_date': end_date,
                'start_time': start_time,
                'end_time': end_time,
                'location': location,
                'participants': participants,
                'description': description,
                'id':id
            }

            try:
                with open('events.json', 'r') as f:
                    events = json.load(f)
            except FileNotFoundError:
                events = []
            except json.decoder.JSONDecodeError:
                return render_template('createEvent.html', failure_message="Error: Unable to read existing events.")

            events.append(event)

            try:
                with open('events.json', 'w') as f:
                    json.dump(events, f, indent=4)
            except IOError:
                return render_template('createEvent.html', failure_message="Error: Unable to write events to file.")

            if not failure_message:
                    return redirect(url_for('admin'))
            return render_template('createEvent.html', failure_message=failure_message)

        return render_template('createEvent.html')

    return redirect(url_for('login'))


@app.route('/edit_event/<event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    if 'loggedIn' in session:
        failure_message = None
        try:
            with open('events.json', 'r') as f:
                events = json.load(f)
        except FileNotFoundError:
            events = []
        except json.decoder.JSONDecodeError:
            return render_template('editEvent.html', failure_message="Error: Unable to read existing events.")   
            
        event = next((event for event in events if event['id'] == event_id), None)

        if request.method == 'POST':
            if event:
                event['title'] = request.form['title']
                event['start_date'] = request.form['start_date']
                event['end_date'] = request.form['end_date']
                event['start_time'] = request.form['start_time']
                event['end_time'] = request.form['end_time']
                event['location'] = request.form['location']
                event['participants'] = request.form['participants']
                event['description'] = request.form['description']

                is_valid, error_message = validate_event_data(event['title'], event['start_date'], event['end_date'], event['start_time'], event['end_time'], event['location'], event['participants'], event['description'])
                if not is_valid:
                    return render_template('editEvent.html', event=event, failure_message=error_message)


                try:
                    with open('events.json', 'w') as f:
                        json.dump(events, f, indent=4)
                except IOError:
                    return render_template('editEvent.html', failure_message="Error: Unable to write events to file.")
                if not failure_message:
                    return redirect(url_for('admin'))
                return render_template('editEvent.html',event=event, failure_message=failure_message)
    
        return render_template('editEvent.html', event=event)

    return redirect(url_for('login'))


@app.route('/delete_event/<event_id>', methods=['GET','POST'])
def delete_event(event_id):
    if 'loggedIn' in session:
        failure_message = None
        if request.method =='POST':
            try:
                with open('events.json', 'r') as f:
                    events = json.load(f)
            except FileNotFoundError:
                events = []
            except json.decoder.JSONDecodeError:
                return render_template('deleteEvent.html', failure_message="Error: Unable to read existing events.")

            events = [event for event in events if event['id'] != event_id]

            try:
                with open('events.json', 'w') as f:
                    json.dump(events, f, indent=4)
            except IOError:
                return render_template('deleteEvent.html', failure_message="Error: Unable to write events to file.")
            if not failure_message:
                return redirect(url_for('admin'))
            return render_template('deleteEvent.html', failure_message=failure_message)
        return render_template('deleteEvent.html',event_id=event_id)
    
    return redirect(url_for('login'))

@app.route('/search')
def search():
    return render_template('search.html')
    
@app.route('/search_event', methods=['GET'])
def search_event():
    # Get search criteria from request args
    title = request.args.get('title')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    try:
        with open('events.json', 'r') as f:
            events = json.load(f)
    except FileNotFoundError:
        events = []

    # Filter events based on criteria
    filtered_events = events
    if title:
        filtered_events = [event for event in filtered_events if title.lower() in event.get('title', '').lower()]
    if start_date:
        filtered_events = [event for event in filtered_events if event.get('start_date') == start_date]
    if end_date:
        filtered_events = [event for event in filtered_events if event.get('end_date') == end_date]

    return render_template('search.html', events=filtered_events) 


if __name__ == "__main__":
    app.run(debug=True)