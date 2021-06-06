import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute("""DROP TABLE games;""")
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def populate_table(conn, populate_table_sql):
    try:
        c = conn.cursor()
        c.execute(populate_table_sql)
    except Error as e:
        print(e)

def commit(conn):
    try:
        c = conn.cursor()
        c.execute("COMMIT")
    except Error as e:
        print(e)

def main():
    database = r"umbra.db"

    # sql_create_table = """ CREATE TABLE IF NOT EXISTS games (
    sql_create_table = """CREATE TABLE games (
                              id INTEGER PRIMARY KEY,
                              name TEXT NOT NULL,
                              game_id INTEGER NOT NULL,
                              path TEXT NOT NULL,
                              args TEXT,
                              favorite BOOLEAN NOT NULL
                          )"""

    sql_populate_table = """INSERT INTO games (name, game_id, path, favorite)
                            VALUES 
                                ("test1", 1,"C:\\Program Files\\Notepad++\\notepad++.exe", false),
                                ("test2", 2,"C:\\Program Files\\Notepad++\\notepad++.exe", true);"""

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_table)
        
        populate_table(conn, sql_populate_table)

        commit(conn)
    else:
        print("Error! cannot create the database connection.")

if __name__ == '__main__':
    main()