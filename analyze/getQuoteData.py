#   Notes
#
#   

import sqlite3
from datetime import timedelta
SQLResults = {}
distinctCoinIDs = []

def getQuoteData(
        dbPath, 
        APIGroupCounts,
        validRecords,
        top1000StableCoins,
        testing
    ):

    # setup DB connection
    print('DB: {}'.format(dbPath))
    conn = sqlite3.connect(dbPath)
    c = conn.cursor()

    #   FOR EACH - API Group
    for k, v in APIGroupCounts.items(): 

        if v > 2: # more than 2 records to analyse for this 

            print('Qualifying API Group ID: {}   Count: {} - fetching from DB...'.format(k, v))

            # GET ALL date quotes for this currency WITH IN this API Group.
            #   FOR EACH - API Group
            #       FOR EACH - API Datetime
            for validRecordsKey, APIEntry in validRecords.items():

                if (APIEntry[0] == k): # if API Group ID's match in both validRecords and APIGroupCounts

                    # original: sql = 'SELECT id, symbol, price, volume_24h, volume_change_24h, percent_change_24h, percent_change_7d, percent_change_30d, market_cap, cmc_rank, num_market_pairs FROM quote WHERE insert_date BETWEEN \'{}\' AND \'{}\''.format((APIEntry[1] - timedelta(minutes=3)), (APIEntry[1] + timedelta(minutes=3)))
                    
                    topXCoins = 3
                    sql = 'SELECT id, symbol, price, volume_24h, volume_change_24h, percent_change_24h, percent_change_7d, percent_change_30d, market_cap, cmc_rank, num_market_pairs FROM quote WHERE id IN (select id from currency WHERE symbol NOT IN ('
                    for stableCoinSymbol in top1000StableCoins:
                        sql = sql + '\'{}\','.format(stableCoinSymbol)
                    sql = sql[:-1] + ') order by cmc_rank limit {}) AND insert_date BETWEEN \'{}\' AND \'{}\''.format(topXCoins, (APIEntry[1] - timedelta(minutes=3)), (APIEntry[1] + timedelta(minutes=3)))

                    if testing: # only 3 coins if testing
                        topXCoins = 2
                        sql = 'SELECT id, symbol, price, volume_24h, volume_change_24h, percent_change_24h, percent_change_7d, percent_change_30d, market_cap, cmc_rank, num_market_pairs FROM quote WHERE id IN (select id from currency WHERE symbol NOT IN ('
                        for stableCoinSymbol in top1000StableCoins:
                            sql = sql + '\'{}\','.format(stableCoinSymbol)
                        sql = sql[:-1] + ') order by cmc_rank limit {}) AND insert_date BETWEEN \'{}\' AND \'{}\''.format(topXCoins, (APIEntry[1] - timedelta(minutes=3)), (APIEntry[1] + timedelta(minutes=3)))
                        # OLD (no stables coins removed) sql = 'SELECT id, symbol, price, volume_24h, volume_change_24h, percent_change_24h, percent_change_7d, percent_change_30d, market_cap, cmc_rank, num_market_pairs FROM quote WHERE id IN (select id from currency order by cmc_rank limit {}) AND insert_date BETWEEN \'{}\' AND \'{}\''.format(topXCoinsTesting, (APIEntry[1] - timedelta(minutes=3)), (APIEntry[1] + timedelta(minutes=3)))
                        
                        # 3 coins
                        # sql = 'SELECT id, symbol, price, volume_24h, volume_change_24h, percent_change_24h, percent_change_7d, percent_change_30d, market_cap, cmc_rank, num_market_pairs FROM quote WHERE insert_date BETWEEN \'{}\' AND \'{}\' AND id IN (1, 1027, 825)'.format((APIEntry[1] - timedelta(minutes=3)), (APIEntry[1] + timedelta(minutes=3)))
                        
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

                        # collect a distinct list of all coin ID's for later

                        if coinRecord[0] not in distinctCoinIDs:

                            distinctCoinIDs.append(coinRecord[0])

    return SQLResults, distinctCoinIDs