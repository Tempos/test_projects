"""Queries for tables"""

STATIONS = ("INSERT INTO devices(name, lab) VALUES(?, ?)",
            [('some_name', 'some_lab'),
             ('another_name', 'another_lab'),
             ('one_more_name', 'one_more_lab')])

SELECT_ALL_FROM_devices = ("SELECT * FROM devices",)
SELECT_ALL_FROM_interfaces = ("SELECT * FROM interfaces",)

INTERFACES = ('''INSERT INTO interfaces(device_id, name, number, speed, status)
                 VALUES(?, ?, ?, ?, ?)''',
              [(1, 'ether', 1, 1000, 'up'),
               (1, 'ether', 2, 1000, 'down'),
               (3, 'ether', 2, 1000, 'down'),
               (3, 'WM',    2, 10,   'down'),
               (3, 'WM',    2, 10,   'down'),
               (3, 'WM',    2, 10,   'down'),
               (3, 'ether', 2, 1000, 'down'),
               (3, 'ether', 2, 1000, 'down'),
               (3, 'BS',    2, 1000, 'down'),
               (2, 'ether', 1, 100,  'up')])

INTERFACES_DELETE = ("DELETE FROM interfaces WHERE name=?",
                     ["BS"])

UPDATE_interfaces = ('''UPDATE interfaces 
                        SET name=?
                        WHERE name = ?''', ("vlan", "WM"))

SELECT_W_CONDITION = ("SELECT * FROM devices WHERE lab = ?", ("some_lab",))

JOIN = ('''SELECT d.id, d.name, d.lab, i.name, i.number, i.speed, i.status
        FROM interfaces as i        
        INNER JOIN devices as d ON i.device_id=d.id     
        WHERE i.speed < ? AND i.status = ?''', (2000, "down",))
