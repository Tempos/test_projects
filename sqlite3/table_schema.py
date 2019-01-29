DEVICE_TABLE = '''CREATE TABLE IF NOT EXISTS devices (id INT PRIMARY KEY UNIQUE, name VARCHAR(10), lab VARCHAR(10))'''
IFACE_TABLE = '''CREATE TABLE IF NOT EXISTS interfaces
                (device_id INT PRIMARY KEY UNIQUE,
                 name VARCHAR(10),
                 number INT, 
                 speed INT, 
                 status VARCHAR(5))'''
