from db_class import ConnectDB
from db_schema import *
from queries import *
from test_data import *

db = ConnectDB('test_beds.db')

# Create tables
db.create(DEVICE_TABLE)
db.create(IFACE_TABLE)

# db.test()

# Insert a row of data
db.insert(STATIONS, STATIONS_INSERT)
db.insert(INTERFACES, INTERFACES_INSERT)

# Delete row
db.delete(INTERFACES_DELETE, ROW_NAME)

# Update table
db.update(UPDATE_interfaces)

# read from table
db.select(SELECT_ALL_FROM_devices)
db.select(SELECT_ALL_FROM_interfaces)

