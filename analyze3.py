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
#           15 days after
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
distinctCoinIDs = []
dayMoves = (1, 2, 3, 5, 7, 10, 14, 30)  # aka lengthOfMove
resultDays = (1, 2, 3, 5, 7, 10, 15, 30)
movePercentLows = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 30, 50, 75, 100)       # using these strictly for the loops below to build out all the combinations
movePercentHighs = (2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 30, 50, 75, 100, 101)    # 101 is used to represent anything above 100
movePercentCombos = []
volumeDeltaLows = (0, 5, 10, 15, 25, 50, 75, 100, 200, 500)      # using these strictly for the loops below to build out all the combinations
volumeDeltaHighs = (5, 10, 15, 25, 50, 75, 100, 200, 500, 501)   # 501 is used to represent anything above 500
volumeDeltaCombos = []

for l in movePercentLows:

    for h in movePercentHighs:

        if l < h:

            movePercentCombos.append((l, h))
            movePercentCombos.append((l * (-1), h * (-1)))

movePercentCombos = tuple(movePercentCombos) # move to a tuple to save memory

for l in volumeDeltaLows:

    for h in volumeDeltaHighs:

        if l < h:

            volumeDeltaCombos.append((l, h))
            volumeDeltaCombos.append((l * (-1), h * (-1)))

volumeDeltaCombos = tuple(volumeDeltaCombos) # move to a tuple to save memory

###########################################
#
#                   TESTING
#
#
testing = True
showAllObjects = True
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

    # print('validRecords Object:')

    # for k, v in validRecords.items():
    #     print('KEY: {}   VALUE: {}'.format(k, v))

    pass

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
    APIGroupCounts = {3: 17, 4: 62}
    

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
                    # 3 coins
                    sql = 'SELECT id, symbol, price, volume_24h, volume_change_24h, percent_change_24h, percent_change_7d, percent_change_30d, market_cap, cmc_rank, num_market_pairs FROM quote WHERE insert_date BETWEEN \'{}\' AND \'{}\' AND id IN (1, 2, 3)'.format((APIEntry[1] - timedelta(minutes=3)), (APIEntry[1] + timedelta(minutes=3)))
                    # 1 coin
                    # sql = 'SELECT id, symbol, price, volume_24h, volume_change_24h, percent_change_24h, percent_change_7d, percent_change_30d, market_cap, cmc_rank, num_market_pairs FROM quote WHERE insert_date BETWEEN \'{}\' AND \'{}\' AND id IN (1)'.format((APIEntry[1] - timedelta(minutes=3)), (APIEntry[1] + timedelta(minutes=3)))
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

                    # collect a distinct list of all coin ID's for later TODO

                    if coinRecord[0] not in distinctCoinIDs:

                        distinctCoinIDs.append(coinRecord[0])

# get Volume Averages for each coin for ALL days

coinAverageVolumes = {}

for coinID in distinctCoinIDs:

    CoinCount = 0
    CoinVolumeTotal = 0
    AverageVolume = 0

    for Group in SQLResults.values():

        for Day in Group.values():

            for coinID2, coinData in Day[2].items():

                if coinID == coinID2:

                    CoinCount = CoinCount + 1
                    CoinVolumeTotal = CoinVolumeTotal + coinData[2] # 24hr Volume

    AverageVolume = CoinVolumeTotal / CoinCount
    coinAverageVolumes[coinID] = AverageVolume

    print('Coin ID: {}   Total Volume: {}   Coin Count: {}   Average Volume: {}'.format(coinID, CoinVolumeTotal, CoinCount, AverageVolume))




#############################################################################
#                                                                           #
#
#       Should now have ALL the data we need in our SQLResults Dict         #
#
#                                                                           #
#############################################################################




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




# create a dictionary with API Day ID, coin membership.

# APIDayCoinMembership:
#
#   {
#       1: {                            # API Day ID
#           (1, 2, 3, 4, 5, etc...)     # Coin IDs
#       }
#   }

APIDayCoinMembership = {}
APIGroupCoinMembership = {}

for APIGroupID, APIDayID in SQLResults.items():

    APIGroupCoinMembership[APIGroupID] = []
    
    for APIDay, APIDayData in APIDayID.items():

        APIDayCoinMembership[APIDay] = []

        for coinID in APIDayData[2].keys():

            APIDayCoinMembership[APIDay].append(coinID)

            if coinID not in APIGroupCoinMembership[APIGroupID]:

                APIGroupCoinMembership[APIGroupID].append(coinID)

        APIDayCoinMembership[APIDay] = tuple(APIDayCoinMembership[APIDay])
    
    APIGroupCoinMembership[APIGroupID] = tuple(APIGroupCoinMembership[APIGroupID])


                
                

