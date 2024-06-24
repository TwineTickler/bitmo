
def aggregateScenarios(
    Output, 
    dayMoves, 
    resultDays, 
    movePercentCombos,
    volumeDeltaCombos
    ):

    Output2 = {}
    output2EmptyCombinations = 0

    for lengthOfMove in dayMoves:   # (1, 2, 3, 5, 7, 10, 14, 30)  # aka lengthOfMove

        Output2[lengthOfMove] = {}

        for rDay in resultDays:

            Output2[lengthOfMove][rDay] = {}

            for moveCombo in movePercentCombos:

                Output2[lengthOfMove][rDay][moveCombo] = {}

                for volumeCombo in volumeDeltaCombos:

                    Output2[lengthOfMove][rDay][moveCombo][volumeCombo] = []
                    output2EmptyCombinations = output2EmptyCombinations + 1

    output2Counter = 0

    for aScenario in Output:    # for each entry in Output

        for lengthOfMove in Output2.keys():    # for each length of move

            if aScenario[1] == lengthOfMove:    # if length of move matches the Output entry move

                for rDay in Output2[lengthOfMove].keys():

                    if aScenario[4] == rDay:

                        for moveCombo in Output2[lengthOfMove][rDay].keys():

                            for moveComboS in aScenario[2]:

                                if moveCombo == moveComboS:

                                    for volumeCombo in Output2[lengthOfMove][rDay][moveCombo].keys():

                                        for volumeComboS in aScenario[3]:

                                            if volumeCombo == volumeComboS:

                                                output2Counter = output2Counter + 1

                                                Output2[lengthOfMove][rDay][moveCombo][volumeCombo].append((
                                                    output2Counter,
                                                    aScenario[5],
                                                    aScenario[9],
                                                    aScenario[10]
                                                ))

    return output2Counter, Output2, output2EmptyCombinations


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