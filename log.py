# used by run.py for logging
#
# import all needed files

import config
import os
from datetime import datetime

# set global variables
full_log_path = config.absolute_path + config.log_path



# if Log path does not exist, then create it.
def check_log_path(caller_is_run=True):

    if (caller_is_run): # caller is run.py

        if (not os.path.exists(full_log_path)):
            # path missing, (can't log it because we don't have a log folder yet)
            # create it
            os.mkdir(full_log_path)
            # beginning a new session
            log('     -----     BEGINNING NEW SESSION     -----')
            # path created. log it
            log('log path created')

        else:
            # beginning a new session
            log('     -----     BEGINNING NEW SESSION     -----')
            # log that path already exists
            log('log path already exists')

    else: # being called by timer.py
       
        if (not os.path.exists(full_log_path)): # if the path doesn't exist then create it.
            os.mkdir(full_log_path)
            log('TIMER: log path created')



def log(message):
    # determine which file to use. If current log file exists then use it, if not, then create one.
    current_file_name = full_log_path + str(datetime.today().strftime('%Y-%m-%d')) + '.txt'
    # if we use the 'a' mode then it shouldn't matter if the file exists or not, if it does not, it will create it.
    try:
        f = open(current_file_name, 'a') # create or open the current file
        f.write(str(datetime.now()) + ' --- ' + message + '\n') # write the log message + a new line
        f.close()
    except:
        print('ERROR: Error writing to log. Please Investigate.')