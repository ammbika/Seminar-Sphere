# Flask Event Management System

This is a simple Flask-based web application for managing events. Users can create, edit, delete, and search for events. There is also an admin login functionality to restrict event creation and modification.

## Features

- **Event Listing:** View a list of all events.
- **Admin Login:** Secure login for administrators to manage events.
- **Event Creation:** Admins can create new events.
- **Event Editing:** Admins can edit existing events.
- **Event Deletion:** Admins can delete events.
- **Event Search:** Users can search for events based on event name and dates.

## Prerequisites

- Python 3.x
- Flask

## Set up

1. Download python from official Python website: [Python Downloads](https://www.python.org/downloads/) and install it

2. ** Clone the repository **
    - git clone https://github.com/ammbika/Seminar-Sphere.git

3. Navigate to the project directory and create a new virtual environment
    - python -m venv <env_name>(For windows)
    - python3 -m venv <env_name>(For macos and linux)

4. Activate the virtual environment:
    - <env_name>\Scripts\activate (For windows)
    - source <env_name>/bin/activate

5. Install FLask
    - pip install flask

6. Verify flask installation
    - pip show flask

## Running the application

1. Set the Flask app environment variable
    - ** Windows**
        set FLASK_APP = app.py
    - ** macOS and Linux
        export FLASK_APP= app.py

2. Running the application
    - flask run


## Application Structure

- **app.py:** The main application file containing routes and logic.
- **templates/:** Directory containing HTML templates for rendering web pages.
  - **base.html:** The base template that other templates extend.
  - **home.html:** The homepage template displaying all events.
  - **login.html:** The login page template for admin login.
  - **admin.html:** The admin dashboard template showing event management options.
  - **createEvent.html:** Template for creating a new event.
  - **editEvent.html:** Template for editing an existing event.
  - **deleteEvent.html:** Template for confirming event deletion.
  - **search.html:** Template for searching events.


## Routes

- `/`: Home page displaying all events.
- `/login`: Admin login page.
- `/admin`: Admin dashboard.
- `/logout`: Logout page.
- `/create_event`: Page to create a new event.
- `/edit_event/<event_id>`: Page to edit an existing event.
- `/delete_event/<event_id>`: Page to delete an event.
- `/search`: Event search page.
- `/search_event`: Endpoint to handle event search requests.


## Custom Functions

- **validate_event_data:** Validates event data ensuring all required fields are filled, and dates and times are correctly formatted.


