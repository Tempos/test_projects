import sqlite3


class ConnectDB:
    def __init__(self, db_name):
        self.db = sqlite3.connect(db_name)
        self.cursor = self.db.cursor()

    def create(self, data):
        with self.db:
            try:
                self.cursor.execute(data)
                self.commit()
            except sqlite3.Error as e:
                print(f"{e.args[0]} occurred.")

    def insert(self, query, data):
        with self.db:
            try:
                self.cursor.executemany(query, data)
                self.commit()
            except sqlite3.IntegrityError:
                print('\nData already exists there.')

    def test(self, query):
        select = self.cursor.execute(query)
        for description in select.description:
            print(description)

    def select(self, query):
        with self.db:
            try:
                select = self.cursor.execute(query)
                print()
                for row in select:
                    print(row)
            except sqlite3.OperationalError as oe:
                print(f"\nError occurred - {oe.args[0]}")
            finally:
                return select

    def update(self, data):
        with self.db:
            try:
                self.cursor.executescript(data)
            except sqlite3.OperationalError as oe:
                print(f"\nError occurred - {oe.args[0]}")

    def delete(self, query, data):
        with self.db:
            try:
                self.cursor.execute(query, data)
                self.commit()
            except sqlite3.OperationalError as oe:
                print(f"\nError occurred - {oe.args[0]}")

    def commit(self):
        self.db.commit()