# Output Example:

#
#       {
#           1: {                        # Coin ID
#               1: {                    # Length of move (1 day)
#                   '1-2%': {           # Price Delta Range (%)
#                       '-0-5%': {      # Average volume delta range % (volume over this time period / average)
#                           3: (        # days to future result
#                               '5%',   # result % increase/decrease
#                               25000,  # starting price
#                               27000,  # result price
#                               '-24%'  # average volume change over this period (volume for this period compared with average daily vol)
#                               '2%',   # highest % change over this result (Intermediate Price Delta)
#                               '-2%',  # lowest % change over this result period (Intermediate Price Delta)
#                               '24000' # high of price during this result period
#                               '24000' # low of the price during this result period
#                           )
#                       }
#                   }
#               }
#           }
#       }

# Output Example:

#
#       {
#           1: {                        # Coin ID
#               1: {                    # Length of move (1 day)
#                   '1-2%': {           # Distance of the move
#                       '-0-5%': {      # Average volume change % (volume over this time period / average)
#                           3: (        # days to future result
#                               '5%',   # result % increase/decrease
#                               25000,  # starting price
#                               27000,  # result price
#                               '-24%'  # average volume change over this period (volume for this period compared with average daily vol)
#                               '-2%',  # highest/lowest % change over this period (Intermediate Price Delta +/-)
#                               '24000' # high/low of price during this time period
#                           )
#                       }
#                   }
#               }
#           }
#       }

# begin creating the Output Shell (ALL scenarios)
    # THEN add in the results

Output = {}

for coinID in distinctCoinIDs:

    ###############################
    #   FOR EACH coinID
    ###############################

    Output[coinID] = {}     # Coin ID
    
    for day in dayMoves:

        #########################################
        #   FOR EACH coinID
        #       FOR EACH dayMove (Length of move)
        #########################################

        Output[coinID][day] = {}    # Length of Move (dayMove)
        
        for distance in movePercentCombos:

            #########################################
            #   FOR EACH coinID
            #       FOR EACH dayMove (Length of move)
            #           FOR EACH distanceOfMove
            #########################################

            Output[coinID][day][distance] = {}  # Distance of the move in Percent
            
            for volumeDelta in volumeDeltaCombos:

                #############################################
                #   FOR EACH coinID
                #       FOR EACH dayMove (Length of move)
                #           FOR EACH distanceOfMove
                #               FOR EACH Average Volume Delta
                #############################################

                Output[coinID][day][distance][volumeDelta] = {}


# Shell setup, 
# begin analyzing and storing the results

#   Objects to consider (parameters)
#
#   Coin
#
#   Length of the initial Move
#
#   Distance of the initial Move
#
#   Volume Delta of the initial Move
#
#   Future result (Days)
#   
#   Results to track:
#       Price % Delta
#       Starting Price
#       Ending Price
#       Average Volume % Delta
#       Intermediate Price % Delta
#       Intermediate Price

exceptionCount = 0
outputCount = 0

