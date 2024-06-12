from flask import Flask, render_template, request, make_response,  url_for, redirect, session
import json

app= Flask(__name__)

app.secret_key = 'your_secret_key_here'

@app.route('/')
def index():
    return render_template('home.html')

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
    return render_template('admin.html')

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

        event = {
            'event_name': event_name,
            'start_date': start_date,
            'end_date': end_date,
            'start_time': start_time,
            'end_time': end_time,
            'location': location,
            'description': description
        }

        try:
            with open('events.json', 'r') as f:
                events = json.load(f)
        except json.decoder.JSONDecodeError:
            events = []

        events.append(event)

        with open('events.json', 'w') as f:
            json.dump(events, f, indent=4)
        
        return redirect(url_for('admin'))

    return render_template('createEvent.html')

if __name__ == "__main__":
    app.run(debug=True)