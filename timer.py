# timer that should always run, and determine when to execute the run program
print('beginning timer...')

import log
import db
from datetime import datetime

log.check_log_path(False) # If log path doesn't exist, then create it.
l = 'TIMER: ' # setting log prefix for this file (timer.py)
log.log(l + '--- STARTING NEW TIMER SESSION ---')

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
    latest_insert_date = datetime.strptime(latest_insert_date_list[0][0], '%Y-%m-%d %H:%M:%S.%f')
    # print(type(latest_insert_date))
    s = 'The latest insert of quote data was on {}'.format(latest_insert_date)
    print(s)
    
    # TODO logging


else:
    s = 'There has never been a successful insert into this database. Running first API call now.'
    print(s)

    # TODO logging