for APIGroupID, APIDayDict in SQLResults.items():

    ##############################
    #   FOR EACH - API Group
    ##############################

    APIDayIDs = []

    for DayID in APIDayDict.keys():

        APIDayIDs.append(DayID)

    pprint('Day IDs (for this API group): {}'.format(APIDayIDs))

    # print('\nAPI Key Group ID: {}   Count: {}\n'.format(APIGroupID, APIGroupCount))

    # Determine the count of the coin in this group
    # actually forget this. Just try to start and calculate based off this coin ID.
    # if we are missing a reference, then we need to code around that and either use a None or NULL value.

    # APIGroupCoinCount = 0

    # for APIID in SQLResults[APIGroupID].keys():

    #     # FOR EACH APIID in the SQLResults FOR THIS API GROUP, how many times does this coin appear?

    #     if coinID in SQLResults[APIGroupID][APIID][2].keys():

    #         print('found an API call with this coin')

    for coin in APIGroupCoinMembership[APIGroupID]:

        ###############################
        #   FOR EACH coinID (in this API Group)
        ###############################

        pprint('API Group ID: {} - Coin ID: {}'.format(APIGroupID, coin))

        for lengthOfMove in dayMoves:

            ###############################
            #   FOR EACH length of move (how many days) = (1, 2, 3, 5, 7, 10, 14, 30) 
            ###############################

            # EX:
            #
            #   lengthOfMove = 1
            #
            #       StartDayID = 1
            #       EndDayID = 2 (StartDayID + lengthOfMove)
            #
            #       StartDayID = 2
            #       EndDayID = 3
            #
            #   lengthOfMove = 2
            #
            #       StartDayID

            for DayID in APIDayIDs:

                EndDayID = DayID + lengthOfMove

                for ResultDay in resultDays:

                    ResultDayID = EndDayID + ResultDay

                    if ResultDayID < (APIDayIDs[0] + APIGroupCounts[APIGroupID]):
                        
                        # Result Day is within the API Group Window
                        # We have a valid occurence to check

                        # print('API Group: {}   API Group Count: {}   Coin: {}   Length Of Move: {}   Start Day: {}   End Day: {}   Days To Result: {}   Result Day: {}'.format(
                        #     APIGroupID, 
                        #     APIGroupCounts[APIGroupID], 
                        #     coin, 
                        #     lengthOfMove, 
                        #     DayID, 
                        #     EndDayID, 
                        #     ResultDay,
                        #     ResultDayID
                        # ))

                        # BEGIN CALCULATIONS

                        # DO A TRY, if we FAIL it's probably becaseu we are missing a coin ID in this date range

                        try:

                            # 1: PRICE DELTA (%) Both for the Move and the Result

                            priceFirstDay = APIDayDict[DayID][2][coin][1]
                            priceLastDay = APIDayDict[EndDayID][2][coin][1]
                            priceResult = APIDayDict[ResultDayID][2][coin][1]
                            priceDifference = priceLastDay - priceFirstDay
                            movePercentage = (priceDifference * 100) / priceFirstDay
                            # 24h price change:  APIDayDict[EndDayID][2][coin][4]
                            priceResultPercentage = ((priceResult - priceLastDay) * 100) / priceLastDay


                            # print('  First Day Price: {}   Last Day Price: {}   Price Difference: {}   %: {}'.format(
                            #     priceFirstDay, 
                            #     priceLastDay, 
                            #     priceDifference, 
                            #     movePercentage
                            # ))

                            # print('    Result Price: {}   %: {}'.format(
                            #     priceResult,
                            #     priceResultPercentage
                            # ))

                            # 2: AVG VOLUME DELTA (%)

                                # compare the average volume for the MOVE PERIOD to the AVERAGE for the coin.

                            MoveVolumeTotal = 0
                            DayCount = 0

                            MoveVolumeDayID = DayID + 1

                            while MoveVolumeDayID <= EndDayID: # go through each day in the move (except the first one)

                                MoveVolumeTotal = MoveVolumeTotal + APIDayDict[MoveVolumeDayID][2][coin][2] # 2 = 24h volume

                                MoveVolumeDayID = MoveVolumeDayID + 1
                                DayCount = DayCount + 1

                            MoveVolumeAverage = MoveVolumeTotal / DayCount
                            MoveVolumeDifference = MoveVolumeAverage - coinAverageVolumes[coin]
                            MoveVolumeDifferencePercent = (MoveVolumeDifference * 100) / coinAverageVolumes[coin]

                            # print('      Move Volume Total: {}   Move Volume Average: {}   Coin Volume Average: {}   Difference: {}   %: {}'.format(
                            #     MoveVolumeTotal, 
                            #     MoveVolumeAverage,
                            #     coinAverageVolumes[coin],
                            #     MoveVolumeDifference,
                            #     MoveVolumeDifferencePercent
                            # ))

                            # 3: Intermediate Price AND Delta %

                                # if result price is higher (see how much lower % it dropped during time period between end of move and result)
                                # if result price is lower (see how much higher % it went during time period between end of move and result)
                                # we don't care about Day 1 or the Last Day in the series (DayID or EndDayID) - just everything in the middle

                            # if lengthOfMove > 1:

                            intermediateDayID = EndDayID + 1
                            intermediateDayPriceHigh = priceLastDay # last day's price
                            intermediateDayPriceLow = priceLastDay  # last day's price

                            while intermediateDayID < ResultDayID:

                                if APIDayDict[intermediateDayID][2][coin][1] < intermediateDayPriceLow:

                                    intermediateDayPriceLow = APIDayDict[intermediateDayID][2][coin][1]

                                if APIDayDict[intermediateDayID][2][coin][1] > intermediateDayPriceHigh:

                                    intermediateDayPriceHigh = APIDayDict[intermediateDayID][2][coin][1]

                                intermediateDayID = intermediateDayID + 1

                            intermediateDayDifferenceHigh = intermediateDayPriceHigh - priceLastDay
                            intermediateDayDifferenceLow = intermediateDayPriceLow - priceLastDay
                            intermediateDayPercentageHigh = (intermediateDayDifferenceHigh * 100) / priceLastDay
                            intermediateDayPercentageLow = (intermediateDayDifferenceLow * 100) / priceLastDay

                            # print('        Max Intermediate Price High: {}   Difference: {}   %: {}'.format(
                            #     intermediateDayPriceHigh,
                            #     intermediateDayDifferenceHigh,
                            #     intermediateDayPercentageHigh
                            # ))
                            # print('        Max Intermediate Price Low: {}   Difference: {}   %: {}'.format(
                            #     intermediateDayPriceLow,
                            #     intermediateDayDifferenceLow,
                            #     intermediateDayPercentageLow
                            # ))




                            # find qualifying move combinations and volume combonations
                            
                            qualifyingMovePercentCombos = []

                            for moveCombo in movePercentCombos:

                                # see which move Combos qualify for this move

                                if abs(moveCombo[1]) == 101: # logic is different for infinite (max) move scenarios

                                    if movePercentage > 0: # positive

                                        if 0 < moveCombo[0] <= movePercentage:

                                            qualifyingMovePercentCombos.append(moveCombo)

                                    else: # negative move

                                        if movePercentage <= moveCombo[0] < 0:

                                            qualifyingMovePercentCombos.append(moveCombo)

                                else:

                                    if movePercentage > 0: # positive

                                        if moveCombo[0] <= movePercentage < moveCombo[1]:

                                            qualifyingMovePercentCombos.append(moveCombo)

                                    else: # negative move

                                        if moveCombo[1] < movePercentage <= moveCombo[0]:

                                            qualifyingMovePercentCombos.append(moveCombo)

                            # print('  Move %: {}   Qualifying Combos: {}'.format(movePercentage, qualifyingMovePercentCombos))


                            qualifyingVolumeDeltaCombos = []

                            for volumeCombo in volumeDeltaCombos:

                                if abs(volumeCombo[1]) == 501: # max scenario

                                    if MoveVolumeDifferencePercent >= 0 and volumeCombo[1] > 0: # positive volume or zero

                                        if 0 <= volumeCombo[0] <= MoveVolumeDifferencePercent:

                                            qualifyingVolumeDeltaCombos.append(volumeCombo)

                                    if MoveVolumeDifferencePercent <= 0 and volumeCombo[1] < 0: # negative volume or zero

                                        if MoveVolumeDifferencePercent <= volumeCombo[0] <= 0:

                                            qualifyingVolumeDeltaCombos.append(volumeCombo)

                                else:   # not a max scenario

                                    if MoveVolumeDifferencePercent > 0: # positive volume

                                        if volumeCombo[0] <= MoveVolumeDifferencePercent < volumeCombo[1]:

                                            qualifyingVolumeDeltaCombos.append(volumeCombo)

                                    else: # negative volume

                                        if volumeCombo[1] < MoveVolumeDifferencePercent <= volumeCombo[0]:

                                            qualifyingVolumeDeltaCombos.append(volumeCombo)

                            # print('  Volume %: {}   Qualifying Combos: {}\n'.format(MoveVolumeDifferencePercent, qualifyingVolumeDeltaCombos))








                            # ADD all of these to the correct Output dictionary values:

