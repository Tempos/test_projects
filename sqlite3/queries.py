"""Insertion data for tables"""

# devices (<id>, name, lab)
STATIONS = ("INSERT INTO devices(name, lab) VALUES(?, ?)",
            [('some_name', 'some_lab'),
             ('another_name', 'another_lab'),
             ('one_more_name', 'one_more_lab')])

# interfaces (<device_id>, name, number, speed, status)
INTERFACES = ("INSERT INTO interfaces(name, number, speed, status) VALUES (?, ?, ?, ?)",
              [('WM', 1, 1000, 'up'),
               ('BS', 2, 1000, 'up')])

SELECT_ALL_DEVICES = "SELECT * FROM devices"
