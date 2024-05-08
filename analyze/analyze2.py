#
#   analyze.py took into consideration consecutive days only.
#
#   This analyze file is going to take a look and analyze the following:
#       1. a number of consecutive days.
#           a. I'd like to leave this up to the program.
#           b. so if we have x amount of days in a row, it will analyze each case.
#           c. for example: consecutive days are: day 1, 2, 3, 4, 5 - 7, 8, 9 - 12, 13, 14, 15, 16, 17, 18
#           d. then I'd like it to look at everything that is consecutive and fits into our criteria such as:
#           e. say we set the positive day threshold to 70% - this would mean that within a given set of consecutive days
#               the currency would have to have a positive change for 70% of the days.
#       2. 


#   User Defined Variables:
#       positiveDayThreshold = 70% is default
#       minIncreaseThreshold = 0% is default (but might want to move this up to at least 0.5% or whatever)
#       minRankThreshold = 0 is default (but can be set to say 200, which would then only include currencies listed in the cmc_rank top 200)
#       minMarketPairs = 0 is default (this might be more desirable to use than filtering by Rank)


####################################################################################################
#
#                           Setup global variables and functions
#
####################################################################################################


import config
import sqlite3
from datetime import datetime
from datetime import timedelta

db_prefix = 'bitmo-01'
db = config.absolute_path + config.db_path + config.db_name
responseStatusGroupingThreshold = (60 * 10) # 10 minutes --> in seconds (typically only around 17 - 35 seconds or so apart, depending on which computer is processing them)
consecutiveDayThreshold = (24 + 8) # in hours --> should be 1 day roughly, but giving 8 hours of buffer
positiveDayThreshold = 70
minIncreaseThreshold = 0
minRankThreshold = 0
minMarketPairs = 0
coin_blacklist = {18513} # a set of coins I am never interesting in trading.


def open_db_connection():

    # Connect to the database
    # print('database is: {}'.format(db))

    try:
        conn = sqlite3.connect(db)
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

print('using this db: {}'.format(db))