# Output Example:

#
#       {
#           1: {                        # Coin ID
#               1: {                    # Length of move (1 day)
#                   '1-2%': {           # Price Move Delta Range (%)
#                       '-0-5%': {      # Average volume delta range % (volume over this time period / average)
#                           3: (        # days to future result
#                               '5%',   # result % increase/decrease
#                               25000,  # starting price
#                               27000,  # result price
#                               '-24%'  # average volume change over this period (volume for this period compared with average daily vol)
#                               '2%',   # highest % change over this result (Intermediate Price Delta)
#                               '-2%',  # lowest % change over this result period (Intermediate Price Delta)
#                               '24000' # high of price during this result period
#                               '24000' # low of the price during this result period
#                           )
#                       }
#                   }
#               }
#           }
#       }



                            for moveCombos in qualifyingMovePercentCombos:

                                for volumeCombos in qualifyingVolumeDeltaCombos:

                                    Output[coin][lengthOfMove][moveCombo][volumeCombos][ResultDay] = (
                                        priceResultPercentage,          # result %
                                        priceLastDay,                   # starting price (end of move)
                                        priceResult,                    # result price
                                        MoveVolumeDifferencePercent,    # average volume % during this move period
                                        intermediateDayPercentageHigh,
                                        intermediateDayPercentageLow,
                                        intermediateDayPriceHigh,
                                        intermediateDayPriceLow
                                    )

                                    outputCount = outputCount + 1






                        except Exception as e:

                            print('failed, probably missing a coin ID for thie scenario. Error: {}'.format(e))
                            exceptionCount = exceptionCount + 1







