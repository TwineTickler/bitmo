#
#
#   
#   Here are some ideas of how we can experiment with this analyses:
#
#   For example:
#      How do the top 200 coins behave if Bitcoins moves up by 1% ?
#
#      When ever the majority of the top 200 coins move up by X %:
#         - How do they perform the following day?
#         - How do they perform in 3 days?
#         - How do they perform in 1 week?
#         - How do the others that did not move perform the following day?
#         - ect...
#
#       What happens the day after a coin moves X% or -X% ?
#
#           #################################
#           # coin # move # next day result #
#           #      #      #                 #
#
#           moves to look for:
#               >= 1% < 2%   and   >= -1% < -2%
#               >= 2% < 3%   and   etc...
#               >= 3% < 4%
#               >= 4% < 5%
#               >= 5% < 6%
#               >= 6% < 7%
#               >= 7% < 8%
#               >= 8% < 9%
#               >= 9% < 10%
#               >= 10% < 15%
#               >= 15% < 20%
#               >= 20% < 30%
#               >= 30% < 50%
#               >= 50% < 75%
#               >= 75% < 100%
#               >= 100%
#               
#               create an array to store low %'s and high %'s
#               lows = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 30, 50, 75, 100]
#               highs = [2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 30, 50, 75, 100]
#
#               then, create every permutation WHEN, high is greater than low.

#                   
#   Permutations:
#       Day-Moves:
#           Single    (Day 1 to day 2, day 2 to day 3, etc...)
#           Two-day   (Day 1 to day 3, day 2 to day 4, etc...)
#           3-day     (Day 1 to day 4, day 2 to day 5, etc...)
#           5-day     (Day 1 to day 6, day 2 to day 7, etc...)
#           Weekly    (Day 1 to day 8, day 2 to day 9, etc...)
#           10-day    (Day 1 to day 11, day 2 to day 12, etc...)
#           bi-weekly (Day 1 to day 15, day 2 to day 16, etc...)  
#           30-day    (Day 1 to day 31, day 2 to day 32, etc...)
#
#       Results of each of those moves:
#           1 day after
#           2 days after
#           3 days after
#           5 days after
#           7 days after
#           10 days after
#           14 days after
#           30 days after
#
#   IMPORTANT NOTES about Output:
#       These ARE NOT solely distinct instances. 
#       A instance can be PART of another instance.
#       What we need to do is FOR EACH scenario, give me ALL of the occurances of this scenario for this coin, 
#           and record each one and their result.
#       1 scenario:
#           length-of-move:             1 day   (can be 1, 2, 3, 5, 7, 10, ...)
#           distance of move:           1-2%    (can be 1-2%, 1-3%, 1-4%, 1-5%, 1-6%, 2-3%, 2-4%, 2-5%, ...)
#           average volume of move:     0-5%    (can be 0-5%, 0-10%, 0-25%, 0-50%, 5-10%, 5-25%, ...)
#           length of future result:    1 day   (can be 1, 2, 3, 5, ...)
#           
#   Output:
#       Dictionary:
#           Keys: coin ID (Ex 1, 5, 1047, etc)
#           Values: Dictionary:
#               Keys: length-of-move (1, 2, 3, 5, 7, 10, 14, 30 representing days)
#               Values: Dictionary:
#                   Keys: distance of move (Ex '1-2%', '2-3%', '-1-2%', etc...)
#                   Values: Dictionary: 
#                       Keys: average volume change % (past 24 hours) - average volume for all quotes of this currency, is above or below?
#                           (Ex '0-5%', '5-10%, '10-25%', '25-50%' '-0-5%', etc...)
#                       Values: Dictionary:
#                          Keys: length-of-future-move (1, 2, 3, 5, 7, 10, 14, 30 representing days)
#                          Values: tuple containing the Future %, beginning price, future price, and the opposite direction low or high in between that distance expressed in % and price
#                               (Ex ('5%', 25000, 27000, '25%', '-2%', 24000))
#                                   (% increase (decrease), beginning price, ending price, average volume change % for the period, highest/lowest % change in-between, high/low price in-between)
#
#
#       Example:
#
#       {
#           1: {                        # Coin ID
#               1: {                    # Length of move (1 day)
#                   '1%-2%': {          # Distance of the move
#                       '-0-5%': {      # Average volume change % (volume over this time period / average)
#                           3: (        # days to future result
#                               '5%',   # result % increase
#                               25000,  # starting price
#                               27000,  # result price
#                               '-24%'  # average volume change over this period (volume for this period compared with average daily vol)
#                               '-2%',  # highest/lowest % change over this period
#                               '24000' # high/low of price during this time period
#                           )
#                       }
#                   }
#               }
#           }
#       }
#
#   We need permutations for every aspect of the quote we are saving. These need to be defined as:
#
#   
#
#
#   Database Idea:
#       What if we stored the anaysis in a database?
#
#           Table - 
#               Coin - 
#               AnalyseTimeStart - 
#               AnalyseTimeEnd - 
#               Move (% up or down)
#               

import validRecords as vr
import config
import sqlite3
from pprint import pprint
from datetime import datetime
from datetime import timedelta

timeStart = datetime.now()
productionDB = '{}{}{}'.format(config.absolute_path,config.db_path,config.db_name)
validRecords = vr.findValidRecords()
SQLResults = {}

###########################################
#
#                   TESTING
#
#
testing = False
showAllObjects = False
#
############################################

