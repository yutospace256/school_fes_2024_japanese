import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
from datetime import timedelta, datetime, timezone
import uuid

from python_func.sql_connector import SqliteConnector
from python_func.classes import User
from python_func.common import CommonObjectProcessor

# define classes
dbname = 'fes_app.db'

cop = CommonObjectProcessor()

# Flask setup
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
        password = request.form['password']
        # Create a new SqliteConnector instance for this request
        with SqliteConnector('fes_app.db') as db:  # Context manager for automatic closing
            # Check if the username already exists
            user = db.fetch_data('SELECT * FROM User WHERE username = ?', (username,))
            if user:
                return render_template('signin.html', error='error: This username is already exist.')  # Display error message in HTML

            
            now_time = datetime.now()
            user_id = cop.generate_uuid(uuid.NAMESPACE_DNS, str(now_time))

            # Insert new user using the connection from the context manager
            db.insert_data('INSERT INTO User (user_id, username, password, points, episode) VALUES (?, ?, ?, ?, ?)', (user_id, username, password, 0, 0))
            session['user_id'] = user_id
        return redirect(url_for('introduce'))
    return render_template('signin.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with SqliteConnector('fes_app.db') as db:  # Use SqliteConnector for thread safety
            # Fetch user using the connection from the context manager
            user = db.fetch_data('SELECT * FROM User WHERE username = ? AND password = ?', (username, password))
            if user:
                # get user_id
                user_id = user[0][1]
                session['user_id'] = user_id
                return redirect(url_for('introduce'))
            return render_template('login.html', error='error: Username or password is incorrect.')
    return render_template('login.html')


@app.route('/introduce', methods=['GET', 'POST'])
def introduce():
    user = cop.get_user_id()
    if user:
        if request.method == 'POST' and 'game_start' in request.form:
            # Use GMT timezone
            game_start = datetime.now(timezone.utc)
            session['game_start'] = game_start
            return redirect(url_for('game'))
        return render_template('introduce.html', user_id=user)
    else:
        return render_template("error.html", site="/introduce", error_code=1)  # Handle case where user is not found
    

@app.route('/game', methods=['GET', 'POST'])
def game():
    user = cop.get_user_id()
    if user:
        game_start = session.get('game_start')
        print(game_start)
        if request.method == 'POST' and 'missioncode' in request.form:
            input_code = request.form['mission_code']
            with SqliteConnector('fes_app.db') as db:
                # Get the data for mission_code=input_code in the misssion table.
                mission = db.fetch_data('SELECT * FROM mission WHERE mission_code = ?', (input_code,))
                if mission:
                    session['mission_id'] = mission[0][1]
                    return redirect(url_for('mission'))
                else:
                    return render_template("error.html", site="/game", error_code=2)  # Handle case where mission is not found
        end_time = game_start + timedelta(minutes=5)
        end_time_timestamp = int(end_time.timestamp() * 1000)  # Convert to milliseconds
        print(end_time)
        return render_template('game.html', user_id=user, end_time=end_time_timestamp)
    else:
        return render_template("error.html", site="/game", error_code=1)  # Handle case where user is not found
    
@app.route('/mission', methods=['GET', 'POST'])
def mission():
    user = cop.get_user_id()
    mission_id = session.get('mission_id')
    USER = User(user[0][1], user[0][2], user[0][3], user[0][4], user[0][5])
    if user:
        if request.method == 'POST' and 'cipher_entry' in request.form:
            cipher = request.form['cipher']
            with SqliteConnector('fes_app.db') as db:
                cipher_data = db.fetch_data('SELECT * FROM Cipher WHERE mission_id = ? AND cipher = ?', (mission_id, cipher))
                if cipher_data:
                    # Check if user_id =USER.id,cipher_id=cipher_data[0][1] exists in the Logs table.
                    log = db.fetch_data('SELECT * FROM Logs WHERE user_id = ? AND cipher_id = ?', (USER.id, cipher_data[0][1]))
                    if log:
                        return render_template('mission.html', user_id=user, mission_id=mission_id, cipher_data=cipher_data, error='error: You have already solved this cipher.')    
                    # Update points using retrieved data (assuming User class with add_points)
                    USER.add_points(cipher_data[0][4])
                    # Update data in USER.points to the points column of the User table in sql
                    db.update_data('UPDATE User SET points = ? WHERE user_id = ?', (USER.points, USER.id))
                    # Insert log data
                    db.insert_data('INSERT INTO Logs (user_id, cipher_id) VALUES (?, ?)', (USER.id, cipher_data[0][1]))
                return render_template('mission.html', user_id=user, mission_id=mission_id)
        elif request.method == 'POST' and 'back_game' in request.form:
            # progress episode 
            # I should update this code for episode progress
            with SqliteConnector('fes_app.db') as db:
                db.update_data('UPDATE User SET points = ? WHERE user_id = ?', (USER.points, USER.id))
            return redirect(url_for('game'))
        else:
            return render_template('mission.html', user_id=user, mission_id=mission_id)
    else:
        return render_template("error.html", site="/mission", error_code=1)


if __name__ == '__main__':
  app.run(debug=True)