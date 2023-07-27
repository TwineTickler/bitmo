# logging for run.py (v2)

import os
import config
from datetime import datetime

def log(message):
    # determine which file to use. If current log file exists then use it, if not, then create one.
    fileName = config.logPath + str(datetime.today().strftime('%Y-%m-%d')) + '.txt'
    # if we use the 'a' mode then it shouldn't matter if the file exists or not, if it does not, it will create it.
    try:
        f = open(fileName, 'a') # create or open the current file
        f.write(str(datetime.now()) + ' --- ' + message + '\n') # write the log message + a new line
        f.close()
    except:
        print('ERROR: Error writing the message - {} - to log. Please Investigate.'.format(message))

# if Log path does not exist, then create it.
# returns True if path already exists OR it successfully created the path.
# returns False if there was an error.
def checkLogPath(path):

    if (not os.path.exists(path)):
        # path missing, (can't log it because we don't have a log folder yet)
        # create it
        try:
            os.mkdir(path)
            log('     -----     BEGINNING NEW SESSION     -----')
            log('new log path created')

        except:
            return False

    else:
        # beginning a new session
        log('     -----     BEGINNING NEW SESSION     -----')
        # log that path already exists
        log('log path already exists')

    return True