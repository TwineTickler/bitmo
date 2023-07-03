# Purpose of this file is to connect to the database and reveal any currency trends
#
# This is the first "reporting" functionality of the program.
# This file will essentially be different from all the others as it will work independently.
# It essentially can be manually ran at any point in time
#
# We would like two things:
#   1. a report based on the number of days you'd like to analyze trends, for all historical data
#   2. a up-to-date report that gives you suggestions on what to trade NOW

# I don't think we need the same type of logging set up for this file because this can be run anytime, separately from all the other functionality.

# first trend I'd like to check are upward trends
# defined as:
# 
# quote table entities:
# - price
#      - continues to increase in value
# - percent_change_24h
#      - I would expect this to also be positive, following the price values


# First we need to find valid currencies to analyze against
# They should have the following:
# at least 3 entries with 3 days, but possibly more.
# What is concidered a valid day?
#
# There will be at least 3 days.
# There will be a day 1:
#    - day 1 does not have a valid day preceeding it.
# There will be an X number of middle days
#    - middle days must have a valid day before and after it.
# There will be an end day:
#    - end day will not have any valid day after it.

# for days to qualify or be considered to be before or after another, they need to be within 24 hours + 8 hours before or after.
# This gives leway for when times are slightly off, or when running the program ran into problems, and was delayed.

# First thing we will need to do is establish our valid days.

# get all the successful inserts in order by date.


####################################################################################################
#
#                           Setup global variables and functions
#
####################################################################################################


import config
import sqlite3
from datetime import datetime

db_prefix = 'bitmo-01'
db = config.absolute_path + config.db_path + db_prefix

def open_db_connection():

    # Connect to the database
    print('database is: {}'.format(db))

    try:
        conn = sqlite3.connect(db)
        print('connected')

    except:
        print('Fatal ERROR: Error connecting to database')
        exit() # quit the program if we cannot connect to the database

    return conn


def close_db_connection(conn):
    # close the connection to the database
    try:
        conn.close()
        print('closed connection to database')

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

def sort_response_status_groups_by_insert_date(element): # this is no longer needed because we are just using the sort within SQL

    return datetime.strptime(element[7], '%Y-%m-%d %H:%M:%S.%f')

# if we'd like to use later, this is how we call it:
# result.sort(key=sort_response_status_groups_by_insert_date) # this will sort the results by 


####################################################################################################
#
#                           Begin fuctionality
#
####################################################################################################


analyze_environment = 0

# determine which database to analyze
while not (analyze_environment == 1 or analyze_environment == 2):

    print('value of input is: {}'.format(analyze_environment))

    print('Choose your environment. Enter a number:' + '\n' + 
        '1: Production' + '\n' +
        '2: Sandbox')

    analyze_environment = input()

    try:
        analyze_environment = int(analyze_environment)
    except:
        pass

# finish created db path
if analyze_environment == 1:
    db = db + '-prod.db'
elif analyze_environment == 2:
    db = db + '-sandbox.db'
else:
    print('Error setting up DB path')
    exit()


sql = '''
    SELECT * FROM response_status
	    WHERE credit_count != 0
		    ORDER BY insert_date
'''
# Example result:
# [ ('2023-06-18T02:53:56.351Z', 0, None, 61, 25, '/v1/cryptocurrency/listings/latest', '2023-06-17 21:53:57.105953', 10399), (...) ]

conn = open_db_connection()
result = query_db(conn, sql) # both opens and closes the connection within this call

# create a dict to store the Response Status's and Group them.
response_status_groups = {}

# Keys:
#     Group ID's
#
# Values:
#     [AVG datetime, [datetime1, datetime2, datetime3, etc]]
#     insert datetime1, 2, 3, etc...
#            NOT SURE IF WE NEED THIS YET --> Order: F (first in group), L (last in group), null (anything else)
#     AVG: average datetime of insert (middle)

print(result)

last_row_datetime = 0
current_group_id = 1

for row in result:
    print(row)
    print(row[7])
    print(type(row[7]))

    # these rows will be in order from latest to ealiest



    last_row_datetime = convert_str_to_datetime(row[7])

    # appending the dictionary
    response_status_groups[current_group_id] = 
