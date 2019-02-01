from del_it.db_class_v2 import ConnectDB
from db_schema import *
from queries import *
from test_data import *

with ConnectDB('test_beds.db') as db:
    cur = db.cursor()

    # Create tables
    cur.create(DEVICE_TABLE)
    cur.create(IFACE_TABLE)

    # Insert a row of data
    cur.insert(STATIONS, STATIONS_INSERT)
    cur.insert(INTERFACES, INTERFACES_INSERT)

    # Delete row
    cur.delete(INTERFACES_DELETE, ROW_NAME)

    # read from table
    cur.select(SELECT_ALL_FROM_devices)
    cur.select(SELECT_ALL_FROM_interfaces)
