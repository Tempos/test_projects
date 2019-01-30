from db_class import ConnectDB
from queries import *
from db_schema import *

db = ConnectDB('test_beds.db')

# Create tables
db.create(DEVICE_TABLE)
db.create(IFACE_TABLE)

# Insert a row of data
db.insert(STATIONS)
db.insert(INTERFACES)

# # Save changes
db.commit()

# read from table
db.select(SELECT_ALL_DEVICES)

# close connection.
db.close()
