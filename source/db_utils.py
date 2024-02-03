import sqlite3

class DBOps:
    def __init__(self, database_path):
        self.con = sqlite3.connect(database_path)
        self.initial_setup()
    def initial_setup(self):
        pass