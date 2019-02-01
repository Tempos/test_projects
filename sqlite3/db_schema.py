DEVICE_TABLE = '''CREATE TABLE IF NOT EXISTS devices 
                (id INTEGER PRIMARY KEY UNIQUE,
                 name VARCHAR(10) UNIQUE,
                 lab VARCHAR(10))'''

IFACE_TABLE = '''CREATE TABLE IF NOT EXISTS interfaces
                (device_id INTEGER PRIMARY KEY UNIQUE,
                 name VARCHAR(10),
                 number INT,
                 speed INT,
                 status VARCHAR(5))'''