#############################
#
#   validRecords (Dictionary)
#       Keys:   API download ID
#       Values: Tuple of the Group ID and timestamp
#
#   Example: 
#       {
#           1:
#           (1, '2023-05-30 23:30:00'),
#           2:
#           (1, '2023-05-31 23:00:00')
#       }

if testing:

    print('validRecords Object:')

    for k, v in validRecords.items():
        print('KEY: {}   VALUE: {}'.format(k, v))

APIGroupCounts = {}

#############################
#
#   APIGroupCounts (Dictionary)
#       Keys:   Groups
#       Values: Count of API Calls in that group
#
#   Example: 
#       {
#           1:
#           6
#       }
#

for k, v in validRecords.items():

    if v[0] not in APIGroupCounts.keys():
        
        APIGroupCounts[v[0]] = 1

    else:

        APIGroupCounts[v[0]] = APIGroupCounts[v[0]] + 1

if testing:
    APIGroupCounts = {3: 17}

print('\nAPIGroupCounts Object:')

for k, v in APIGroupCounts.items():
    print('API Key Group ID: {}   Count: {}'.format(k, v))



conn = sqlite3.connect(productionDB)
c = conn.cursor()





#####################################
#   FOR EACH - API Group
#####################################
for k, v in APIGroupCounts.items(): 

    if v > 2: # more than 2 records to analyse for this 

        print('\nQualifying API Group ID: {}   Count: {} - fetching from DB...'.format(k, v))

        # GET ALL date quotes for this currency WITH IN this API Group.

        #####################################
        #   FOR EACH - API Group
        #       FOR EACH - API Datetime
        #####################################
        for validRecordsKey, APIEntry in validRecords.items():

            if (APIEntry[0] == k): # if API Group ID's match in both validRecords and APIGroupCounts

                sql = 'SELECT id, symbol, price, volume_24h, volume_change_24h, percent_change_24h, percent_change_7d, percent_change_30d, market_cap, cmc_rank, num_market_pairs FROM quote WHERE insert_date BETWEEN \'{}\' AND \'{}\''.format((APIEntry[1] - timedelta(minutes=3)), (APIEntry[1] + timedelta(minutes=3)))
                if testing: # only 3 coins if testing
                    sql = 'SELECT id, symbol, price, volume_24h, volume_change_24h, percent_change_24h, percent_change_7d, percent_change_30d, market_cap, cmc_rank, num_market_pairs FROM quote WHERE insert_date BETWEEN \'{}\' AND \'{}\' AND id IN (1, 2, 3)'.format((APIEntry[1] - timedelta(minutes=3)), (APIEntry[1] + timedelta(minutes=3)))
                c.execute(sql)
                r = c.fetchall()

                # print('\nAPI Group ID: {}'.format(k))
                # print('\nSQL Result: {}'.format(r))

                # for record in r:

                #     print('\nAPI Group ID: {}'.format(k))
                #     print('\nSQL Result: {}'.format(record))

                # put ALL the SQL results into a massive Dictionary

                #############################################################
                #                                                           #
                #               Massive SQL Results Dictionary              #
                #                                                           #
                #############################################################

                # SQLResults (Dict)
                #
                #   {
                #       1: {                            # API Group ID
                #           1: [                        # API Day ID (key from validRecords)
                #               '2024-01-01 21:05:00',  # Day API Time LOW
                #               '2024-01-01 21:12:00',  # Day API Time HIGH
                #               {
                #                   1: (...)            # coin ID and it's data
                #                   2: (...)
                #                   3: (...)
                #               }
                #           ]
                #           2: [                        # API Day ID
                #               '2024-01-02 21:05:00',  # Day API Time LOW
                #               '2024-01-02 21:12:00',  # Day API Time HIGH
                #               {
                #                   1: (...)            # coin ID and it's data
                #                   2: (...)
                #                   3: (...)
                #               }
                #           ]
                #       }
                #       2: {...}                        # API Group ID...
                #   }

                # if API Group ID doesn't exist yet, add it.
                if k in SQLResults.keys():

                    # API group already in SQLResults
                    SQLResults[k][validRecordsKey] = [      # API Day ID
                        APIEntry[1] - timedelta(minutes=3), # Day API Time LOW
                        APIEntry[1] + timedelta(minutes=3), # Day API Time HIGH
                        {}
                    ]

                else:

                    # add first record in this API group
                    SQLResults[k] = {                           # API Group ID
                        validRecordsKey: [                      # API Day ID
                            APIEntry[1] - timedelta(minutes=3), # Day API Time LOW
                            APIEntry[1] + timedelta(minutes=3), # Day API Time HIGH
                            {}
                        ]
                    }

                # add each coin to SQL results
                for coinRecord in r:
                    
                    SQLResults[k][validRecordsKey][2][coinRecord[0]] = (coinRecord[1:])

                


        


#############################################################################
#                                                                           #
#
#       Should now have ALL the data we need in our SQLResults Dict         #
#
#                                                                           #
#############################################################################





















# Print all entities we've created:
if showAllObjects: # change to true if you'd like to see all variables we use in this script

    for k, v in validRecords.items():
        print('KEY: {}   VALUE: {}'.format(k, v))

    for k, v in APIGroupCounts.items():
        print('API Key Group ID: {}   Count: {}'.format(k, v))

    print('SQLResults dictionary:')
    pprint(SQLResults)

timeEnd = datetime.now()

print('\nTotal runtime: {} Seconds\n'.format((timeEnd-timeStart).seconds))

# further questions to ask ourselves after this:
#
#   - Is there possibly a trend the is positive but not necesarily based off the same time frame each time?
#   - If there is a trend, where is the best entry and stop loss?
