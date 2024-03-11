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
#       What happens the day after a coin moves X% or X% ?
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
#   Output:
#       Dictionary:
#           Keys: coin ID (Ex 1, 5, 1047, etc)
#           Values: Dictionary:
#               Keys: length-of-move (1, 2, 3, 5, 7, 10, 14, 30 representing days)
#               Values: Dictionary:
#                   Keys: distance of move (Ex '1%-2%', '2%-3%', '-1%-2%', etc...)
#                   Values: (tuple that contains the count, and a Dictionary:)
#                       Keys: length-of-future-move (1, 2, 3, 5, 7, 10, 14, 30 representing days)
#                       Values: Future %
#
#       Example:
#
#       {
#           1: {                # Coin ID
#               1: {            # Length of move (1 day)
#                   '1%-2%': (  # Distance of the move
#                       5,      # count of these moves
#                       {
#                           1:  # Length of future move (1 day)
#                           4%  # Future move %
#                       }
#                   )
#               }
#           }
#       }
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
from datetime import datetime
from datetime import timedelta

productionDB = '{}{}{}'.format(config.absolute_path,config.db_path,config.db_name)
validRecords = vr.findValidRecords()

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

for k, v in APIGroupCounts.items():
    print('API Key Group ID: {}   Count: {}'.format(k, v))



conn = sqlite3.connect(productionDB)
c = conn.cursor()






#####################################
#   FOR EACH - API Group
#####################################
for k, v in APIGroupCounts.items(): 

    if v > 2: # more than 2 records to analyse for this 

        print('Qualifying API Group ID: {}   Count: {}'.format(k, v))

        # GET ALL date quotes for this currency WITH IN this API Group.

        #####################################
        #   FOR EACH - API Group
        #       FOR EACH - API Datetime
        #####################################
        for APIEntry in validRecords.values():

            if (APIEntry[0] == k): # if API Group ID's match in both validRecords and APIGroupCounts

                sql = 'SELECT * FROM quote WHERE insert_date BETWEEN \'{}\' AND \'{}\''.format((APIEntry[1] - timedelta(minutes=3)), (APIEntry[1] + timedelta(minutes=3)))
                c.execute(sql)
                r = c.fetchall()

                for record in r:

                    print('\nAPI Group ID: {}'.format(k))
                    print('\nSQL Result: {}'.format(record))

                















# further questions to ask ourselves after this:
#
#   - Is there possibly a trend the is positive but not necesarily based off the same time frame each time?
#   - If there is a trend, where is the best entry and stop loss?
