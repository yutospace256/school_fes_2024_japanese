import sqlite3
from flask import Flask, render_template, request


dbname = 'test_comments.db'


def db_connect():
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    return conn, cur

def add_comments(comment):
    conn, cur = db_connect()
    cur.execute('INSERT INTO comments(comment) values(?)', (comment,))
    conn.commit()
    cur.close()
    conn.close()

def show_comments():
    conn, cur = db_connect()
    cur.execute('SELECT * FROM comments')
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'signin' in request.form:
            return render_template('comment.html')
        else:  # Handle comment submission
            comment = request.form['comment']
            add_comments(comment)  # Add the comment to the database
            return render_template('index.html', message="Comment added successfully!")  # Display success message
    return render_template('index.html')

@app.route('/comment', methods=['POST'])
def comments():
    comment = request.form['comment']
    add_comments(comment)
    return render_template('index.html', message="Comment added successfully!")  # Redirect or display success message

@app.route('/show')
def show():
    rows = show_comments()
    return render_template('show.html', rows=rows)

if __name__ == '__main__':
  app.run(debug=True)