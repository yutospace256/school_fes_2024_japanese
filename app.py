import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
from datetime import timedelta, datetime
import uuid

from python_func.sql_connector import SqliteConnector
from python_func.classes import User
from python_func.common import CommonObjectProcessor

# define classes
dbname = 'fes_app.db'

cop = CommonObjectProcessor()

# Flask setu@
app = Flask(__name__)
app.secret_key = "694c64d6-e1a5-5aae-9cef-18671138b4e0"
app.permanent_session_lifetime = timedelta(minutes=10)


# Flask routes
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'signin' in request.form:
            return redirect(url_for('signin'))
        elif 'login' in request.form:
            return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']

        # Create a new SqliteConnector instance for this request
        with SqliteConnector('fes_app.db') as db:  # Context manager for automatic closing
            # Check if the username already exists
            user = db.fetch_data('SELECT * FROM User WHERE username = ?', (username,))
            if user:
                return render_template('signin.html', error='error: This username is already exist.')  # Display error message in HTML

            password = request.form['password']
            now_time = datetime.now()
            user_id = cop.generate_uuid(uuid.NAMESPACE_DNS, str(now_time))

            # Insert new user using the connection from the context manager
            db.insert_data('INSERT INTO User (user_id, username, password) VALUES (?, ?, ?)', (user_id, username, password))
            session['user_id'] = user_id
        return redirect(url_for('explain'))
    return render_template('signin.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with SqliteConnector('fes_app.db') as db:  # Use SqliteConnector for thread safety
            # Fetch user using the connection from the context manager
            user = db.fetch_data('SELECT * FROM User WHERE username = ? AND password = ?', (username, password))
            # get user_id
            user_id = db.fetch_data('SELECT user_id FROM User WHERE username = ?', (username,))
            if user:
                session['user_id'] = user_id
                return redirect(url_for('explain'))
            return render_template('login.html', error='error: Username or password is incorrect.')
    return render_template('login.html')


@app.route('/explain', methods=['GET', 'POST'])
def explain():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    user_id = user_id[0][0]
    # Use SqliteConnector for thread-safe connection
    with SqliteConnector('fes_app.db') as db:
        user = db.fetch_data('SELECT * FROM User WHERE user_id = ?', (user_id,))
        if user:
              # Assuming user is a list of dictionaries
            return render_template('explain.html', user_id=user)
        else:
            return 'User not found.'  # Handle case where user is not found


@app.route('/game', methods=['GET', 'POST'])
def game():
    return render_template('game.html')

if __name__ == '__main__':
  app.run(debug=True)