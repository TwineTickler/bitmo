# used by run.py for logging
#
# import all needed files

import config
import os
from datetime import datetime

# set global variables
full_log_path =  config.absolute_path + config.log_path

# if Log path does not exist, then create it.
def check_log_path():
    if (not os.path.exists(full_log_path)):
        # path missing, (can't log it because we don't have a log folder yet)
        # create it
        os.mkdir(full_log_path)
        # path created. log it
        log('log - log path created')
    else:
        # log that path already exists
        log('log - log path already exists')

def log(message):
    # determine which file to use.
    # if current log file exists then use it, if not, then create one.
    current_file_name = full_log_path + str(datetime.today().strftime('%Y-%m-%d')) + '.txt'
    if (os.path.isfile(current_file_name)):
        print('file exists')
    else:
        print('file does not exist')
