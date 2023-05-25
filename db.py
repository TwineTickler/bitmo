# will be used for inserting, and selecting data from the database

import config
import log
import sqlite3
from datetime import datetime

database_path = config.absolute_path + config.db_path + config.db_name # build the path based off the config file

def open_db_connection():
    # Connect to the database
    log.log('database is: ' + database_path)

    try:
        conn = sqlite3.connect(database_path)
        log.log('connected to database')
    except:
        s = 'Error connecting to database'
        log.log(s)
        print(s)
        exit() # quit the program if we cannot connect to the database
    return conn

def close_db_connection(conn):
    # close the connection to the database
    try:
        conn.close()
        log.log('closed connection to database')
    except:
        s = 'Error closing connection to database'
        log.log(s)
        print(s)

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
                endpoint TEXT,
                insert_date NUMERIC
            )
        """)    
        log.log('response_status table is setup (created or already exists)')
    except:
        s = 'error creating response_status table'
        log.log(s)
        print(s)
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
                last_update NUMERIC,
                insert_date NUMERIC
            )
        ''')
        log.log('currency table is setup (created or already exists)')
    except:
        s = 'error creating currency table'
        log.log(s)
        print(s)
    try:
        c.execute('''
            CREATE TABLE IF NOT EXISTS quote (
                id INTEGER,
                currency_base TEXT,
                insert_date NUMERIC,
                price NUMERIC,
                volume_24h NUMERIC,
                volume_change_24h NUMERIC,
                percent_change_1h NUMERIC,
                percent_change_24h NUMERIC,
                percent_change_7d NUMERIC,
                percent_change_30d NUMERIC,
                percent_change_60d NUMERIC,
                percent_change_90d NUMERIC,
                market_cap NUMERIC,
                market_cap_dominance NUMERIC,
                last_updated_cmc NUMERIC
            )
        ''')
        log.log('quote table is setup (created or already exists)')
    except:
        s = 'error creating quote table'
        log.log(s)
        print(s)
    try:
        conn.commit() # commit the changes
    except:
        s = 'error commiting table setup changes'
        log.log(s)
        print(s)

def insert_response_status(conn, d):
    log.log('inserting response status into db')
    data_tuple = (
        d['timestamp'],
        d['error_code'],
        d['error_message'],
        d['elapsed'],
        d['credit_count'],
        '/v1/cryptocurrency/listings/latest', # hard coding this for now until we begin using another endpoint
        str(datetime.now()) # insert_date
    )
    sql = '''
        INSERT INTO response_status (
            timestamp, 
            error_code, 
            error_message, 
            elapsed, 
            credit_count, 
            endpoint, 
            insert_date
        )
        VALUES (?, ?, ?, ?, ?, ?, ?);
    '''
    c = conn.cursor()
    try:
        c.execute(sql, data_tuple)
        conn.commit()
        log.log('response status successfully inserted into db')
    except:
        s = 'error inserting into response_status table'
        log.log(s)
        print(s)

def save_currency(conn, d):
    # if currency doesn't exist yet, then INSERT it.
    # if it exists then UPDATE any data that has changed on it.
    # setup cursor
    c = conn.cursor()

    # run a select to see if it exists
    sql = 'SELECT * FROM currency where id = {};'.format(d['id']) # try to select the ID of the currency
    c.execute(sql)
    select_result = c.fetchall()

    if (len(select_result) > 0):
        log.log('currency id {} already exists, check for updates')
        print('one or more currency found')
        
        # lenth of the result SHOULD only be 1. If it's more than 1, throw an error.
        if (len(select_result) > 1):
            s = 'Error: the currency ID {} returned MORE than 1 result. The ID SHOULD be distinct in this table, please investigate'.format(d['id'])
            log.log(s)
            print(s)
            return False # return with an error

        # ONLY 1 result -> find what values need to be updated
        

    else:
        # insert new currency into the currency table
        log.log('no currency match found. Insert new entry')
        data_tuple = (
            d['id'],
            d['name'],
            d['symbol'],
            d['slug'],
            d['cmc_rank'],
            d['num_market_pairs'],
            d['infinite_supply'],
            d['last_updated'],
            str(datetime.now()), # last_update
            str(datetime.now())  # insert_date
        )
        # INSERT
        sql = '''
            INSERT INTO currency (
                id,
                name,
                symbol,
                slug,
                cmc_rank,
                num_market_pairs,
                infinite_supply,
                last_updated_cmc,
                last_update,
                insert_date
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        '''
        try:
            c.execute(sql, data_tuple)
            conn.commit()
            log.log('currency ID ' + str(d['id']) + ' (' + str(d['name']) + ') successfully inserted into currency table')
            return True # used to track errors.
        except:
            s = 'error inserting currency ID ' + str(d['id']) + ' (' + str(d['name']) + ') into currency table'
            log.log(s)
            print(s)
            return False # used to track if an error occurred.

    # TODO: we don't need to always insert all the data into this table.
    #       create logic that will only update data that has changed, IF the entry for the currency already exists.
    #       if we are doing an UPDATE instead of an INSERT, then log the changes that were made (OLD data -> NEW data)