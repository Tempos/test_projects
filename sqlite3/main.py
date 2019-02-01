from db_class import ConnectDB
from db_schema import *
from queries import *
# from test_data import *

db = ConnectDB('test_beds.db')

# Create tables
db.create(DEVICE_TABLE)
db.create(IFACE_TABLE)

# Insert a row of data
db.insert(STATIONS)
db.insert(INTERFACES)

# read from table
# db.select(SELECT_ALL_FROM_devices)
db.select(SELECT_ALL_FROM_interfaces)

# Update table
db.update(UPDATE_interfaces)

# Delete row
db.delete(INTERFACES_DELETE)

# read from table
db.select(SELECT_ALL_FROM_interfaces)

print('='*20)

db.select(SELECT_W_CONDITION)
db.select(JOIN)
