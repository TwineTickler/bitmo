#   Database file for use with version 2 of Bitmo
#
#
#   functions:
#
#       openDBConnection (mode)
#           
#           returns: conn
#
#       closeDBConnection (conn)
#
#           returns: N/A
#
#       createTables (conn)
#
#           returns: 
#               result (True or False)
#
#       saveQuote (conn, q)
#
#           parameters:
#               conn - 
#               q - 
#               url - 
#
#           returns: 
#               result - True or False depending on if the save to the DB was successful (True) or not (False)
#
#       getLastSuccessfulCall (mode)
#
#           returns: N/A
#

import config
import os
import log
import sqlite3
from datetime import datetime, timezone

# setup database filenames

sandboxDB = '{}bitmoV2-sandbox.db'.format(config.dbPath)
productionDB = '{}bitmoV2-prod.db'.format(config.dbPath)

def openDBConnection(mode='sandbox'):

    # if path does not exist, create it
    if (not os.path.exists(config.dbPath)):

        log.log('missing database folder. Creating path...')
        os.mkdir(config.dbPath)

    if (mode == 'sandbox' or mode == 'offline'):
        DB = sandboxDB
    elif (mode == 'production'):
        DB = productionDB

    try:
        conn = sqlite3.connect(DB)
        log.log('connected to database: {} successfully.'.format(DB))

    except:
        log.log('FATAL Error connecting to database: {}'.format(DB),1)
        exit()

    return conn


def closeDBConnection(conn):

    # close the connection to the database
    try:
        conn.close()
        log.log('closed connection to database')

    except:
        log.log('error closing db connection',1,1)


#########################################################################
#                                                                       #
#                           Create Tables                               #
#                                                                       #
#########################################################################


def createTables(conn):

    result = False

    try:
        c = conn.cursor()

        c.execute("""
                CREATE TABLE IF NOT EXISTS serverResponse (
                    insertDate NUMERIC,
                    serverStatusCode INTEGER,
                    serverReason TEXT,
                    timestamp NUMERIC,
                    errorCode INTEGER,
                    errorMessage TEXT,
                    elapsed INTEGER,
                    creditCount INTEGER,
                    notice TEXT,
                    totalCount INTEGER,
                    endpoint TEXT
                )
            """) # This table is good.
        
        c.execute('''
                CREATE TABLE IF NOT EXISTS currency (
                    insertDate NUMERIC,
                    id INTEGER,
                    name TEXT,
                    symbol TEXT,
                    slug TEXT,
                    numMarketPairs INTEGER,
                    maxSupply INTEGER,
                    circulatingSupply INTEGER
                    totalSupply INTEGER,
                    infiniteSupply NUMERIC,
                    cmcRank INTEGER,
                    tvlRatio INTEGER,
                    lastUpdated NUMERIC,
                    lastModified NUMERIC
                )
            ''') # this table looks good.
        
        c.execute('''
                CREATE TABLE IF NOT EXISTS quote (
                    id INTEGER,
                    symbol TEXT,
                    currencyBase TEXT,
                    insertDate NUMERIC,
                    price NUMERIC,
                    volume24h NUMERIC,
                    volumeChange24h NUMERIC,
                    percentChange1h NUMERIC,
                    percentChange24h NUMERIC,
                    percentChange7d NUMERIC,
                    percentChange30d NUMERIC,
                    percentChange60d NUMERIC,
                    percentChange90d NUMERIC,
                    marketCap NUMERIC,
                    marketCapDominance NUMERIC,
                    lastUpdatedCmc NUMERIC,
                    cmcRank INTEGER,
                    numMarketPairs INTEGER
                )
            ''') # checking this table...
        
        conn.commit()

        result = True

        log.log('Verified db tables are ready')
        
    except Exception as e:

        # log error message
        log.log('Error running createTables in db.py: {}'.format(e),0,1)

    return result


#########################################################################
#                                                                       #
#                           Save Quote                                  #
#                                                                       #
#########################################################################


def saveQuote(conn, q, url):

    #   parameters:
    #       conn
    #           context for the current database connection (production, or sandbox data file)
    #       q
    #           the API quote data returned from the endpoint
    #       url
    #           the URL of the endpoint that was queried
    #
    #   returns:
    #       True or False depending on if the save to the DB was successful (True) or not (False)
    
    # a quote will have 3 parts:
    #   1. status
    #       serverResponse Table
    #   2. data
    #       currency Table
    #       quote Table
    #   3. serverResponse
    #       serverResponse Table

    result = False

    # first save to the serverResponse Table
    
    dataTuple = (
        str(datetime.now(timezone.utc)),    # insertDate        NUMERIC
        q['serverResponse']['statusCode'],  # serverStatusCode  INTEGER
        q['serverResponse']['reason'],      # serverReason      TEXT
        q['status']['timestamp'],           # timestamp         NUMERIC
        q['status']['error_code'],          # errorCode         INTEGER
        q['status']['error_message'],       # errorMessage      TEXT
        q['status']['elapsed'],             # elapsed           INTEGER
        q['status']['credit_count'],        # creditCount       INTEGER
        q['status']['notice'],              # notice            TEXT
        q['status']['total_count'],         # totalCount        INTEGER
        str(url)                            # endpoint          TEXT
    )
    
    sql = '''
        INSERT INTO serverResponse (
            insertDate,
            serverStatusCode,
            serverReason,
            timestamp,
            errorCode,
            errorMessage,
            elapsed,
            creditCount,
            notice,
            totalCount,
            endpoint
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    '''

    c = conn.cursor()

    try:

        c.execute(sql, dataTuple)
        conn.commit()
        result = True
        log.log('serverResponse record successfully inserted into the database')

    except Exception as e:

        log.log('Error inserting record into serverResponse table: {}'.format(e),1,1)

    # save to the quote and currency Tables



    

    return result


def getLastSuccessfulCall(mode='sandbox'):

    #   mode
    #       'sandbox' (default), 'production', 'offline'
    #
    #   returns 
    #       datetime in UTC of last successful API call 
    #       OR 0 if none exists.
    pass



