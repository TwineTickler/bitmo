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

def scenarioAverages(
        Output2,
        minimumNumberOfEntries,
        minimumAverageResultPercentage
    ):

    scenarioResults = []
    maxScenarioEntryCount = 0
    scenarioWithEntriesCount = 0
    positiveResultCount = 0
    negativeResultCount = 0

    for k1 in Output2.keys():
        for k2 in Output2[k1].keys():
            for k3 in Output2[k1][k2].keys():
                for k4 in Output2[k1][k2][k3].keys():
                    if Output2[k1][k2][k3][k4]: # there are entries (tuples) in this List
                        scenarioWithEntriesCount = scenarioWithEntriesCount + 1
                        thisListLength = len(Output2[k1][k2][k3][k4])

                        if thisListLength > maxScenarioEntryCount: # find the MAX entries out of all scenarios
                            maxScenarioEntryCount = thisListLength

                        thisSumOfResultPercentage = 0

                        for t in Output2[k1][k2][k3][k4]: # this is a List of Tuples
                            thisSumOfResultPercentage = thisSumOfResultPercentage + t[1]

                        thisResultPercentageAverage = thisSumOfResultPercentage / thisListLength
                        
                        # add scenario to results
                        # THIS IS OUR SECRET SAUCE
                        # The average result for THIS move is either X greater or X lesser than your target.
                        if thisListLength >= minimumNumberOfEntries and (thisResultPercentageAverage >= minimumAverageResultPercentage or thisResultPercentageAverage <= -minimumAverageResultPercentage):

                            scenarioResults.append((thisResultPercentageAverage, thisListLength, k1, k2, k3, k4))

                            if thisResultPercentageAverage > 0: # count number of positive and negative results
                                positiveResultCount = positiveResultCount + 1
                            else:
                                negativeResultCount = negativeResultCount + 1

    return scenarioResults, scenarioWithEntriesCount, maxScenarioEntryCount, positiveResultCount, negativeResultCount


# Scenario Results:
#
#   [                       # list
#       (                   # tuple
#           10%,            # The Average Result % (thisResultPercentageAverage)
#           5,              # the number of occurances of this scenario (thisListLength)
#           3,              # day move (k1)
#           5,              # result day (k2)
#           (1, 2),         # the move % (k3 - move percentage combination)
#           (0, 5),         # volume change % (k4 - volume change combination)
#       ),
#       (
#           ...
#       )
#   ]
