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

###########################################
#
#                   TESTING
#
#
testing = True
showAllObjects = True
testingFiveRecordsOnly = False
#
############################################

import validRecords as vr
import getQuoteData as gqd
import convertQuotesToScenarios as cqts
import aggregateScenarios as ags
import scenarioAverages as sa
import pathlib
# import config
import sys
from pprint import pprint
from datetime import datetime
from datetime import timedelta

# adjust these to view results
minimumNumberOfEntries = 25
minimumAverageResultPercentage = 10

absolute_path = str(pathlib.Path(__file__).parent.resolve()) # wherever THIS file is
dbPath = absolute_path + '/../db/analyze-testing.db'
timeStart = datetime.now()
validRecords = vr.findValidRecords(dbPath) # get and store valid records
dayMoves = (1, 2, 3, 5, 7, 10, 14, 30)  # aka lengthOfMove
resultDays = (1, 2, 3, 5, 7, 10, 15, 30)
movePercentLows = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 30, 50, 75, 100)       # using these strictly for the loops below to build out all the combinations
movePercentHighs = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 30, 50, 75, 100, 101)    # 101 is used to represent anything above 100
movePercentCombos = []
volumeDeltaLows = (0, 5, 10, 15, 25, 50, 75, 100, 200, 500)      # using these strictly for the loops below to build out all the combinations
volumeDeltaHighs = (5, 10, 15, 25, 50, 75, 100, 200, 500, 501)   # 501 is used to represent anything above 500
volumeDeltaCombos = []
top1000StableCoins = ['USDT', 'USDC', 'DAI', 'FDUSD', 'USDD', 'TUSD', 'USDe', 'FRAX',
					'PYUSD', 'USDJ', 'USTC', 'CRVUSD', 'USDP', 'EURS', 'GUSD', 'LUSD',
					'vUSDC', 'USDX', 'BUSD', 'AEUR', 'vBUSD', 'SBD', 'RSV', 'SUSD',
					'EURC', 'EURt', 'CSUD', 'XSGD', 'vUSDT', 'USDK', 'ZUSD', 'USDV',
					'MKUSD', 'FEI', 'BIDR', 'GYEN'] # as of April 14, 2024 - sourced from: https://coinmarketcap.com/view/stablecoin/

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

    print('\n###############                   ###############')
    print('###############     Test Mode     ###############')
    print('###############                   ###############\n')

########################
#
#   Each valid API response will be a member of a group of API responses.
#   Each group much adhere to the requirements of the timeframe in between API responses to be 
#       considered a valid API response for that group.
#
#   For example:
#       If 45 consecutive days are found with API responses each day, analysis can be done for that entire group of responses.
#       If day 46 is missing an API response, then a new group must be made for the remainder of the records
#           since data will be missing for day 46.
#
#   Analysis will be done for one group at a time.
#
#   In an ideal situation, it is possible to go back and fill in the gaps in missing days.
#       I believe this can be accomplished using the coinmarketcap historical API endpoint.

APIGroupCounts = {}

#############################
#
#   APIGroupCounts (Dictionary)
#       Keys:   Group  ID
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

if testingFiveRecordsOnly:
    APIGroupCounts = {3: 5}

APIGroupCountTotal = 0

for k, v in APIGroupCounts.items():
    print('API Group ID: {}   Count: {}'.format(k, v))
    APIGroupCountTotal = APIGroupCountTotal + v

# get quote data for all valid records
SQLResults, distinctCoinIDs = gqd.getQuoteData(dbPath, APIGroupCounts, validRecords, top1000StableCoins, testing)

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

    print('Coin ID: {}   Total Volume: {:,.0f}   Coin Count: {}   Average Volume: {:,.0f}'.format(coinID, CoinVolumeTotal, CoinCount, AverageVolume))

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

APIDayCoinMembership = {} # what coins are included in each valid API run
APIGroupCoinMembership = {} # what coins are included in each API group (in theory they only need to appear at least on 1 day in the group)

for APIGroupID, APIDayID in SQLResults.items():

    APIGroupCoinMembership[APIGroupID] = []
    
    for APIDay, APIDayData in APIDayID.items():

        APIDayCoinMembership[APIDay] = []

        for coinID in APIDayData[2].keys():

            APIDayCoinMembership[APIDay].append(coinID)

            if coinID not in APIGroupCoinMembership[APIGroupID]:

                APIGroupCoinMembership[APIGroupID].append(coinID)

        APIDayCoinMembership[APIDay] = tuple(APIDayCoinMembership[APIDay]) # move from list to tuple
    
    APIGroupCoinMembership[APIGroupID] = tuple(APIGroupCoinMembership[APIGroupID]) # move from list to tuple

# print('API Day Coin Membership: {}'.format(APIDayCoinMembership))
# print('API Group Coin Membership: {}'.format(APIGroupCoinMembership))

Output, exceptionCount = cqts.convertQuotesToScenarios(SQLResults, APIGroupCoinMembership, dayMoves, resultDays, APIGroupCounts, coinAverageVolumes, movePercentCombos, volumeDeltaCombos)

