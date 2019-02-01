"""Queries for tables"""

STATIONS = "INSERT INTO devices(name, lab) VALUES(?, ?)"

SELECT_ALL_FROM_devices = "SELECT * FROM devices"
SELECT_ALL_FROM_interfaces = "SELECT * FROM interfaces"

INTERFACES = "INSERT INTO interfaces(name, number, speed, status) " \
             "VALUES(?, ?, ?, ?)"

INTERFACES_DELETE = "DELETE FROM interfaces WHERE name=?"
UPDATE_interfaces = "UPDATE interfaces" \
                    "SET name='port_name', number='port_number'"
