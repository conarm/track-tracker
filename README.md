# TrackTracker - A Flask Web Application

## Statement of Purpose

**TrackTracker** is a Flask-based web application designed for music enthusiasts to track their favorite albums, contribute ratings and reviews, and discover new music. The application aggregates user ratings to display the highest-rated albums on a "Top Albums" page and promotes the most-liked reviews on a "Top Reviews" page. It provides a community-driven platform for music fans to engage with others and share their experiences.

---

## Installation

Provided **Python 3.4+** is installed, create a new python virtual environment with `python -m venv <directory>`

The new environment can now be activated through `venv\Scripts\activate.bat` (cmd.exe) or `venv\Scripts\Activate.ps1` (PowerShell)

Once the environment is activated, from the project directory run: `pip install -r requirements.txt` to install all of the dependencies

---

## Initial migration

On first install, there will be no database set up, requiring the user to create and apply an initial migration based on the schema:

 - Create the database with `flask db init`
 - Create the initial migration with `flask db migrate -m "initial migration"`
 - Upgrade the database using the migration with `flask db upgrade`

---

## Running the application

Once installation has completed and the environment is activated, the application can be ran with `flask run`.

---

## Features

- **Album Rating and Review:** Users can rate albums, post reviews, and read others’ reviews.
- **Top Albums/Reviews:** Lists of highest-rated albums and most-liked reviews.
- **Likes:** Users can like individual reviews, elevating thoughtful content.
- **Authentication:** Secure user login and registration system using Flask-Login.

---

## Architecture

TrackTracker uses a **three-tier architecture**:

1. **Presentational Tier:** Handles user interactions through HTML, Flask-WTF forms, and Jinja2 templates.
2. **Business Logic Tier:** Core functionalities like request handling and album rating logic, managed in `views.py`.
3. **Data Access Tier:** Communicates with the database using SQLAlchemy ORM to handle models and queries.

---

## Web Forms

The application uses Flask-WTF to implement and validate forms. Three main forms are available:

- **LoginForm:** For users to log in.
- **RegistrationForm:** For creating new accounts.
- **RatingForm:** To submit album ratings and reviews.

Each form includes appropriate field types and validators, ensuring data integrity.

---

## Database

The application uses **SQLite** with **Flask-SQLAlchemy** for ORM. The models are designed to manage albums, artists, genres, and reviews.

The data model can be found below:

![image](https://github.com/user-attachments/assets/921b2013-35e6-442d-9335-36a425688786)


---

## Authentication and Sessions

Authentication is managed using **Flask-Login** for session handling. Key features:

- Logged-in users are tracked via `current_user.is_authenticated`.
- Certain pages are restricted using the `@login_required` decorator.
- Passwords are securely hashed using Werkzeug’s `generate_password_hash()` and `check_password_hash()`.

---

## Security Measures

To mitigate potential security threats, the following measures have been implemented:

- **Cross-Site Scripting (XSS) protection:** Flask escapes unsanitized input to prevent the injection of harmful code.
- **Session Management:** Flask-Login securely manages sessions to prevent session hijacking.
- **Password Hashing:** User passwords are securely hashed before storing in the database.

---

## Unit Testing

Basic unit tests are implemented using Python’s `unittest` module.

These can be ran using `python test.py`

---

## Logging

Logging is used to track key events such as errors and info logs. Logs are saved to `tracktracker.log`, capturing the date and time of each event.
