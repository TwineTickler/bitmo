# timer that should always run, and determine when to execute the run program
print('beginning timer...')

import log
import db
import pandas as pd
from datetime import datetime

log.check_log_path(False) # If log path doesn't exist, then create it.
l = 'TIMER: ' # setting log prefix for this file (timer.py)
log.log(l + '--- STARTING NEW TIMER SESSION ---')

##############################################   Define Functions  #############################################


def run_API_program():
    # Runs the main API get_quote program.
    # Returns the current Datetime

    with open('run.py') as f:
        exec(f.read())

    return datetime.now()


def format_timedelta(delta) -> str:
    """Formats a timedelta duration to [N days] %H:%M:%S format"""
    seconds = int(delta.total_seconds())

    secs_in_a_day = 86400
    secs_in_a_hour = 3600
    secs_in_a_min = 60

    days, seconds = divmod(seconds, secs_in_a_day)
    hours, seconds = divmod(seconds, secs_in_a_hour)
    minutes, seconds = divmod(seconds, secs_in_a_min)

    time_fmt = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    if days > 0:
        suffix = "s" if days > 1 else ""
        return f"{days} day{suffix} {time_fmt}"

    return time_fmt


############################################## Begin runtime logic #############################################

# get datetime right now
now = datetime.now()
s = 'start time is: {}'.format(now)
log.log(l + s)
print(s)

# get time of last database update
# Verify Database is connected and setup:
conn = db.open_db_connection(False) # open db connection (False is just used to tell logging that the call for this is coming from the timer.py, and not run.py)
db.create_tables(conn, False) # insure tables are created
latest_insert_date_list = db.get_latest_response_time(conn)

if (len(latest_insert_date_list) == 1): # we have a valid result from the SQL call

    # convert from list/tuple/string into datetime object
    log.log(l + 'found a valid date as last insert datetime, converting from string to datetime object...')
    latest_insert_date = datetime.strptime(latest_insert_date_list[0][0], '%Y-%m-%d %H:%M:%S.%f')

    # print(type(latest_insert_date))
    s = 'The latest insert of quote data was on {}'.format(latest_insert_date)
    log.log(l + s)
    print(s)

else:

    log.log(l + 'no valid last insert date found.')
    s = 'There has never been a successful insert into this database. Running first API call now.'
    log.log(l + s)
    print(s)

    # run the program
    latest_insert_date = run_API_program()

# by now we should have a last run datetime. (either just now or sometime)

# first need to determine how far away that run time was from now.

time_since_last_run = (datetime.now() - latest_insert_date)
s = 'It has been -   {}   - since the last API call'.format(format_timedelta(time_since_last_run))
log.log(l + s)
print(s)

# get the hours, rounded to nearest. (eaiest way was to use a pandas timedelta)
time_since_last_run_hours = (int((pd.Timedelta(time_since_last_run).round(freq='H')).total_seconds() / 3600))
log.log(l + 'time since last run in rounded hours: ' + str(time_since_last_run_hours))

#time_since_rounded_hour = get_rounded_hour(time_since_last_run)
#print('Time since with rounded hour: ' + str(time_since_rounded_hour))

# determine the next time to run an API call.

'''
When to run an API call?

based off 3 things:
    Target Time - currently 9:00 PM
    Current Time
    Time Since Last Call

If hour is:

    less than or equal to 24:
        If hour 24 is 9:00 PM -> then at 9:00 PM
        If hour 24 is anything else -> then at hour 25

        Ex:
            Time Since: 6 hours (rounded)
                Current Time: 4:00 PM

                Current Time: 11:00 PM

                Current TIme: 9:00 PM

            Time Since: 23 hours
                Current Time: 4:00 PM

                Current Time: 11:00 PM

                Current Time: 9:00 PM

            Time Since: 24 hours
                Current Time: 4:00 PM

                Current Time: 11:00 PM

                Current Time: 9:00 PM

            Time Since: 0 hours (less than 30 minutes)
                Current Time: 4:00 PM

                Current Time: 11:00 PM

                Current Time: 9:00 PM

    greater than 24:
        Run now

        Ex:
            Time Since: 25 hours (rounded)
                Current Time: 4:00 PM

                Current Time: 11:00 PM

                Current Time: 9:00 PM
            
            Time Since: 30 hours
                Current Time: 4:00 PM

                Current Time: 11:00 PM

                Current Time: 9:00 PM

            Time Since: 72 hours
                Current Time: 4:00 PM

                Current Time: 11:00 PM

                Current Time: 9:00 PM


'''