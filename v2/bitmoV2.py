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
#           the largest cmc_rank you'd like to retrieve from the API. (going to start with 400)
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
#       All times should be in UTC time.
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
#       - Get a production API response and verify the DB entities are setup the way I want
#       - Update the sampleData.json with a production API response
#       - Saving a quote to the DB
#       - Timer
#
#

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
from datetime import datetime

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
    # db.createTables(conn)

    # call the API and return the result so we can confirm database objects

    q = getQuotes.getQuotes(mode, maxCmcRank)

    print('\nq.Status: {}'.format(q['status']))
    print('\nq.Data: {}\n'.format(q['data']))

    # dump contents of the API response into a file each time in json format, in the case we need it later.

    fileName = "{}/{}.json".format(apiResponsePath,datetime.today().strftime('%Y-%m-%d_%H:%M:%S'))

    try:
        with open(fileName, 'w') as fp:
            json.dump(q, fp)
    except Exception as e:
        message = 'Error creating apiResponse/ file: {}'.format(e)
        log.log(message,prnt=1)


    

    # setup timer

    # TODO

    # nextScheduledAPIcall





    log.log('reached the end of the program\n', prnt=1)



startProgram(mode='offline', maxCmcRank=15) # THIS is calling the program


















