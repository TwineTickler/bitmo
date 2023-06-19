# timer that should always run, and determine when to execute the run program
print('beginning timer...')

import log
import db
import pandas as pd
import time
from datetime import datetime
from datetime import timedelta

target_run_time = 21 # should be an integer from 0 - 23 representing the hour at which you'd like to run the API call.

log.check_log_path(False) # If log path doesn't exist, then create it.
l = 'TIMER: ' # setting log prefix for this file (timer.py)
log.log(l + '--- STARTING NEW TIMER SESSION ---')

if (not (0 <= target_run_time <= 23)):
    s = 'target_run_time variable NOT setup correctly. Stopping program.'
    log.log(l + s)
    print(s)
    exit()

##############################################   Define Functions  #############################################


def run_API_program():
    # Runs the main API get_quote program.
    # Returns the current Datetime
    # always call this while assigning to the latest_insert_date variable because we need that variable to always be updated to the most recent date.

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


def get_datetime_of_next_API_call():

    # uses the target_run_time and the time_since_last_run_hours to determine when should be the next API call.
    # returns the datetime of next API call.
    # should only be called whenever the hours are less than 24.
    # hours that qualify:
    #   23
    #   22
    #   21
    #   ...
    #   2
    #   1
    #   0

    log.log(l + 'getting datetime of next API call...')

    hours_until_next_API_call = 23 - time_since_last_run_hours
    log.log(l + 'hours until next API call = ' + str(hours_until_next_API_call))
    run_now = False

    # if it's 23 hours since last run time, then run now UNLESS the current time is 1 hour before the desired target time.
    # if that is the case then run it at the target_run_time (in 1 hour)

    if (hours_until_next_API_call == 0):

        # if current hour is 1 hour before the desired target time.
        # now_hr + 1_hr = target_hour then run at target time.
        now_plus_1hour = (datetime.now() + timedelta(hours=1))

        if (now_plus_1hour.hour == target_run_time):

            log.log(l + 'now + 1hr = {}'.format(now_plus_1hour.hour))
            log.log(l + 'target_run_time: {}'.format(target_run_time))

            # run at target_time
            return_datetime = now_plus_1hour.replace(minute=0, second=0, microsecond=0)
            # return_datetime = datetime.now().replace(hour=target_run_time, minute=0, second=0, microsecond=0)

        else:

            # run now
            run_now = True
            return_datetime = 0

    else:

        # set API call time based off 23 hours from last run.
        # create a datetime that is based off the rounded hours, and then add 23 hours to it.
        
        time_of_last_run_rounded = pd.Timestamp(latest_insert_date).round(freq='H')
        log.log(l + 'time of last run rounded: ' + str(time_of_last_run_rounded))
        
        target_datetime = time_of_last_run_rounded + pd.Timedelta(hours=23)
        log.log(l + 'time of last run, +23 hours (new target): {}'.format(target_datetime))

        return_datetime = target_datetime.to_pydatetime()

    return run_now, return_datetime


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

# print('latest_insert_date: ' + str(latest_insert_date))
time_since_last_run = (datetime.now() - latest_insert_date)
s = 'It has been -   {}   - since the last API call'.format(format_timedelta(time_since_last_run))
log.log(l + s)
print(s)

# get the hours, rounded to nearest. (eaiest way was to use a pandas timedelta)
# explaination: sending timedelta to a pandas timedelta, then rounding on the hour, then getting total seconds, dividing by 3600 and converting to an int.
time_since_last_run_hours = (int((pd.Timedelta(time_since_last_run).round(freq='H')).total_seconds() / 3600))
log.log(l + 'time since last run in rounded hours: ' + str(time_since_last_run_hours))

# determine the next time to run an API call.
if (time_since_last_run_hours >= 24):

    # run the API call now
    latest_insert_date = run_API_program()

else:

    runnow, next_API_runtime = get_datetime_of_next_API_call()
    #print('runnow: ' + str(runnow))
    #print('next API runtime: ' + str(next_API_runtime))
    
    if (runnow):

        # run the API call now
        s = 'runnow is True. Running API call now.'
        log.log(l + s)
        print(s)
        latest_insert_date = run_API_program()
    
    else:

        # target runtime established...
        # loop the timer, until it's time to run...
        s = 'next API runtime set: {}'.format(next_API_runtime)
        log.log(l + s)
        print(s)

        continue_loop = True

        while continue_loop:
            
            #TODO
            # add 15 minute check intervals.

            #TODO
            # debug why it ran last night and stopped after 4 days of not running

            # print('sleeping for 5 minutes...')
            s = 'time is: {} - Next API call is at: {} - T minus {}'.format(datetime.now().strftime('%H:%M:%S'), next_API_runtime.strftime('%H:%M:%S'), (next_API_runtime - datetime.now()))
            log.log(l + s)
            print(s)
            time.sleep(5)

            # check if now is the correct hour to run the program.
            if (next_API_runtime.hour == datetime.now().hour):
                
                # now is the target runtime. Run the program
                s = 'target runtime is NOW. Running API call...'
                log.log(l + s)
                print(s)
                latest_insert_date = run_API_program()

                # get the runtime of next API call
                s = 'next API runtime set: {}'.format(next_API_runtime)
                log.log(l + s)
                print(s)
                runnow, next_API_runtime = get_datetime_of_next_API_call()


'''
When to run an API call?

based off 3 things:
    Target Time - currently 9:00 PM
    Current Time
    Time Since Last Call

If hour is:

    less than 24:
        If current hour is 9:00 PM -> then at 9:00 PM
        If current hour is NOT 9:00 PM -> then at hour 23

        Ex:
            Time Since: 6 hours (rounded)
                Current Time: 4:00 PM
                    Last run: 10:00 AM
                    Next run: + 23 hours since last run = 9:00 AM
                    Next +1 run: + 23 hours since last run = 8:00 AM ... etc...

                Current Time: 11:00 PM
                    Last run: 5:00 PM
                    Next run: 4:00 PM + 23 hours
                    Next +1 run: 3:00 PM + 23 hours... etc...

                Current Time: 9:00 PM
                    Last run: 3:00 PM
                    Next run: 2:00 PM + 23 hours... etc...

            Time Since: 23 hours
                Current Time: 4:00 PM
                    last run: 5:00 PM
                    next run: NOW + 23 hours
                    next run +1: 3:00 PM + 23 hours... etc...

                Current Time: 11:00 PM
                    last run: 12:00 AM
                    next run: NOW + 23 hours
                    next run +1: 10:00 PM + 23 hours... etc...

                Current Time: 9:00 PM
                    last run: 10:00 PM
                    next run: NOW <-- run is 9:00 PM + 23 hours
                    next run: +1: 9:00 PM + 24 hours
                    next run: +2: 9:00 PM + 24 hours

            Time Since: 0 hours (less than 30 minutes)
                Current Time: 4:00 PM
                    last run: 4:00 PM
                    next run: 3:00 PM + 23 hours

                Current Time: 11:00 PM
                    last run: 11:00 PM
                    next run: 10:00 PM + 23 hours

                Current Time: 9:00 PM
                    last run: 9:00 PM
                    next run: 9:00 PM + 24 hours

    equal to or greater than 24:
        Run now


'''