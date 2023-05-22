# will be used for inserting, and selecting data from the database

import config
import log
import sqlite3

database_path = config.absolute_path + config.db_path + config.db_name # build the path based off the config file

def open_db_connection():
    # Connect to the database
    log.log('database is: ' + database_path)

    try:
        conn = sqlite3.connect(database_path)
        log.log('connected to database')
    except:
        log.log('Error connecting to database')
        print('Error connecting to database')
    return conn

def close_db_connection(conn):
    # close the connection to the database
    try:
        conn.close()
        log.log('closed connection to database')
    except:
        log.log('Error closing connection to database')
        print('Error closing connection to database')

def create_tables(conn):
    # create the tables we need if they do not already exist
    log.log('verifing tables are setup')
    c = conn.cursor()
    # create response_status table
    try:
        c.execute("""
            CREATE TABLE IF NOT EXISTS response_status (
                timestamp NUMERIC,
                error_code INTEGER,
                error_message TEXT,
                elapsed INTEGER,
                credit_count INTEGER,
                endpoint TEXT
            )
        """)    
        log.log('response_status table is setup (created or already exists)')
    except:
        log.log('error creating response_status table')
        print('error creating response_status table')
    try:
        c.execute('''
            CREATE TABLE IF NOT EXISTS currency (
                id INTEGER,
                name TEXT,
                symbol TEXT,
                slug TEXT,
                cmc_rank INTEGER,
                num_market_pairs INTEGER,
                infinite_supply NUMERIC,
                last_updated_cmc NUMERIC,
                last_insert NUMERIC,
                original_date_insert NUMERIC
            )
        ''')
        log.log('currency_data table is setup (created or already exists)')
    except:
        log.log('error creating currency table')
        print('error creating currency table')

    # next we need to create the quote table to store quote info each time to grab it: TODO
    #
    #
    #
    #
    
    try:
        conn.commit() # commit the changes
    except:
        log.log('error commiting table setup changes')
        print('error commiting table setup changes')

def insert_response_status(conn, d):
    log.log('inserting response status into db')
    data_tuple = (d['timestamp'],
                  d['error_code'],
                  d['error_message'],
                  d['elapsed'],
                  d['credit_count'],
                  '/v1/cryptocurrency/listings/latest' # hard coding this for now until we begin using another endpoint
                  )
    sql = '''
        INSERT INTO response_status
            (timestamp, error_code, error_message, elapsed, credit_count, endpoint)
            VALUES (?, ?, ?, ?, ?, ?);'''
    c = conn.cursor()
    try:
        c.execute(sql, data_tuple)
        conn.commit()
        log.log('response status successfully inserted into db')
    except:
        log.log('error inserting into response_status table')
        print('error inserting into response_status table')
    
