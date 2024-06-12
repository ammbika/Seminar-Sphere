from flask import Flask, render_template, request, make_response,  url_for, redirect, session
import json
import uuid

app= Flask(__name__)

app.secret_key = 'your_secret_key_here'

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

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        username= request.form['username']
        password= request.form['password']

        if username!=ADMIN_USERNAME or password!= ADMIN_PASSWORD:
            return "Invalid credentials", 401
        
        session['username'] = username
        resp = make_response(redirect(url_for('admin')))
        resp.set_cookie('username', username)
        return resp
    
    return render_template('login.html')
    
@app.route('/admin')
def admin():
    username = request.cookies.get('username')
    if not username or username!=ADMIN_USERNAME:
    #if 'username' not in session or session['username']!= ADMIN_USERNAME:
        return redirect(url_for('login'))
    try:
        with open('events.json', 'r') as f:
            events = json.load(f)
    except FileNotFoundError:
        events = []
    except json.decoder.JSONDecodeError:
        events = []
    return render_template('admin.html', events=events)

@app.route('/logout')
def logout():
    return render_template('logout.html')

@app.route('/logout_decision', methods=['POST'])
def logout_decision():
    decision= request.form['decision']
    if decision == 'Yes':
        #session.pop('username', None)
        resp = make_response(redirect(url_for('index')))
        resp.set_cookie('username', '', expires=0)
        return resp

    else:
        return redirect(url_for('admin'))
    
@app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    username = request.cookies.get('username')

    success_message = None
    failure_message = None

    if not username or username != ADMIN_USERNAME:
        return redirect(url_for('login'))

    if request.method == 'POST':
        event_name = request.form['event_name']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        location = request.form['location']
        description = request.form['description']
        id = str(uuid.uuid4())

        event = {
            'event_name': event_name,
            'start_date': start_date,
            'end_date': end_date,
            'start_time': start_time,
            'end_time': end_time,
            'location': location,
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

        # Set success message
        success_message = "Event created successfully!"
        failure_message = None

        return render_template('createEvent.html', success_message=success_message, failure_message=failure_message)

    return render_template('createEvent.html')

@app.route('/edit_event/<event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    username = request.cookies.get('username')

    if not username or username != ADMIN_USERNAME:
        return redirect(url_for('login'))

    try:
        with open('events.json', 'r') as f:
            events = json.load(f)
    except FileNotFoundError:
        events = []
    except json.decoder.JSONDecodeError:
        return render_template('createEvent.html', failure_message="Error: Unable to read existing events.")   
        
    event = next((event for event in events if event['id'] == event_id), None)

    if request.method == 'POST':
        if event:
            event['event_name'] = request.form['event_name']
            event['start_date'] = request.form['start_date']
            event['end_date'] = request.form['end_date']
            event['start_time'] = request.form['start_time']
            event['end_time'] = request.form['end_time']
            event['location'] = request.form['location']
            event['description'] = request.form['description']

            try:
                with open('events.json', 'w') as f:
                    json.dump(events, f, indent=4)
            except IOError:
                return render_template('createEvent.html', failure_message="Error: Unable to write events to file.")
            success_message = "Event updated successfully!"
            return redirect(url_for('admin', success_message=success_message))

    return render_template('editEvent.html', event=event)


@app.route('/delete_event/<event_id>', methods=['GET','POST'])
def delete_event(event_id):
    username = request.cookies.get('username')

    if not username or username != ADMIN_USERNAME:
        return redirect(url_for('login'))

    if request.method =='POST':
        try:
            with open('events.json', 'r') as f:
                events = json.load(f)
        except FileNotFoundError:
            events = []
        except json.decoder.JSONDecodeError:
            return render_template('createEvent.html', failure_message="Error: Unable to read existing events.")

        events = [event for event in events if event['id'] != event_id]

        try:
            with open('events.json', 'w') as f:
                json.dump(events, f, indent=4)
        except IOError:
            return render_template('createEvent.html', failure_message="Error: Unable to write events to file.")
        success_message = "Event updated successfully!"
        return redirect(url_for('admin', success_message=success_message))
    
    return render_template('deleteEvent.html',event_id=event_id)


if __name__ == "__main__":
    app.run(debug=True)