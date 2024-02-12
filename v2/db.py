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
#
#   NOTES:
#
#       Sqlite automatically creates a primary key autoincrement field for each table called ROWID
#
#   TABLES:
#
#       tags - keep track of which tags are active on cmc for any given currency
#
#           currencyID INTEGER
#               Foreign Key to the Currency ID column in the currency table
#               This ID is what is used by CMC to designate a unique currency
#
#           insertDate NUMERIC
#               datetime (UTC) the record was inserted
#
#           tag TEXT
#               the tag name
#
#           active INTEGER
#               can be either 0 (inactive) or 1 (active)
#               used to designate if this tag is currently included on cmc or not
#               most recent tags will be set to 1 (active)
#               any tag this is not included in a response will be marked as inactive
#
#       auditLog - record all UPDATES to any records in the DB
#
#           insertDate NUMERIC
#               datetime (UTC) the record was inserted
#
#           tableName TEXT
#               name of the table in which the record update took place
#
#           recordRowID INTEGER
#               the RowID of the record which was updated
#
#           column TEXT
#               the column name which was updated
#
#           oldValue TEXT
#               the value in the column before the update was made
#
#           newValue TEXT
#               the value in the column after the update was made
#
#           changeType TEXT
#               the type of change that was made to the record (INSERT, UPDATE, DELETE)
#               (currently all of these values should be UPDATE, unless I add others later to the program.)


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

    # NOTE: Sqlite automatically creates an Auto Increment Primary Key field titled ROWID

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
            """)
        
        c.execute('''
                CREATE TABLE IF NOT EXISTS currency (
                    insertDate NUMERIC,
                    lastModified NUMERIC,
                    currencyID INTEGER,
                    name TEXT,
                    symbol TEXT,
                    slug TEXT,
                    numMarketPairs INTEGER,
                    dateAdded NUMERIC,
                    maxSupply INTEGER,
                    circulatingSupply INTEGER,
                    totalSupply INTEGER,
                    infiniteSupply NUMERIC,
                    cmcRank INTEGER,
                    tvlRatio INTEGER,
                    lastUpdated NUMERIC
                )
            ''')
        
        c.execute('''
                CREATE TABLE IF NOT EXISTS quote (
                    currencyRowID INTEGER,
                    currencyID INTEGER,
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
        
        c.execute('''
                CREATE TABLE IF NOT EXISTS tags (
                    currencyID INTEGER,
                    insertDate NUMERIC,
                    tag TEXT,
                    active INTEGER
                )
            ''')

        c.execute('''
                CREATE TABLE IF NOT EXISTS auditLog (
                    insertDate NUMERIC,
                    tableName TEXT,
                    recordRowID INTEGER,
                    column TEXT,
                    oldValue TEXT,
                    newValue TEXT,
                    changeType TEXT
                )
            ''')
        
        conn.commit()

        result = True

        log.log('Verified DB tables are ready')
        
    except Exception as e:

        # log error message
        log.log('Error running createTables in db.py: {}'.format(e),1,1)

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

    result = True # if any exceptions occur, set this to False

    # save to the serverResponse Table
    
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
        log.log('serverResponse record successfully inserted into the database')

    except Exception as e:

        log.log('Error inserting record into serverResponse table: {}'.format(e),1,1)
        result = False

    # save the currencies
    #   for each currency in the response: 
    #       if it doesn't already exist, then create a record for it
    #       if it does, then update any value on the record that has changed (any updates should be logged in the auditLog)

    # get a list of all currencies ID's already in the database, to compare against.

    sql = 'SELECT currencyID FROM currency;'
    c.execute(sql)
    r = c.fetchall() # Example result: [(1830,), (8117,), (6350,), (1472,)]
    currenciesInTheDB = []
    for i in r: # moving this weird list of tuples into a normal list
        currenciesInTheDB.append(i[0])

    print('currencies in the DB: {}'.format(currenciesInTheDB))

    # TODO: build comparison to see if an update is needed. otherwise, insert.




    for i in q['data']:

        if i['id'] in currenciesInTheDB:
            
            # already in the DB --> UPDATE currency AND possibly tags
            # TODO
            pass

        else: # not in the DB yet --> INSERT INTO currency AND tags

            dataTuple = (
                str(datetime.now(timezone.utc)),    # insertDate        NUMERIC
                str(datetime.now(timezone.utc)),    # lastModified      NUMERIC
                i['id'],                            # currencyID        INTEGER
                i['name'],                          # name              TEXT
                i['symbol'],                        # symbol            TEXT
                i['slug'],                          # slug              TEXT
                i['num_market_pairs'],              # numMarketPairs    INTEGER
                i['date_added'],                    # dateAdded         NUMERIC
                i['max_supply'],                    # maxSupply         INTEGER
                i['circulating_supply'],            # circulatingSupply INTEGER
                i['total_supply'],                  # totalSupply       INTEGER
                i['infinite_supply'],               # infiniteSupply    NUMERIC
                i['cmc_rank'],                      # cmcRank           INTEGER
                i['tvl_ratio'],                     # tvlRatio          INTEGER
                i['last_updated']                   # lastUpdated       NUMERIC
            )

            sql = '''
                INSERT INTO currency (
                    insertDate,
                    lastModified,
                    currencyID,
                    name,
                    symbol,
                    slug,
                    numMarketPairs,
                    dateAdded,
                    maxSupply,
                    circulatingSupply,
                    totalSupply,
                    infiniteSupply,
                    cmcRank,
                    tvlRatio,
                    lastUpdated
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            '''

            try:

                c.execute(sql, dataTuple)
                conn.commit()
                log.log('currency record successfully inserted into the database')
            
            except Exception as e:

                log.log('Error inserting record into currency table: {}'.format(e),1,1)
                result = False

            # Insert the tags
        
            if len(i['tags']) > 0:

                for tag in i['tags']:

                    dataTuple = (
                        str(datetime.now(timezone.utc)),    # insertDate    NUMERIC
                        i['id'],                            # currencyID    INTEGER
                        tag,                                # tag           TEXT
                        1                                   # active        INTEGER
                    )

                    sql = '''
                        INSERT INTO tags (
                            insertDate,
                            currencyID,
                            tag,
                            active
                        )
                        VALUES (?, ?, ?, ?);
                    '''

                    try:

                        c.execute(sql, dataTuple)
                        conn.commit()
                        log.log('tag record successfully inserted into the database')

                    except Exception as e:

                        log.log('Error inserting record into tag table: {}'.format(e),1,1)
                        result = False
                    
            else:

                log.log('No tags to insert for this currency')





    # TODO: save the tags (new currency tags insert done)







    # TODO: save the quotes







    return result


def getLastSuccessfulCall(mode='sandbox'):

    #   mode
    #       'sandbox' (default), 'production', 'offline'
    #
    #   returns 
    #       datetime in UTC of last successful API call 
    #       OR 0 if none exists.
    pass