# Print all entities we've created:
if showAllObjects: # change to true if you'd like to see all variables we use in this script

    for k, v in validRecords.items():
        print('KEY: {}   VALUE: {}'.format(k, v))

    for k, v in APIGroupCounts.items():
        print('API Key Group ID: {}   Count: {}'.format(k, v))

    if testing: # only print this if in testing mode (otherwise too long)
        # print('SQLResults dictionary:')   # OUTPUT TOO MUCH
        # pprint(SQLResults)                # OUTPUT TOO MUCH

        # print('Output: ')             # OUTPUT TOO LARGE
        # pprint(Output)                # OUTPUT TOO LARGE

        pass

    print('distinct Coin IDs: \n{}'.format(distinctCoinIDs))
    print('\ncount of distinct Coin IDs: {}'.format(len(distinctCoinIDs)))
    print('\nmove Percent Combonations: {}'.format(movePercentCombos))
    print('\nvolume Delta Combonations: {}'.format(volumeDeltaCombos))
    # print('\ncoin Average Volumes: {}'.format(coinAverageVolumes))

    l = len(distinctCoinIDs) * len(dayMoves) * len(movePercentCombos) * len(volumeDeltaCombos)
    print('Estimated length of empty Output dict shell: {}'.format(l))

    pprint(APIGroupCoinMembership)
    pprint(APIDayCoinMembership)

    print('\nOutput count: {}'.format(f'{outputCount:,}'))



print('Exception Count: {}'.format(exceptionCount))

timeEnd = datetime.now()

s = (timeEnd-timeStart).seconds
if s < 60:
    print('\nTotal runtime: {} Seconds\n'.format(s))
else:
    m = int(s/60)
    s = s%60
    print('\nTotal runtime: {} Minutes {} Seconds\n'.format(m,s))


# further questions to ask ourselves after this:
#
#   - Is there possibly a trend the is positive but not necesarily based off the same time frame each time?
#   - If there is a trend, where is the best entry and stop loss?



#####################################################################################
#                                                                                   #
#           Don't think we need this below - but keeping in case we do              #
#                                                                                   #
#####################################################################################

# Output Example:

#
#       {
#           1: {                        # Coin ID
#               1: {                    # Length of move (1 day)
#                   '1-2%': {           # Distance of the move
#                       '-0-5%': {      # Average volume change % (volume over this time period / average)
#                           3: (        # days to future result
#                               '5%',   # result % increase/decrease
#                               25000,  # starting price
#                               27000,  # result price
#                               '-24%'  # average volume change over this period (volume for this period compared with average daily vol)
#                               '-2%',  # highest/lowest % change over this period (Intermediate Price Delta +/-)
#                               '24000' # high/low of price during this time period
#                           )
#                       }
#                   }
#               }
#           }
#       }

# begin creating the Output Shell (ALL scenarios)
    # THEN add in the results

# Output = {}

# for coinID in distinctCoinIDs:

#     ###############################
#     #   FOR EACH coinID
#     ###############################

#     Output[coinID] = {}     # Coin ID
    
#     for day in dayMoves:

#         #########################################
#         #   FOR EACH coinID
#         #       FOR EACH dayMove (Length of move)
#         #########################################

#         Output[coinID][day] = {}    # Length of Move (dayMove)
        
#         for distance in movePercentCombos:

#             #########################################
#             #   FOR EACH coinID
#             #       FOR EACH dayMove (Length of move)
#             #           FOR EACH distanceOfMove
#             #########################################

#             Output[coinID][day][distance] = {}  # Distance of the move in Percent
            
#             for volumeDelta in volumeDeltaCombos:

#                 #############################################
#                 #   FOR EACH coinID
#                 #       FOR EACH dayMove (Length of move)
#                 #           FOR EACH distanceOfMove
#                 #               FOR EACH Average Volume Delta
#                 #############################################

#                 Output[coinID][day][distance][volumeDelta] = {}