import sqlite3



class User():
    def __init__(self, id, username, password, points, episode):
        self.id = id
        self.username = username
        self.password = password
        self.points = points
        self.episode = episode

    def add_points(self, points):
        self.points += points
        # LOG 

    def progress_episode(self):
        self.episode += 1
        # LOG
