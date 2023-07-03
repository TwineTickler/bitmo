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
from datetime import timedelta

db_prefix = 'bitmo-01'
db = config.absolute_path + config.db_path + db_prefix
response_status_grouping_threshold = (60 * 10) # 10 minutes --> in seconds (typically only around 17 - 35 seconds or so apart, depending on which computer is processing them)
consecutiveDayThreshold = (24 + 8) # in hours --> should be 1 day roughly, but giving 8 hours of buffer.
consecutiveDays = 5 # how many days would we like to report on?

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

# print(result)

previous_row_insert_date = 0
current_row_insert_date = 0
current_group_id = 1
current_group_insert_dates = []

for row in result:
    print(row)
    # print(row[7])
    # print(type(row[7]))

    # these rows will be in order from oldest to newest
    current_row_insert_date = convert_str_to_datetime(row[7])

    if previous_row_insert_date == 0:

        # this is the first entry of the list
        print('first row in the list')

    else:
        
        # we have a datetime from the previous row
        if (previous_row_insert_date + timedelta(seconds=response_status_grouping_threshold)) >= current_row_insert_date:

            # this insert date is within the response_status_grouping_threshold (10 mintutes) of the last insert date (because this loop will be executed in ascending order by insert_date)
            print('this is in the same group as the previous row')

        else:

            # this is the start of a new group
            # first build the previous group into the Dictionary
            # then begin building the next group ID
            # AND YES, we can actually make this code less lines, by using not's and getting rid of the two else's.. but I think it would be more confusing for a human to read and troubleshoot, so leaving it like this for now.
            # the first two if statements, essentially do nothing, it's just the else's we are using.

            # add the previous group to the dictionary:
            print('previous group is DONE, adding it to the dictionary...')
            # avgTime = datetime.strftime(datetime.fromtimestamp(sum(map(datetime.timestamp,current_group_insert_dates))/len(current_group_insert_dates)),"%H:%M:%S") # I just grabbed this from a post online. Seems to work.
            avgTime = datetime.fromtimestamp(sum(map(datetime.timestamp,current_group_insert_dates))/len(current_group_insert_dates))  # I just grabbed this from a post online. Seems to work.
            response_status_groups[current_group_id] = [avgTime,current_group_insert_dates] # TODO need to add the average to this.

            # reset to build the next group ID
            print('resettings variables and preparing for the next group ID...')
            current_group_id = current_group_id + 1
            current_group_insert_dates = []
            
    current_group_insert_dates.append(current_row_insert_date)
    previous_row_insert_date = current_row_insert_date

print('Dictionary complete\n')

for key, value in response_status_groups.items():
    print('key is: {}'.format(key))
    print('value is: {}'.format(value))



# Next build the Response Status Group Relationships
# this will tell us if any day has:
#     1. a valid day preceeding it.
#     2. a valid day following it.

# scratch that, just going to go straight to the Consecutive Group List

# build the Consecutive Group List.
# This will show us a groups of Group ID's that fall within the criteria of consecutive days
#     currently going to define a consecutive day of within the range of 1 day + 8 hours.

consecutiveGroups = []

for groupID, values in response_status_groups.items():

    print(groupID)
    currentGroupInsertDate = values[0]
    currentGroupID = groupID
    currentGroupIDs = [groupID]

    # we only want to execute the while loop IF there are enough days AFTER the current Group ID to check for. So:

    if (len(response_status_groups) - (consecutiveDays - 1)) >= groupID:

        # this will loop through each of the keys in the dictionary (groups/days)

        counter = 1

        while counter < consecutiveDays:
            
            # for this group ID, see if we have a consecutive group based off the consecutiveDays we are targeting (ie, 5 days in a row)
            # if so, create a tuple to add to the consecutive group list

            if (currentGroupInsertDate + timedelta(hours=consecutiveDayThreshold)) >= response_status_groups[(currentGroupID + 1)][0]:

                # this day's insert date is within the threshold from the previous day.
                
                counter = counter + 1
                currentGroupIDs.append(currentGroupID + 1)

                if counter == consecutiveDays:
                    
                    # all days passed, add the tuple to the list
                    consecutiveGroups.append(currentGroupIDs)

                else:
                    
                    # update the variables to check for the next day.
                    currentGroupID = currentGroupID + 1
                    currentGroupInsertDate = response_status_groups[currentGroupID][0]

            else:

                # one of the days failed, do not add the tuple to the list. End the while loop early.
                counter = consecutiveDays

print('Consecutive Groups Compiled\n\n')
for row in consecutiveGroups:
    print(row)
        