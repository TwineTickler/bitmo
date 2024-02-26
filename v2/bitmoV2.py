#   Purpose:
#
#       - make an API call of a fixed schedule
#           every 5 min, 10, min, 30 min, etc. Smallest should be 1 minute.
#           only going to get a results from CMC based off cmc_rank. Currently thinking the top 1000
#           store the results in a database
#
#       - If API call is not successful:
#           log the attempt in the database as a failure.
#           (may want to add logic to re-try later based off API call frequency)
#
#   Parameters:
#
#       callFrequencyMinutes:
#           acceptable values:
#               integer from 1 - 1440: (1 minute to 1 day)
#           Represents the number of minutes in between API calls
#
#       maxCmcRank:
#           the largest number of quotes you'd like to retrieve from the API. (going to start with 400)
#           ordered from largest market cap to smallest
#           An API credit is used for ever 200 quotes received
#           expects integer > 0
#
#       mode: (specifies which environment to use.)
#           acceptable values:
#               'sandbox' (default), 'production', 'offline'
#           
#
#   Other Notes:
#
#       Sandbox, Production, and Simulation (offline) environments.
#           Sandbox will call the Sandbox API
#           Production will call Production API
#           Simulate will NOT call an API, but instead simulate a production insert with either a copy of a Production insert, or something similar.
#               This is for two reasons:
#                   1. Sometimes I will be working offline
#                   2. Sometimes their Sandbox data is not similar enough to production data.
#
#       All times that are recorded and created by this program should be in UTC time.
#
#       Major archetechural changes from version 1:
#
#           - When running the API call, there will be a separate file for this functionality (titled getQuotes.py) and returns the result to this function.
#               Then THIS function will call another DB function to save that data based on the result.
#           - I am REMOVING the functionality for requesting MORE than 5000 quotes per Timer Execution Instance.
#               Previously, I was gathering EVERY coin listed on CMC, but this data is not helpful.
#               The complexity is not worth the benefit, as the benefit is extremely minimal.
#               It would mean I would want data on coins that have a market cap less than the top 5,000 coins.
#               Most coins in this category are going to be junk, and not worth applying any kind of trading strategy towards.
#               This greatly simplifies the program.
#  
#
#   Remaining items to build:
#
#       - Saving a quote to the DB
#       - Timer (how do we want all these things bundled)
#           - try to get a quote (what context to handle failures)
#           - try to save a quote
#           - how to handle script failures?
#
#   Testing:
#
#       Verify the following:
#           - Console output
#           - log
#           - API Response dump file
#           - Entries in the database

################################################################################
#                                                                              #
#                                     SETUP                                    #
#                                                                              #
################################################################################

import log
import config
import db
import getQuotes
import json
import os
from datetime import datetime, timezone

def fatalError(message):
    message = 'FATAL ERROR: {}'.format(message)
    log.log(message,prnt=1)
    exit()

# First verify Logging is setup:

if (not log.checkLogPath(config.logPath)):
    m = 'Error setting up log path. Please investigate. Exiting the program...'
    print(m)
    exit()

# Verify apiResponses folder is setup:

apiResponsePath = '{}/apiResponses'.format(config.absolutePath)

if (not os.path.exists(apiResponsePath)):
    m = 'apiResponses folder does not exist. Creating it now...'
    log.log(m,1)

    try:
        os.mkdir(apiResponsePath)
    except Exception as e:
        fatalError('Error creating /apiResponses folder: {}'.format(e))

# find last successful API call

lastSuccessfulAPICall = db.getLastSuccessfulCall() # will be set to 0 if none exists

################################################################################
#                                                                              #
#                                     EXECUTE                                  #
#                                                                              #
################################################################################

def startProgram(
        callFrequencyMinutes=15,
        maxCmcRank=400,
        mode='sandbox'
    ):

    # verify parameters

    if not (
            (0 < callFrequencyMinutes < 1441) and 
            (maxCmcRank > 0) and 
            (mode == 'sandbox' or mode == 'production' or mode == 'offline')
        ):
        
        m = 'parameters not set correctly. callFrequencyMinutes={} maxCmCRank={} mode={}'.format(callFrequencyMinutes, maxCmcRank, mode)
        fatalError(m)
        
    else:
        # log parameters
        m = 'callFrequencyMinutes={} maxCmCRank={} mode={}'.format(callFrequencyMinutes, maxCmcRank, mode)
        log.log(m)

        if not mode == 'production':
            log.log('RUNNING IN {} MODE'.format(mode),1,1)

    # setup DB tables

    conn = db.openDBConnection(mode)

    # call the API and return the result so we can confirm database objects

    success, q, url = getQuotes.getQuotes(mode, maxCmcRank)
    # TODO if success is False, then this error needs to be handled by the timer.
    # retry X times
    # send a telegram message

    print('\nAPI fetch Success: {}'.format(success))

    # dump contents of the API response into a file each time in json format, in the case we need it later.

    fileName = "{}/{}.json".format(apiResponsePath,datetime.now(timezone.utc).strftime('%Y-%m-%d_%H-%M-%S'))

    if not mode == 'production':

        fileName = fileName[0:-5] + '_sandbox.json'

    try:

        with open(fileName, 'w') as fp:
            json.dump(q, fp, sort_keys=True, indent=4)
        log.log('API response dump file created: {}'.format(fileName))

    except Exception as e:

        message = 'Error creating apiResponse/ file: {}'.format(e)
        log.log(message,prnt=1)

    if success == False:
        # Error occurred fetching from the API
        log.log('Some kind of error occurred when fetching API data. Investigate.', 1, 1)

    elif not (q['serverResponse']['statusCode'] == 200):
        log.log('Problem with the server response. Investigate: {}'.format(q['serverResponse']), 1, 1)

    else: # good server response. Save the data.

        # print('\nq.Status: {}'.format(q['status']))
        # print('\nq.Data: {}'.format(q['data']))
        print('\nq.serverResponse: {}\n'.format(q['serverResponse']))

        # TODO Only save the quote and currency data if the response status is a 200
        # TODO How to handle response status codes that are NOT 200 and/or q.status.error_code does NOT equal 0

        # TODO, fairly rubust API calling established. Next:
        # begin work on function to save the data to the DB
    
        dbResponse = db.createTables(conn)

        if not dbResponse: # if this is false, fatal error.

            fatalError('Error setting up Tables in DB. Investigate.')

        dbResponse = db.saveQuote(conn, q, url)

        if not dbResponse: # if this is false, there was an error when trying to save this data.

            fatalError('Error saving the quote to the Database. Investigate.')

        else:

            log.log('quote successfully saved to the database.')




    # setup timer

    # TODO

    # nextScheduledAPIcall





    log.log('reached the end of the program\n', prnt=1)

# sandbox, production, offline
startProgram(callFrequencyMinutes=15, mode='sandbox', maxCmcRank=2) # THIS is calling the program


















