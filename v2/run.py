# Purpose:
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
# Variables:
#
#       callFrequencyMinutes:
#           expects integer from 1 - 1440: represents 1 minute to 1 day.
#       maxCmcRank:
#           the largest cmc_rank you'd like to retrieve from the API. (going to start with 1,000)
#           expects integer > 1
#
# Other Notes:
#
#       Sandbox, Production, and Simulation environments.
#           Sandbox will call the Sandbox API
#           Production will call Production API
#           Simulate will NOT call an API, but instead simulate a production insert with either a copy of a Production insert, or something similar.
#               This is for two reasons:
#                   1. Sometimes I will be working offline
#                   2. Sometimes their Sandbox data is not similar enough to production data.
#
#

################################################################################
#                                                                              #
#                                     SETUP                                    #
#                                                                              #
################################################################################

import log
import config

def fatalError(message):
    # log the error message
    print(message)
    exit()

################################################################################
#                                                                              #
#                                     EXECUTE                                  #
#                                                                              #
################################################################################

# First verify Logging is setup:

if (not log.checkLogPath(config.logPath)):
    m = 'Error setting up log path. Please investigate. Exiting the program...'
    print(m)
    exit()






















