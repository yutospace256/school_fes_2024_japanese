import sqlite3

from python_func.sql_connector import SqliteConnector

dbname = 'fes_app.db'

sql = SqliteConnector(dbname)

class User():
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

