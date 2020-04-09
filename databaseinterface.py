import sqlite3
from sqlite3 import Error
from datetime import datetime
now = str(datetime.now().isoformat())
#Database Schemas
sql_create_service_table = """ CREATE TABLE IF NOT EXISTS service (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    creation_date text
                                ); """
sql_create_passwords_table = """CREATE TABLE IF NOT EXISTS passwords (
                                id integer PRIMARY KEY,
                                usernamehash text NOT NULL,
                                passwordhash text NOT NULL,
                                salt text NOT NULL,
                                service_id integer NOT NULL,
                                creation_date text NOT NULL,
                                expiry_date text NOT NULL,
                                FOREIGN KEY (service_id) REFERENCES service (id)
                            );"""
service_row = """ INSERT INTO service (name,creation_date) VALUES(?,?)"""
password_row = """ INSERT INTO passwords (usernamehash,passwordhash,salt,service_id,creation_date,expiry_date) VALUES(?,?,?,?,?,?)"""

#### TO IMPLEMENT LATER ####
# sql_create_extrainfo_table = """CREATE TABLE IF NOT EXISTS extrainfo (
#                                 id integer PRIMARY KEY,
#                                 name_of_data text NOT NULL,
#                                 username text NOT NULL,
#                                 passwords_id integer NOT NULL,
#                                 FOREIGN KEY (passwords_id) REFERENCES passwords (id)
#                             );"""

def create_connection(db_file):
    """
    create a database connection to an SQLite database
    :param db_file: database file
    :return: Connection object of None
    """
    connection = None
    try:
        connection = sqlite3.connect(db_file)
        # print(sqlite3.version)
        #return connection
    except Error as e:
        print(e)
    return connection

def close_connection(connection):
    if connection:
        connection.close()

def create_default_tables(connection):
    # create tables
    if connection is not None:
        # create main services table based on scheme declared in variables
        create_table(connection, sql_create_service_table)
        #create passwords table based on schema declared in variable
        create_table(connection, sql_create_passwords_table)
        return connection
    else:
        print("Error! cannot create the database connection.")

def create_table(connection,create_table_sql):
    """
    create a table from the create_table_sql statement
    :param connection: connection object
    :param create_table_sql: a CREATE TABLE SQL statement
    :return:
    """
    try:
        c = connection.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def service_creation(database, service):
    #create a database connection
    connection = create_connection(database)
    # create_default_tables(connection)
    # create_service(connection,service)
    # close_connection(connection)
    with connection:
        #service_id = create_service(connection,service)
        create_default_tables(connection)
        try:
            c = connection.cursor()
            c.execute(service_row, service)
        except Error as e:
            print(e)
        return c.lastrowid
    # add code to close connection  """connection.close()"""

def password_creation(database,identity):
    #create a database connection
    connection = create_connection(database)
    with connection:
        create_default_tables(connection)
        try:
            c = connection.cursor()
            c.execute(password_row, identity)
        except Error as e:
            print(e)
        return c.lastrowid
    # add code to close connection  """connection.close()"""


def select_passwords_table(database):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    connection = create_connection(database)
    with connection:
        #create_default_tables(connection)
        try:
            c = connection.cursor()
            c.execute("SELECT * FROM passwords")
        except Error as e:
            print(e)
        rows = c.fetchall()   ### need to select each item seperately to release hash
        return rows

def select_service_table(database):
    connection = create_connection(database)
    with connection:
        #create_default_tables(connection)
        try:
            c = connection.cursor()
            c.execute("SELECT * FROM service")
        except Error as e:
            print(e)
        rows = c.fetchall()   ### need to select each item seperately to release hash
        return rows

def select_all_service_passwords(database,service_id):
    connection = create_connection(database)
    service_passwords_query = """SELECT service_id, service.name, passwords.usernamehash, passwords.passwordhash, passwords.salt, passwords.expiry_date FROM passwords INNER JOIN service ON passwords.service_id = service.id WHERE service.id="""+service_id+""";"""
    with connection:
        #create_default_tables(connection)
        try:
            c = connection.cursor()
            c.execute(service_passwords_query)
        except Error as e:
            print(e)
        rows = c.fetchall()   ### need to select each item seperately to release hash
        service_id, service_name, usernamehash, passwordhash, salt, expiry_date = rows[0]
        return service_id, service_name, usernamehash, passwordhash, salt, expiry_date

if __name__ == '__main__':
    main()