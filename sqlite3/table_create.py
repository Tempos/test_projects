import sqlite3
from table_inserts import STATIONS, INTERFACES
from table_schema import DEVICE_TABLE, IFACE_TABLE

conn_dev = sqlite3.connect('devices.db')
conn_iface = sqlite3.connect('interfaces.db')

device = conn_dev.cursor()
iface = conn_iface.cursor()

# Create table
device.execute(DEVICE_TABLE)
iface.execute(IFACE_TABLE)

# Insert a row of data
try:
    device.executemany("INSERT INTO devices VALUES(?, ?, ?)", STATIONS)
    iface.executemany("INSERT INTO interfaces VALUES (?, ?, ?, ?, ?)", INTERFACES)
except sqlite3.IntegrityError:
    print('Data already exists there.')

# Save changes and close connection.
conn_dev.commit()
conn_iface.commit()

for row in device.execute('SELECT * FROM devices'):
    print(row)

conn_dev.close()
conn_iface.close()
