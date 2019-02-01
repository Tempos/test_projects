import sqlite3


class ConnectDB:
    cursor = ''

    def __init__(self, db_name):
        self.db_name = db_name

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        # self.cursor = self.conn.cursor()
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    def create(self, data):
        try:
            self.cursor.execute(data)
            self.commit()
        except sqlite3.Error as e:
            print(f"{e.args[0]} occurred.")

    def insert(self, query, data):
        try:
            self.cursor.executemany(query, data)
            self.commit()
        except sqlite3.IntegrityError:
            print('Data already exists there.')

    def select(self, query):
        try:
            for row in self.cursor.execute(query):
                print(row)
        except sqlite3.OperationalError as oe:
            print(f"Error occurred - {oe.args[0]}")

    def delete(self, query, data):
        try:
            self.cursor.execute(query, data)
            self.commit()
        except sqlite3.OperationalError as oe:
            print(f"\nError occurred - {oe.args[0]}\n")

    def commit(self):
        self.conn.commit()
