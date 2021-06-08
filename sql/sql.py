import sqlite3
from sqlite3 import Error
from sqlite3 import OperationalError

DATABASE = r"db\\umbra.db"
# SQL_FILE = 'sql\\populate_table.sql'
SQL_FILE = 'sql\\create_table.sql'

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

def main():
    conn = create_connection(DATABASE)

    if conn is not None:
        c = conn.cursor()
        executeScriptsFromFile(c, SQL_FILE)
    else:
        print("Error! cannot create the database connection.")

def executeScriptsFromFile(c, filename):
    # Open and read the file as a single buffer
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()

    # all SQL commands (split on ';')
    sqlCommands = sqlFile.split(';')

    # Execute every command from the input file
    for command in sqlCommands:
        # This will skip and report errors
        # For example, if the tables do not yet exist, this will skip over
        # the DROP TABLE commands
        try:
            c.execute(command)
        except OperationalError as msg:
            print("Command skipped: ", msg)

if __name__ == '__main__':
    main()