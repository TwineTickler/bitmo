# will be used for inserting, and selecting data from the database

import config
import log
import sqlite3

database_path = config.absolute_path + config.db_path + config.db_name # build the path based off the config file

def initiate_db(t, d): # using t for type of database process, and d for the data
    # Connect to the database
    database_path = config.absolute_path + config.db_path + config.db_name # build the path based off the config file
    log.log('database is: ' + database_path)

    try:
        conn = sqlite3.connect(database_path)
        log.log('connected to database')
    except:
        log.log('Error connecting to database')
        print('Error connecting to database')

    # create the tables we need if they do not already exist
    c = conn.cursor()
    try:
        c.execute("""
            CREATE TABLE response_statuses (
                timestamp NUMERIC,
                error_code INTEGER,
                error_message TEXT,
                elapsed INTEGER,
                credit_count INTEGER
            )
        """)    
        log.log('created response_statuses table')
    except:
        log.log('Error creating response_statuses table (table probably already exists)')

    if (t == 'insert_status_response'):
        log.log('inserting status reponse into database')
        print('inserting status reponse into database')
        print(d)

    conn.commit()

    # close the connection to the database
    try:
        conn.close()
        log.log('closed connection to database')
    except:
        log.log('Error closing connection to database')

def open_db_connection():
    # Connect to the database
    log.log('database is: ' + database_path)

    try:
        sqlite3.connect(database_path)
        log.log('connected to database')
    except:
        log.log('Error connecting to database')
        print('Error connecting to database')

def close_db_connection():
    # close the connection to the database
    try:
        sqlite3.connect(database_path).close()
        log.log('closed connection to database')
    except:
        log.log('Error closing connection to database')