print('Total Scenarios: {:,}'.format(len(Output)))

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

# aggregate the output

# Combos we are looking at: 
#
#   lengthOfMove            - dayMoves
#   qualifyingMoveRange     - movePercentCombos
#   qualifyingVolumeDelta   - volumeDeltaCombos
#   ResultDay               - ResultDay

# Output2 example:

# {
#     1: {                        # day moves (1, 2, 3, ... 30)
#         1: {                    # result day (1, 2, 3, ... 30)
#             (1, 2): {           # move percentage combinations ((1, 2),(1, 3), ... (100, 101))
#                 (0, 5): [       # volume change combinations ((0, 5),(0, 10), ... (0, 501))
#                     (
#                           1,    # output2Counter (1, 2, 3, 4, 5...)
#                         10.5,   # priceResultPercentage
#                         4.3,    # intermediateDayPercentageHigh
#                         -3.0    # intermediateDayPercentageLow
#                     ),
#                     ...
#                 ]      #      
#             }
#         }
#     }              
# }

print('Aggregating Scenarios...')

output2Counter, Output2, output2EmptyCombinations = ags.aggregateScenarios(Output, dayMoves, resultDays, movePercentCombos, volumeDeltaCombos)

print('Calculating Scenario Averages...\n')

# cyle though each aggregate scenario and record the average result % for each one.
scenarioResults, scenarioWithEntriesCount, maxScenarioEntryCount, positiveResultCount, negativeResultCount = sa.scenarioAverages(Output2, minimumNumberOfEntries, minimumAverageResultPercentage)






# Print all entities we've created:
if showAllObjects: # change to true if you'd like to see all variables we use in this script

    # for k, v in validRecords.items():
    #     print('KEY: {}   VALUE: {}'.format(k, v))

    for k, v in APIGroupCounts.items():
        print('API Key Group ID: {}   Count: {}'.format(k, v))

    if testing: # only print this if in testing mode (otherwise too long)
        # print('SQLResults dictionary:')   # OUTPUT TOO MUCH
        # pprint(SQLResults)                # OUTPUT TOO MUCH

        # print('Output: ')             # OUTPUT TOO LARGE
        # pprint(Output)                # OUTPUT TOO LARGE

        pass

    # print('distinct Coin IDs: \n{}'.format(distinctCoinIDs))
    print('\nCount of distinct Coin IDs: {}'.format(len(distinctCoinIDs)))
    print('API Group Count (total number of days): {}\n'.format(APIGroupCountTotal))
    # print('\nmove Percent Combonations: {}'.format(movePercentCombos))
    # print('\nvolume Delta Combonations: {}'.format(volumeDeltaCombos))
    # print('\ncoin Average Volumes: {}'.format(coinAverageVolumes))

    # l = len(distinctCoinIDs) * len(dayMoves) * len(movePercentCombos) * len(volumeDeltaCombos)
    # print('Estimated length of empty Output dict shell: {}'.format(l))

    # pprint(APIGroupCoinMembership)
    # pprint(APIDayCoinMembership)
print('###############                  ###############')
print('###############     Output 1     ###############')
print('###############                  ###############\n')

print('Total Scenarios: {:,}'.format(len(Output)))

# x = Output[0]
# print('\nOutput First Entry: \n')
# print('Coin ID: {}'.format(x[0]))
# print('Length Of Move: {} days'.format(x[1]))
# print('Qualifying Move Ranges: {}'.format(x[2]))
# print('Qualifying Result Volume Ranges: {}'.format(x[3]))
# print('Number of days to Result: {} days'.format(x[4]))
# print('Result %: {:.1f}%'.format(x[5]))
# print('Starting Price: ${:,.2f} - Result Price: ${:,.2f}'.format(x[6], x[7]))
# print('Average Relative Move Volume: {:,.1f}%'.format(x[8]))
# print('Stop loss High: {:.1f}% (${:,.2f})'.format(x[9], x[11]))
# print('Stop loss Low: {:.1f}% (${:,.2f})'.format(x[10], x[12]))
# print('Move % Change: {:.1f}'.format(x[13]))

# print("{:.1f}".format(my_float))

# print('\nOutput Last Entry: \n')
# x = Output[-1]
# print('Coin ID: {}'.format(x[0]))
# print('Length Of Move: {} days'.format(x[1]))
# print('Qualifying Move Ranges: {}'.format(x[2]))
# print('Qualifying Result Volume Ranges: {}'.format(x[3]))
# print('Number of days to Result: {} days'.format(x[4]))
# print('Result %: {:.1f}%'.format(x[5]))
# print('Starting Price: ${:,.2f} - Result Price: ${:,.2f}'.format(x[6], x[7]))
# print('Average Relative Move Volume: {:,.1f}%'.format(x[8]))
# print('Stop loss High: {:.1f}% (${:,.2f})'.format(x[9], x[11]))
# print('Stop loss Low: {:.1f}% (${:,.2f})'.format(x[10], x[12]))
# print('Move % Change: {:.1f}'.format(x[13]))

