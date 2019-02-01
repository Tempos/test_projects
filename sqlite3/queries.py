"""Queries for tables"""

STATIONS = ("INSERT INTO devices(name, lab) VALUES(?, ?)",
            [('some_name', 'some_lab'),
             ('another_name', 'another_lab'),
             ('one_more_name', 'one_more_lab')])

SELECT_ALL_FROM_devices = ("SELECT * FROM devices",)
SELECT_ALL_FROM_interfaces = ("SELECT * FROM interfaces",)

INTERFACES = ('''INSERT INTO interfaces(name, number, speed, status)
                VALUES(?, ?, ?, ?)''',
              [('WM', 1, 1000, 'up'),
               ('BS', 2, 1000, 'down'),
               ('BS', 2, 1000, 'down'),
               ('BS', 1, 100, 'up')])

INTERFACES_DELETE = ("DELETE FROM interfaces WHERE name=?",
                     ["BS"])
UPDATE_interfaces = '''UPDATE interfaces
                    SET name="port_name", number="port_number"'''

A = ("SELECT * FROM devices WHERE lab = ?", ("some_lab",))
B = ('''SELECT d.id, d.name, d.lab, i.name, i.number, i.speed, i.status
        FROM interfaces as i        
        INNER JOIN devices as d ON i.device_id = d.id        
        WHERE i.speed < ? AND i.status = ?''', (1000, "up",))
