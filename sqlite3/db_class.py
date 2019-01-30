import sqlite3


class ConnectDB:
    def __init__(self, db_name):
        self.db = sqlite3.connect(db_name)
        self.cursor = self.db.cursor()

    def create(self, data):
        self.cursor.execute(data)

    def insert(self, data):
        query, items = data
        try:
            self.cursor.executemany(query, items)
        except sqlite3.IntegrityError:
            print('Data already exists there.')

    def select(self, query):
        for row in self.cursor.execute(query):
            print(row)

    def commit(self):
        self.db.commit()

    def close(self):
        self.db.close()
