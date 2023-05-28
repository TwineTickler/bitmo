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
        s = 'ERROR: Error connecting to database'
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
        s = 'ERROR: Error closing connection to database'
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
        log.log('response_status table is setup')

    except:
        s = 'ERROR: Error creating response_status table'
        log.log(s)
        print(s)
        exit() # end the program here if tables are not setup

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
        log.log('currency table is setup')

    except:
        s = 'ERROR: Error creating currency table'
        log.log(s)
        print(s)
        exit() # end the program here if tables are not setup

    try:
        c.execute('''
            CREATE TABLE IF NOT EXISTS quote (
                id INTEGER,
                symbol TEXT,
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
        log.log('quote table is setup')

    except:
        s = 'ERROR: Error creating quote table'
        log.log(s)
        print(s)
        exit() # end the program here if tables are not setup

    try:
        conn.commit() # commit the changes

    except:
        s = 'ERROR: Error commiting table setup changes'
        log.log(s)
        print(s)
        exit() # end the program here if tables are not setup



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
        s = 'ERROR: Error inserting into response_status table. Please investigate!'
        log.log(s)
        log.log('Data Dump: ' + str(d)) # Data dumped into Log, needs investigation why it could not be inserted into DB
        print(s)



def save_currency(conn, d):
    # if currency doesn't exist yet, then INSERT it.
    # if it exists then UPDATE any data that has changed on it.
    # expects a return value of True or False.
    # if successful return True
    # if error return False

    # setup cursor
    c = conn.cursor()

    # run a select to see if it exists
    sql = 'SELECT * FROM currency where id = {};'.format(d['id']) # try to select the ID of the currency
    # sql = 'SELECT * FROM currency where id = 252' # used for testing
    # d['id'] = 252 # used for testing
    c.execute(sql)
    select_result = c.fetchall()
    # an example select_result:
    # [(252, 'w2cym56x6h', 'ov801b7pi1m', 'su6c1umozi', 8253, 7074, None, '2023-05-23T04:41:06.961Z', '2023-05-22 23:41:06.991538', '2023-05-22 23:41:06.991554')]
    # print(select_result) # used for testing

    if (len(select_result) > 0):
        log.log('currency ID {} already exists, verify only 1 match returned and then UPDATE the record'.format(d['id']))
        # print('one or more currency match found') # will remove this later after testing
        
        # lenth of the result SHOULD only be 1. If it's more than 1, throw an error.
        if (len(select_result) > 1):
            s = 'ERROR: the currency ID {} returned MORE than 1 result. The ID SHOULD be distinct in this table, please investigate'.format(d['id'])
            log.log(s)
            log.log('Data Dump: ' + str(d)) # dump the data into the log for later review
            print(s)
            return False # return with an error

        # two fields SHOULD NOT change (name and symbol)
        # If any of these two fields do not match, then throw an error and DO NOT UPDATE the record
        if (select_result[0][1] != d['name'] or select_result[0][2] != d['symbol']):
            s = 'ERROR: the currency ID {} does not match on either the NAME or SYMBOL field with what is in the db. These fields SHOULD NOT CHANGE. Please investiage'.format(d['id'])
            log.log(s)
            log.log('Data Dump: ' + str(d)) # dump the data into the log for later review
            print(s)
            return False # return with an error

        # ONLY 1 result -> find what values need to be updated
        log.log('updating currency ID {}'.format(d['id']))
        # begin building the SQL command to complete the UPDATE
        sql = 'UPDATE currency SET ' 
        data_tuple = ()

        # see which columns have changed and only update them.
        # and yes, technically, even if they have stayed the same we COULD have still updated them all, but this is a little cleaner.
        if (select_result[0][3] != d['slug']):
            # slug has changed, include it in the UPDATE
            sql += 'slug = ?, '
            data_tuple += (d['slug'],) # adding a tuple member to the list

        if (select_result[0][4] != d['cmc_rank']):
            # cmc_rank has changed, include it in the UPDATE
            sql += 'cmc_rank = ?, '
            data_tuple += (d['cmc_rank'],)

        if (select_result[0][5] != d['num_market_pairs']):
            # num_market_pairs has changed, include it in the UPDATE
            sql += 'num_market_pairs = ?, '
            data_tuple += (d['num_market_pairs'],)

        if (select_result[0][6] != d['infinite_supply']):
            # infinite_supply has changed, include it in the UPDATE
            sql += 'infinite_supply = ?, '
            data_tuple += (d['infinite_supply'],)

        # include the two columns that will be updated no matter what
        sql += 'last_updated_cmc = ?, last_update = ? WHERE id = ?'
        data_tuple += (d['last_updated'],str(datetime.now()),d['id'])
        log.log('OLD values: ' + str(select_result))
        # log.log('NEW values: ' + str(d['id']) + ) We could list out ALL the new values, but that will take a lot of log space. Only going to include the UPDATE statement for now.
        log.log('SQL statement: ' + sql)
        log.log('DATA: ' + str(data_tuple))

        try:
            c.execute(sql, data_tuple)
            conn.commit()
            log.log('currency ID {} successfully updated in db'.format(d['id']))
            return True # No error occurred
        
        except:
            s = 'ERROR: Error updating currency ID {} into currency table. Please investigate!'.format(d['id'])
            log.log(s)
            log.log('Data Dump: ' + str(d)) # dump the data into the log for later review
            print(s)
            return False # Error occurred

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
            s = 'ERROR: Error inserting currency ID ' + str(d['id']) + ' (' + str(d['name']) + ') into currency table. Please investigate!'
            log.log(s)
            log.log('Data Dump: ' + str(d)) # dump the data into the log for later review
            print(s)
            return False # used to track if an error occurred.
        


def save_quote(conn, d):
    # expects a return value
    # if successful return True
    # if error return False

    # setup cursor
    cur = conn.cursor()

    err = False # for error tracking in the for loop, so we know how to return.

    # the only thing we should be doing here is INSERT, no need for any updating.
    # for each currency, we will need to add an entry.
    currency_list = list(d['quote'].keys()) # d quote's value is it's own dictionary. Need the name of each key in it.
    # print(currency_list)

    for c in currency_list:
        
        single_quote_error = False # for tracking only one quote at a time.

        # add 3 missing dictionary key value pairs if in Sandbox environment:
        if (config.cmc_environment['environment'] == 'sandbox'):
            d['quote'][c]['percent_change_30d'] = 4.839483
            d['quote'][c]['percent_change_60d'] = -8.22839
            d['quote'][c]['percent_change_90d'] = 0.384733

        # for each currency base, setup the data and add an entry:
        try:
            data_tuple = (
                d['id'],
                d['symbol'],
                c, # currency_base
                str(datetime.now()), # insert_date
                d['quote'][c]['price'],
                d['quote'][c]['volume_24h'],
                d['quote'][c]['volume_change_24h'],
                d['quote'][c]['percent_change_1h'],
                d['quote'][c]['percent_change_24h'],
                d['quote'][c]['percent_change_7d'],
                d['quote'][c]['percent_change_30d'],
                d['quote'][c]['percent_change_60d'],
                d['quote'][c]['percent_change_90d'],
                d['quote'][c]['market_cap'],
                d['quote'][c]['market_cap_dominance'],
                d['quote'][c]['last_updated'] # last_updated_cmc
            )
        
        except:
            s = 'ERROR: failed to setup data_tuple properly for this quote. ID: {} currency_base: {}. Please investigate.'.format(d['id'],c)
            log.log(s)
            log.log('Data Dump: ' + str(d))
            print(s)
            err = True # error occurred for this quote
            single_quote_error = True

        sql = '''
            INSERT INTO quote (
                id,
                symbol,
                currency_base,
                insert_date,
                price,
                volume_24h,
                volume_change_24h,
                percent_change_1h,
                percent_change_24h,
                percent_change_7d,
                percent_change_30d,
                percent_change_60d,
                percent_change_90d,
                market_cap,
                market_cap_dominance,
                last_updated_cmc
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        '''

        # if error already occured, don't even try to insert
        if (not single_quote_error):

            try:
                cur.execute(sql, data_tuple)
                conn.commit()
                log.log('quote for ID: {} {} successfully inserted into quote table.'.format(d['id'], c))
            
            except Exception as ex:
                s = 'ERROR: Error inserting quote for ID: {} {}. {}'.format(d['id'], c, ex)
                log.log(s)
                log.log('Data Dump: ' + str(d)) # dump the data into the log for later review
                print(s)
                err = True # used to track if an error occurred.
        
    if (err):
        return False # there was an error
    else:
        return True
