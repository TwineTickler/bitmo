#   Database file for use with version 2 of Bitmo
#
#
#
#
#

import config
import os
import log
import sqlite3

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


def createTables(conn):

    c = conn.cursor()

    c.execute("""
            CREATE TABLE IF NOT EXISTS serverResponse (
                timestamp NUMERIC,
                errorCode INTEGER,
                errorMessage TEXT,
                elapsed INTEGER,
                creditCount INTEGER,
                totalCount INTEGER,
                endpoint TEXT,
                insertDate NUMERIC
            )
        """)
    
    c.execute('''
            CREATE TABLE IF NOT EXISTS currency (
                id INTEGER,
                name TEXT,
                symbol TEXT,
                slug TEXT,
                cmcRank INTEGER,
                numMarketPairs INTEGER,
                infiniteSupply NUMERIC,
                lastUpdatedCmc NUMERIC,
                lastUpdate NUMERIC,
                insertDate NUMERIC
            )
        ''')
    
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
        ''')

    conn.commit()




def getLastSuccessfulCall(mode='sandbox'):

    #   mode
    #       'sandbox' (default), 'production', 'offline'
    #
    #   returns 
    #       datetime in UTC of last successful API call 
    #       OR 0 if none exists.
    pass



