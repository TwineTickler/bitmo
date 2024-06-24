Output = []
outputCount = 0
from pprint import pprint

def convertQuotesToScenarios(
        SQLResults,
        APIGroupCoinMembership,
        dayMoves,
        resultDays,
        APIGroupCounts,
        coinAverageVolumes,
        movePercentCombos,
        volumeDeltaCombos
    ):

    exceptionCount = 0

    # begin creating the Output Shell (ALL scenarios)
        # THEN add in the results

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

            # pprint('API Group ID: {} - Coin ID: {}'.format(APIGroupID, coin))

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
                            
                            exceptionTracker = False
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

                            except Exception:

                                # print('Error in section 1: {}'.format(e))
                                # print('API Day Dict (Day ID {}): {}'.format(DayID, APIDayDict[DayID]))
                                # print('API Day Dict (End Day ID {}): {}'.format(EndDayID, APIDayDict[EndDayID]))
                                # print('API Day Dict (Result Day ID {}): {}'.format(ResultDayID, APIDayDict[ResultDayID]))
                                exceptionTracker = True

                            try:
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

                            except Exception:

                                # print('Error in section 2: {}'.format(e))
                                exceptionTracker = True

                            try:
                                # 3: Intermediate Price AND Delta % (to determine stop loss)

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

                            except Exception:

                                # print('Error in section 3: {}'.format(e))
                                exceptionTracker = True

                            try:

                                # find qualifying move combinations and volume combonations
                                qualifyingMovePercentCombos = []

                                for moveCombo in movePercentCombos:

                                    # see which move Combos qualify for this move
                                    if abs(moveCombo[1]) == 101: # logic is different for infinite (max) move scenarios

                                        if movePercentage > 0: # positive
                                            if 0 <= moveCombo[0] <= movePercentage:
                                                qualifyingMovePercentCombos.append(moveCombo)

                                        else: # negative move

                                            if movePercentage <= moveCombo[0] <= 0:
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

    #   [
    #       (
    #           coinID,
    #           lengthOfMove,
    #           {(1, 2), (1, 3), (1, 4), ...},      # set of qualifying move ranges (1-2%, 1-3%)
    #           {(0, 5), (0, 10), (0, 15), ...},    # set of qualifying average volume delta ranges
    #           ResultDay,                          # number of days to result
    #           priceResultPercentage,          # result %
    #           priceLastDay,                   # starting price (end of move)
    #           priceResult,                    # ending price
    #           MoveVolumeDifferencePercent,    # volume (compared to average) during the move period
    #           intermediateDayPercentageHigh,
    #           intermediateDayPercentageLow,
    #           intermediateDayPriceHigh,
    #           intermediateDayPriceLow,
    #           movePercentage                  # change in % during the move
    #       )
    #   ]

                            except Exception:

                                # print('Error in section 4: {}'.format(e))
                                exceptionTracker = True

                            if not exceptionTracker:   # if no exceptions, then add it

                                # might need to remove this requirement for price result percentage
                                if len(qualifyingMovePercentCombos) > 0: #and abs(priceResultPercentage) >= 1:

                                    Output.append(
                                        (
                                            coin,
                                            lengthOfMove,
                                            qualifyingMovePercentCombos,
                                            qualifyingVolumeDeltaCombos,
                                            ResultDay,
                                            priceResultPercentage,
                                            priceLastDay,
                                            priceResult,
                                            MoveVolumeDifferencePercent,
                                            intermediateDayPercentageHigh,
                                            intermediateDayPercentageLow,
                                            intermediateDayPriceHigh,
                                            intermediateDayPriceLow,
                                            movePercentage
                                        )
                                    )

                                # sys.getsizeof('my list')
                                # then convert to tuple
                                # sys.getsizeof('my tuple')
                            
                            else:
                                exceptionCount = exceptionCount + 1

    return Output, exceptionCount