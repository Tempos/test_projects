import sqlite3

db_path = "cars.db"

connect = sqlite3.connect(db_path)
cursor = connect.cursor()

view_data = (
    'Name',
    'Number',
    'Address',
    'Price',
    'Profile',
    'Information',
    'Link'
    )


def _exe_raw_sql(sql):
    try:
        cursor.execute(sql)
        fetchall = cursor.fetchall()
    except sqlite3.DatabaseError as err:
        raise err
    else:
        connect.commit()
    return fetchall


def create_bd():
    sql = """
    CREATE TABLE if not exists people(
        ID INTEGER PRIMARY KEY UNIQUE,
        Name VARCHAR(255) NOT NULL,
        Number VARCHAR(255) NOT NULL UNIQUE, 
        Address VARCHAR(255),     
        Price VARCHAR(255),
        Profile VARCHAR(255),
        Information VARCHAR(255),      
        Link VARCHAR(255)
        );
    """
    _exe_raw_sql(sql)
