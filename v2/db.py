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
#       quote - 
#
#           serverResponseRowID INTEGER
#               Foreign Key to dbo.serverResponse
#               Used to link a quote record directly to the API call it arrived on
#
#       tags - keep track of which tags are active on cmc for any given currency
#
#           currencyID INTEGER
#               Foreign Key to the Currency ID column in the currency table
#               This ID is what is used by CMC to designate a unique currency
#
#           serverResponseRowID INTEGER
#               Foreign Key to dbo.serverResponse
#               Used to identify which API call it arrived in
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
#               the RowID of the record which was updated.
#               ( this is a hidden Identity Auto-Increment column on ALL tables )
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

import random # FOR TESTING
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
                    serverResponseRowID INTEGER,
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
                    serverResponseRowID INTEGER,
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

    ######################################################
    #              save to dbo.serverResponse            #
    ######################################################

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

    ######################################################
    #               save to dbo.currency                 #
    ######################################################

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

    # print('currencies in the DB: {}\n'.format(currenciesInTheDB))


    # q['data'][0]['max_supply'] = random.randrange(1, 1000) # TESTING
    # q['data'][0]['slug'] = 'text{}'.format(random.randrange(1, 9)) # TESTING
    # q['data'][0]['numMarketPairs'] = random.randrange(1, 1000) # TESTING
    # q['data'][1]['symbol'] = 'BTC{}'.format(random.randrange(1, 9)) # TESTING


    for newCurrencyRecord in q['data']: # newCurrencyRecord = each currency in the CMC API Response

        if newCurrencyRecord['id'] in currenciesInTheDB: # currency already in the DB --> UPDATE dbo.currency AND possibly dbo.tags
            
            # first grab the dbo.currency record, then compare it.

            sql = 'SELECT RowID, name, symbol, slug, numMarketPairs, dateAdded, maxSupply, circulatingSupply, totalSupply, infiniteSupply, cmcRank, tvlRatio, lastUpdated FROM currency WHERE currencyID = {}'.format(newCurrencyRecord['id'])
            c.execute(sql)
            existingCurrencyRecord = c.fetchall()

            # print('this currency is already in the database: {}'.format(existingCurrencyRecord))

            sql = 'UPDATE currency SET ' # begin building the SQL for the UPDATE and for the AuditLog
            auditLogSQL = 'INSERT INTO auditLog (insertDate, tableName, recordRowID, column, oldValue, newValue, changeType) VALUES'
            auditLogDataTuple = ()

            ###################################################################
            #               check for dbo.currency.name update                #
            ###################################################################

            if existingCurrencyRecord[0][1] != newCurrencyRecord['name']: # name doesn't match, update this field

                sql += 'name = "{}"'.format(newCurrencyRecord['name'])

                log.log('name field to be updated: {} --> {}'.format(existingCurrencyRecord[0][1], newCurrencyRecord['name']), 1, 1)

                auditLogSQL += '(?, ?, ?, ?, ?, ?, ?)' # ADD to the Audit Log

                auditLogDataTuple = auditLogDataTuple + (
                    str(datetime.now(timezone.utc)),    # insertDate    NUMERIC
                    'currency',                         # tableName     TEXT
                    existingCurrencyRecord[0][0],       # recordRowID   INTEGER
                    'name',                             # column        TEXT
                    existingCurrencyRecord[0][1],       # oldValue      TEXT
                    newCurrencyRecord['name'],          # newValue      TEXT
                    'UPDATE'                            # changeType    TEXT
                )

            ###################################################################
            #               check for dbo.currency.symbol update              #
            ###################################################################

            if existingCurrencyRecord[0][2] != newCurrencyRecord['symbol']:

                if '=' in sql:

                    sql += ', '

                sql += 'symbol = "{}"'.format(newCurrencyRecord['symbol'])

                log.log('symbol field to be updated: {} --> {}'.format(existingCurrencyRecord[0][2], newCurrencyRecord['symbol']), 1, 1)

                if '?' in auditLogSQL:

                    auditLogSQL += ', '

                auditLogSQL += '(?, ?, ?, ?, ?, ?, ?)' # ADD to the Audit Log

                auditLogDataTuple = auditLogDataTuple + (
                    str(datetime.now(timezone.utc)),    # insertDate    NUMERIC
                    'currency',                         # tableName     TEXT
                    existingCurrencyRecord[0][0],       # recordRowID   INTEGER
                    'symbol',                           # column        TEXT
                    existingCurrencyRecord[0][2],       # oldValue      TEXT
                    newCurrencyRecord['symbol'],        # newValue      TEXT
                    'UPDATE'                            # changeType    TEXT
                )

            ###################################################################
            #               check for dbo.currency.slug update                #
            ###################################################################

            if existingCurrencyRecord[0][3] != newCurrencyRecord['slug']:

                if '=' in sql:

                    sql += ', '

                sql += 'slug = "{}"'.format(newCurrencyRecord['slug'])

                log.log('slug field to be updated: {} --> {}'.format(existingCurrencyRecord[0][3], newCurrencyRecord['slug']), 1, 1)

                if '?' in auditLogSQL:

                    auditLogSQL += ', '

                auditLogSQL += '(?, ?, ?, ?, ?, ?, ?)' # ADD to the Audit Log

                auditLogDataTuple = auditLogDataTuple + (
                    str(datetime.now(timezone.utc)),    # insertDate    NUMERIC
                    'currency',                         # tableName     TEXT
                    existingCurrencyRecord[0][0],       # recordRowID   INTEGER
                    'slug',                             # column        TEXT
                    existingCurrencyRecord[0][3],       # oldValue      TEXT
                    newCurrencyRecord['slug'],          # newValue      TEXT
                    'UPDATE'                            # changeType    TEXT
                )

            #############################################################################
            #               check for dbo.currency.numMarketPairs update                #
            #############################################################################

            if existingCurrencyRecord[0][4] != newCurrencyRecord['num_market_pairs']:

                if '=' in sql:

                    sql += ', '

                sql += 'numMarketPairs = {}'.format(newCurrencyRecord['num_market_pairs'])

                log.log('numMarketPairs field to be updated: {} --> {}'.format(existingCurrencyRecord[0][4], newCurrencyRecord['num_market_pairs']), 1, 0)

                if '?' in auditLogSQL:

                    auditLogSQL += ', '

                auditLogSQL += '(?, ?, ?, ?, ?, ?, ?)' # ADD to the Audit Log

                auditLogDataTuple = auditLogDataTuple + (
                    str(datetime.now(timezone.utc)),        # insertDate    NUMERIC
                    'currency',                             # tableName     TEXT
                    existingCurrencyRecord[0][0],           # recordRowID   INTEGER
                    'numMarketPairs',                       # column        TEXT
                    existingCurrencyRecord[0][4],           # oldValue      TEXT
                    newCurrencyRecord['num_market_pairs'],  # newValue      TEXT
                    'UPDATE'                                # changeType    TEXT
                )

            #############################################################################
            #               check for dbo.currency.dateAdded update                     #
            #############################################################################

            if existingCurrencyRecord[0][5] != newCurrencyRecord['date_added']:

                if '=' in sql:

                    sql += ', '

                sql += 'dateAdded = "{}"'.format(newCurrencyRecord['date_added'])

                log.log('dateAdded field to be updated: {} --> {}'.format(existingCurrencyRecord[0][5], newCurrencyRecord['date_added']), 1, 1)

                if '?' in auditLogSQL:

                    auditLogSQL += ', '

                auditLogSQL += '(?, ?, ?, ?, ?, ?, ?)' # ADD to the Audit Log

                auditLogDataTuple = auditLogDataTuple + (
                    str(datetime.now(timezone.utc)),        # insertDate    NUMERIC
                    'currency',                             # tableName     TEXT
                    existingCurrencyRecord[0][0],           # recordRowID   INTEGER
                    'dateAdded',                            # column        TEXT
                    existingCurrencyRecord[0][5],           # oldValue      TEXT
                    newCurrencyRecord['date_added'],        # newValue      TEXT
                    'UPDATE'                                # changeType    TEXT
                )

            #############################################################################
            #               check for dbo.currency.maxSupply update                     #
            #############################################################################

            if existingCurrencyRecord[0][6] != newCurrencyRecord['max_supply']:

                if '=' in sql:

                    sql += ', '

                sql += 'maxSupply = {}'.format(newCurrencyRecord['max_supply'])

                log.log('maxSupply field to be updated: {} --> {}'.format(existingCurrencyRecord[0][6], newCurrencyRecord['max_supply']), 1, 0)

                if '?' in auditLogSQL:

                    auditLogSQL += ', '

                auditLogSQL += '(?, ?, ?, ?, ?, ?, ?)' # ADD to the Audit Log

                auditLogDataTuple = auditLogDataTuple + (
                    str(datetime.now(timezone.utc)),        # insertDate    NUMERIC
                    'currency',                             # tableName     TEXT
                    existingCurrencyRecord[0][0],           # recordRowID   INTEGER
                    'maxSupply',                            # column        TEXT
                    existingCurrencyRecord[0][6],           # oldValue      TEXT
                    newCurrencyRecord['max_supply'],        # newValue      TEXT
                    'UPDATE'                                # changeType    TEXT
                )

            #############################################################################
            #               check for dbo.currency.circulatingSupply update             #
            #############################################################################

            if existingCurrencyRecord[0][7] != newCurrencyRecord['circulating_supply']:

                if '=' in sql:

                    sql += ', '

                sql += 'circulatingSupply = {}'.format(newCurrencyRecord['circulating_supply'])

                log.log('circulatingSupply field to be updated: {} --> {}'.format(existingCurrencyRecord[0][7], newCurrencyRecord['circulating_supply']), 1, 0)

                if '?' in auditLogSQL:

                    auditLogSQL += ', '

                auditLogSQL += '(?, ?, ?, ?, ?, ?, ?)' # ADD to the Audit Log

                auditLogDataTuple = auditLogDataTuple + (
                    str(datetime.now(timezone.utc)),        # insertDate    NUMERIC
                    'currency',                             # tableName     TEXT
                    existingCurrencyRecord[0][0],           # recordRowID   INTEGER
                    'circulatingSupply',                    # column        TEXT
                    existingCurrencyRecord[0][7],           # oldValue      TEXT
                    newCurrencyRecord['circulating_supply'],# newValue      TEXT
                    'UPDATE'                                # changeType    TEXT
                )

            #############################################################################
            #               check for dbo.currency.totalSupply update                   #
            #############################################################################

            if existingCurrencyRecord[0][8] != newCurrencyRecord['total_supply']:

                if '=' in sql:

                    sql += ', '

                sql += 'totalSupply = {}'.format(newCurrencyRecord['total_supply'])

                log.log('totalSupply field to be updated: {} --> {}'.format(existingCurrencyRecord[0][8], newCurrencyRecord['total_supply']), 1, 0)

                if '?' in auditLogSQL:

                    auditLogSQL += ', '

                auditLogSQL += '(?, ?, ?, ?, ?, ?, ?)' # ADD to the Audit Log

                auditLogDataTuple = auditLogDataTuple + (
                    str(datetime.now(timezone.utc)),        # insertDate    NUMERIC
                    'currency',                             # tableName     TEXT
                    existingCurrencyRecord[0][0],           # recordRowID   INTEGER
                    'totalSupply',                          # column        TEXT
                    existingCurrencyRecord[0][8],           # oldValue      TEXT
                    newCurrencyRecord['total_supply'],      # newValue      TEXT
                    'UPDATE'                                # changeType    TEXT
                )

            #############################################################################
            #               check for dbo.currency.infiniteSupply update                #
            #############################################################################

            if existingCurrencyRecord[0][9] != newCurrencyRecord['infinite_supply']:

                if '=' in sql:

                    sql += ', '

                sql += 'infiniteSupply = {}'.format(newCurrencyRecord['infinite_supply'])

                log.log('infiniteSupply field to be updated: {} --> {}'.format(existingCurrencyRecord[0][9], newCurrencyRecord['infinite_supply']), 1, 0)

                if '?' in auditLogSQL:

                    auditLogSQL += ', '

                auditLogSQL += '(?, ?, ?, ?, ?, ?, ?)' # ADD to the Audit Log

                auditLogDataTuple = auditLogDataTuple + (
                    str(datetime.now(timezone.utc)),        # insertDate    NUMERIC
                    'currency',                             # tableName     TEXT
                    existingCurrencyRecord[0][0],           # recordRowID   INTEGER
                    'infiniteSupply',                       # column        TEXT
                    existingCurrencyRecord[0][9],           # oldValue      TEXT
                    newCurrencyRecord['infinite_supply'],   # newValue      TEXT
                    'UPDATE'                                # changeType    TEXT
                )

            ######################################################################
            #               check for dbo.currency.cmcRank update                #
            ######################################################################

            if existingCurrencyRecord[0][10] != newCurrencyRecord['cmc_rank']:

                if '=' in sql:

                    sql += ', '

                sql += 'cmcRank = {}'.format(newCurrencyRecord['cmc_rank'])

                log.log('cmcRank field to be updated: {} --> {}'.format(existingCurrencyRecord[0][10], newCurrencyRecord['cmc_rank']), 1, 0)

                if '?' in auditLogSQL:

                    auditLogSQL += ', '

                auditLogSQL += '(?, ?, ?, ?, ?, ?, ?)' # ADD to the Audit Log

                auditLogDataTuple = auditLogDataTuple + (
                    str(datetime.now(timezone.utc)),        # insertDate    NUMERIC
                    'currency',                             # tableName     TEXT
                    existingCurrencyRecord[0][0],           # recordRowID   INTEGER
                    'cmcRank',                              # column        TEXT
                    existingCurrencyRecord[0][10],          # oldValue      TEXT
                    newCurrencyRecord['cmc_rank'],          # newValue      TEXT
                    'UPDATE'                                # changeType    TEXT
                )

            ######################################################################
            #               check for dbo.currency.tvlRatio update               #
            ######################################################################

            if existingCurrencyRecord[0][11] != newCurrencyRecord['tvl_ratio']:

                if '=' in sql:

                    sql += ', '

                sql += 'tvlRatio = {}'.format(newCurrencyRecord['tvl_ratio'])

                log.log('tvlRatio field to be updated: {} --> {}'.format(existingCurrencyRecord[0][11], newCurrencyRecord['tvl_ratio']), 1, 0)

                if '?' in auditLogSQL:

                    auditLogSQL += ', '

                auditLogSQL += '(?, ?, ?, ?, ?, ?, ?)' # ADD to the Audit Log

                auditLogDataTuple = auditLogDataTuple + (
                    str(datetime.now(timezone.utc)),        # insertDate    NUMERIC
                    'currency',                             # tableName     TEXT
                    existingCurrencyRecord[0][0],           # recordRowID   INTEGER
                    'tvlRatio',                             # column        TEXT
                    existingCurrencyRecord[0][11],          # oldValue      TEXT
                    newCurrencyRecord['tvl_ratio'],         # newValue      TEXT
                    'UPDATE'                                # changeType    TEXT
                )

            #########################################################################
            #               check for dbo.currency.lastUpdated update               #
            #########################################################################

            if existingCurrencyRecord[0][12] != newCurrencyRecord['last_updated']:

                if '=' in sql:

                    sql += ', '

                sql += 'lastUpdated = "{}"'.format(newCurrencyRecord['last_updated'])

                log.log('lastUpdated field to be updated: {} --> {}'.format(existingCurrencyRecord[0][12], newCurrencyRecord['last_updated']), 1, 0)

                if '?' in auditLogSQL:

                    auditLogSQL += ', '

                auditLogSQL += '(?, ?, ?, ?, ?, ?, ?)' # ADD to the Audit Log

                auditLogDataTuple = auditLogDataTuple + (
                    str(datetime.now(timezone.utc)),        # insertDate    NUMERIC
                    'currency',                             # tableName     TEXT
                    existingCurrencyRecord[0][0],           # recordRowID   INTEGER
                    'lastUpdated',                           # column        TEXT
                    existingCurrencyRecord[0][12],          # oldValue      TEXT
                    newCurrencyRecord['last_updated'],       # newValue      TEXT
                    'UPDATE'                                # changeType    TEXT
                )


            print('length of auditLogDataTuple: {}'.format(len(auditLogDataTuple)))
            

            if len(auditLogDataTuple) > 0: # if we have at least one field that has changed. Update the record.

                sql += ', lastModified = "{}"'.format(datetime.now(timezone.utc))
                sql += ' WHERE currencyID = {}'.format(newCurrencyRecord['id'])

                print('\nUPDATE statement: {}'.format(sql))
                print('\nAuditLogSQL: {}\n\nAuditLogData: {}\n\n'.format(auditLogSQL, auditLogDataTuple))

                try:

                    c.execute(sql)
                    c.execute(auditLogSQL, auditLogDataTuple)
                    conn.commit()

                    log.log('dbo.currency record successfully updated')
                
                except Exception as e:

                    log.log('Error updating record into dbo.currency: {}'.format(e),1,1)
                    result = False






            # TODO check if there are any updates needed to the dbo.tags record

            # first grab the dbo.tags record, then compare it.



        else: # not in the DB yet --> INSERT INTO dbo.currency AND dbo.tags

            dataTuple = (
                str(datetime.now(timezone.utc)),            # insertDate        NUMERIC
                str(datetime.now(timezone.utc)),            # lastModified      NUMERIC
                newCurrencyRecord['id'],                    # currencyID        INTEGER
                newCurrencyRecord['name'],                  # name              TEXT
                newCurrencyRecord['symbol'],                # symbol            TEXT
                newCurrencyRecord['slug'],                  # slug              TEXT
                newCurrencyRecord['num_market_pairs'],      # numMarketPairs    INTEGER
                newCurrencyRecord['date_added'],            # dateAdded         NUMERIC
                newCurrencyRecord['max_supply'],            # maxSupply         INTEGER
                newCurrencyRecord['circulating_supply'],    # circulatingSupply INTEGER
                newCurrencyRecord['total_supply'],          # totalSupply       INTEGER
                newCurrencyRecord['infinite_supply'],       # infiniteSupply    NUMERIC
                newCurrencyRecord['cmc_rank'],              # cmcRank           INTEGER
                newCurrencyRecord['tvl_ratio'],             # tvlRatio          INTEGER
                newCurrencyRecord['last_updated']           # lastUpdated       NUMERIC
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
                log.log('dbo.currency record successfully inserted')
            
            except Exception as e:

                log.log('Error inserting record into dbo.currency: {}'.format(e),1,1)
                result = False

            # Insert the tags
        
            if len(newCurrencyRecord['tags']) > 0:

                for tag in newCurrencyRecord['tags']:

                    dataTuple = (
                        str(datetime.now(timezone.utc)),    # insertDate    NUMERIC
                        newCurrencyRecord['id'],            # currencyID    INTEGER
                        tag,                                # tag           TEXT
                        1                                   # active        INTEGER
                    )

                    # TODO include the serverResponseRowID ( need to find it and then include it )

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
                        log.log('dbo.tag record successfully inserted')

                    except Exception as e:

                        log.log('Error inserting record into dbo.tag: {}'.format(e),1,1)
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



