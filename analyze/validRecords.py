# 
#
#
#    a function that returns valid database records that can be used for analysis
#
#
#    Receives:
#
#        dbPath string - required
#        nextDownloadMinTime integer (seconds) - default 28800 (8 hours)
#        nextDownloadMaxTime integer (seconds) - default 28800 (8 hours)
#        apiDownloadTimeWindow integer (seconds) - default 300 (5 minutes)
#
#
#    Returns:
#
#        dictionary containing valid datetimes for analysis
#             results{}
#                  keys = 1, 2, 3, 4, etc... (group IDs)
#                  values (tuple) = (seriesNumber, 'response_status.insert_date')
#                       value is a tuple with the first value representing the number of the series and the second the earliest insertdate in the API group
#
#    Assumptions:
#
#        one valid download request should be within:
#            + 5 minutes of the lowest response_status.insert_date value for any given API download.
#
#    Check:
#
#        Next API call must be +/- 8 hours of the next expected API call (+24 hours)
#
#   Notes:
#
#   Each valid API response will be a member of a group of API responses.
#   Each group member must adhere to the requirements of the timeframe in between API responses to be 
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
#
#
#####################################################################################################################


def findValidRecords(
        dbPath,
        nextDownloadMinTime=28800,
        nextDownloadMaxTime=28800,
        apiDownloadTimeWindow=300
    ):

    import sqlite3
    # import config
    from datetime import datetime
    from datetime import timedelta

    def open_db_connection():
        # Connect to the database    print('database is: {}'.format(db))
        try:
            conn = sqlite3.connect(dbPath)
            # print('connected')

        except:
            print('Fatal ERROR: Error connecting to database')
            exit() # quit the program if we cannot connect to the database

        return conn
    
    def close_db_connection(conn):
        # close the connection to the database
        try:
            conn.close()
            # print('closed connection to database')

        except:
            print('ERROR: Error closing connection to database')

    def query_db(conn, sql):

        c = conn.cursor()

        try:
            c.execute(sql)
            response = c.fetchall()
            close_db_connection(conn)

        except Exception as e:
            print(e)
            exit()

        return response
    
    def convert_str_to_datetime(str): # takes a string (typically a datetime inserted by the run.py program) and converts it to a datetime object

        new_datetime = datetime.strptime(str, '%Y-%m-%d %H:%M:%S.%f')

        return new_datetime

    ####################################################################################################
    #
    #                           Begin fuctionality
    #
    ####################################################################################################

    # find the earliest valid API call
    sql = '''
        select insert_date from response_status rs 
            where 1=1
                and error_code = 0
                and error_message IS NULL
                and credit_count > 0
                    order by insert_date 
                        limit 1
    '''

    conn = open_db_connection()
    earliestValidRecord = query_db(conn, sql)

    if (len(earliestValidRecord) == 0):
        print('Earliest Valid Record cound not be found.')
        exit()

    # print('first valid record: {}'.format(convert_str_to_datetime(earliestValidRecord[0][0])))

    results = {1: (1, convert_str_to_datetime(earliestValidRecord[0][0]))}

    # find the next valid API record (the next API download after the apiDownloadTimeWindow)
    # if it falls between the nextDownloadMinTime and nextDownloadMaxTime (+24 hours) then it will be our next valid record.
    # if it does not:
    #     If it is Less Than:
    #         Check to see if there is another entry that falls within the desired time window.
    #             If so -> skip over this one, and use the valid one, and continue normally.
    #             If not -> use this entry as the beginning of a new series, and continue normally.
    #
    #     If it is Greater Than:
    #         Use this entry as the beginning of a new series and continue normally.

    seriesID = 1
    keyID = 1
    nextPotentialValidRecord = [1] # initialize this variable so that we will begin the loop
    
    while (len(nextPotentialValidRecord) > 0):

        apiDownloadWindowMaxTime = results[keyID][1] + timedelta(seconds=apiDownloadTimeWindow)
        nextAPIDownloadWindowMin = (results[keyID][1] + timedelta(seconds=86400)) - timedelta(seconds=nextDownloadMinTime)
        nextAPIDownloadWindowMax = (results[keyID][1] + timedelta(seconds=86400)) + timedelta(seconds=nextDownloadMaxTime)
        keyID = keyID + 1

        sql = '''
            select insert_date from response_status rs 
                where 1=1
                    and error_code = 0
                    and error_message IS NULL
                    and credit_count > 0
                    and insert_date > '{}'
                        order by insert_date 
                            limit 1
        '''.format(apiDownloadWindowMaxTime)

        conn = open_db_connection()
        nextPotentialValidRecord = query_db(conn, sql)

        # verify at least one more entry has been found (if not then we have reached the end of the entries)
        if (len(nextPotentialValidRecord) != 0):

            nextPotentialValidRecordDateTime = convert_str_to_datetime(nextPotentialValidRecord[0][0])

            # print('next Potential Valid Record: {}'.format(nextPotentialValidRecordDateTime))
            # print('next API Window Min: {} next API Window Max: {}'.format(nextAPIDownloadWindowMin, nextAPIDownloadWindowMax))

            # does this next API download qualify as part of this series?
            if (nextAPIDownloadWindowMax > nextPotentialValidRecordDateTime > nextAPIDownloadWindowMin):
                # yes

                results[keyID] = (seriesID, nextPotentialValidRecordDateTime)

            else:
                # no
                # is it less than or greater than the nextAPIDownloadWindow?

                if (nextPotentialValidRecordDateTime < nextAPIDownloadWindowMin):
                    # less than
                    # print('less than')

                    # IS there another valid entry that falls Within the nextAPIDownloadWindow?
                    sql = '''
                        select insert_date from response_status rs 
                            where 1=1
                                and error_code = 0
                                and error_message IS NULL
                                and credit_count > 0
                                and insert_date BETWEEN '{}' AND '{}'
                                    order by insert_date 
                                        limit 1
                    '''.format(nextAPIDownloadWindowMin, nextAPIDownloadWindowMax)

                    conn = open_db_connection()
                    nextValidRecord = query_db(conn, sql)

                    if (len(nextValidRecord) != 0):
                        # yes, there is a valid record that falls in between. Use this one (ignore the other) and then continue normally.
                        nextValidRecord = convert_str_to_datetime(nextValidRecord[0][0])

                        # print('NEW next Valid Record: {}'.format(nextValidRecord))

                        results[keyID] = (seriesID, nextValidRecord)

                    else:
                        # no, there is no valid record in between
                        # use this record as the beginning of a NEW series and continue normally.

                        # print('Confirmed Potential Valid Record: {}').format(nextPotentialValidRecordDateTime)

                        seriesID = seriesID + 1
                        results[keyID] = (seriesID, nextPotentialValidRecordDateTime)

                else:
                    # greater than
                    # add this record as the beginning of the next series.
                    # print('greater than')

                    seriesID = seriesID + 1
                    results[keyID] = (seriesID, nextPotentialValidRecordDateTime)

    # for k, v in results.items():
    #     print('KEY: {} VALUE: {}'.format(k, v))

    return results