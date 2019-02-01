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

    def insert(self, query):
        with self.db:
            try:
                self.cursor.executemany(*query)
                self.commit()
            except sqlite3.IntegrityError:
                pass  # print('\nData already exists there.')

    def test(self, query):
        select = self.cursor.execute(query)
        for description in select.description:
            print(description)

    def select(self, query):
        with self.db:
            try:
                select = self.cursor.execute(*query)
                print()
                for row in select:
                    print(row)
            except sqlite3.OperationalError as oe:
                print(f"\nError occurred - {oe.args[0]}")

    def update(self, data):
        with self.db:
            try:
                self.cursor.execute(*data)
            except sqlite3.OperationalError as oe:
                print(f"\nError1 occurred - {oe.args[0]}")
            except sqlite3.IntegrityError as ie:
                print(f"\nError2 occurred - {ie.args[0]}")

    def delete(self, query):
        with self.db:
            try:
                self.cursor.execute(*query)
                self.commit()
            except sqlite3.OperationalError as oe:
                print(f"\nError occurred - {oe.args[0]}")

    def commit(self):
        self.db.commit()
