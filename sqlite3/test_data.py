"""Data, needed for queries."""

# devices (<id>, name, lab)
STATIONS_INSERT = [('some_name', 'some_lab'),
                   ('another_name', 'another_lab'),
                   ('one_more_name', 'one_more_lab')]

# interfaces (<device_id>, name, number, speed, status)
INTERFACES_INSERT = [('WM', 1, 1000, 'up'),
                     ('BS', 2, 1000, 'up')]

ROW_NAME = ['BS']