# print('\nOutput count: {:,}'.format(len(Output)))
# f'{len(Output):,}'

print('Exception Count: {:,}'.format(exceptionCount))
# f'{exceptionCount:,}'

print('\n###############                  ###############')
print('###############     Output 2     ###############')
print('###############                  ###############\n')

print('Empty Output 2 Combination Count: {:,}'.format(output2EmptyCombinations))
print('Output 2 Entries: {:,}'.format(output2Counter))

print('Output 2 First Entry:\n')

firstEntry = True
entryCounter = 0
for k1 in Output2.keys():
    for k2 in Output2[k1].keys():
        for k3 in Output2[k1][k2].keys():
            for k4 in Output2[k1][k2][k3].keys():
                if Output2[k1][k2][k3][k4]:
                    for t in Output2[k1][k2][k3][k4]:
                        entryCounter = entryCounter + 1
                    if firstEntry:      # only print this header info once
                        print('Day move: {}'.format(k1))
                        print('Result day: {}'.format(k2))
                        print('Move % range: {}'.format(k3))
                        print('Volume % range: {}'.format(k4))
                        print('Number of entries in this scenario: {:,}'.format(len(Output2[k1][k2][k3][k4])))
                        for t in Output2[k1][k2][k3][k4]:
                            print('---   ---   ---')
                            print('Entry #: {:,}'.format(t[0]))
                            print('Result Price %: {:.2f} %'.format(t[1]))
                            print('Stop loss HIGH: {:.2f} %'.format(t[2]))
                            print('Stop loss LOW: {:.2f} %'.format(t[3]))
                        firstEntry = False
                    if entryCounter == output2Counter: # if entryCounter # matches the Total number of entries (this should be the last one)
                        lastListLength = len(Output2[k1][k2][k3][k4]) # find how many entries are in this array. Because we could have already passed over a few.
                        print('\nOutput 2 Last Entry:\n')
                        print('Day move: {}'.format(k1))
                        print('Result day: {}'.format(k2))
                        print('Move % range: {}'.format(k3))
                        print('Volume % range: {}'.format(k4))
                        print('Number of entries in this scenario: {:,}'.format(len(Output2[k1][k2][k3][k4])))
                        while lastListLength > 0:
                            lastListLength = lastListLength - 1
                            print('---   ---   ---')
                            print('Entry #: {:,}'.format(Output2[k1][k2][k3][k4][lastListLength][0]))
                            print('Result Price %: {:.2f} %'.format(Output2[k1][k2][k3][k4][lastListLength][1]))
                            print('Stop loss HIGH: {:.2f} %'.format(Output2[k1][k2][k3][k4][lastListLength][2]))
                            print('Stop loss LOW: {:.2f} %'.format(Output2[k1][k2][k3][k4][lastListLength][3]))
                                
print('\n###############                          ###############')
print('###############     Scenario Results     ###############')
print('###############                          ###############\n')
                            
print('Number of Results: {:,}'.format(len(scenarioResults)))
print('Scenarios with Entries count: {:,}'.format(scenarioWithEntriesCount))
print('Max entry scenario count: {:,}'.format(maxScenarioEntryCount))
print('Average scenario entry count: {:.1f}'.format(output2Counter/scenarioWithEntriesCount))
print('Positive result count: {:,}'.format(positiveResultCount))
print('Negative result count: {:,}\n'.format(negativeResultCount))

scenarioResults = sorted(scenarioResults)
                        
print('First Result: {}'.format(scenarioResults[0]))
print('Second Result: {}'.format(scenarioResults[1]))
# print('First Result Details:')
# for entry in Output2[scenarioResults[0][2]][scenarioResults[0][3]][scenarioResults[0][4]][scenarioResults[0][5]]:
#     print('---   ---   ---')
#     print('Entry #: {:,}'.format(entry[0]))
#     print('Result Price %: {:.2f} %'.format(entry[1]))
#     print('Stop loss HIGH: {:.2f} %'.format(entry[2]))
#     print('Stop loss LOW: {:.2f} %'.format(entry[3]))

for x in scenarioResults:
    if x[0] > 0:
        # print('Positive Result: {}'.format(x))
        pass


# print('Day Move: {}'.format(Output2[30].values()))





print('\n###############                 ###############')
print('###############     Runtime     ###############')
print('###############                 ###############\n')

timeEnd = datetime.now()

s = (timeEnd-timeStart).seconds
if s < 60:
    print('Total runtime: {} Seconds\n'.format(s))
else:
    m = int(s/60)
    s = s%60
    print('Total runtime: {} Minutes {} Seconds\n'.format(m,s))


# further questions to ask ourselves after this:
#
#   - Is there possibly a trend the is positive but not necesarily based off the same time frame each time?
#   - If there is a trend, where is the best entry and stop loss?

#   TODO 
#
#   Each of these scenarios need ID's (possible a mapping table)