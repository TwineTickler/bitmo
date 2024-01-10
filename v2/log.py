# logging for run.py (v2)
#
#   What parameters would we like to use?
#
#       message:
#           the message you'd like printed to the log file
#
#       prnt: bit 0 or 1
#           If prnt is 0, then do not print to console.
#           If prnt is 1, then print the message to console as well.
#
#       t (type): 0 or 1
#           0 - default (info)
#           1 - warning
#
#

import os
import config
from datetime import datetime

def log(message,prnt=0,t=0):

    # determine which file to use. If current log file exists then use it, if not, then create one.
    fileName = config.logPath + str(datetime.today().strftime('%Y-%m-%d')) + '.txt'

    if (t == 1):
        message = 'WARNING: {}'.format(message)

    if (prnt == 1):
        print(message)

    # if we use the 'a' mode then it shouldn't matter if the file exists or not, if it does not, it will create it.
    try:
        f = open(fileName, 'a') # create or open the current file
        f.write(str(datetime.now()) + ' --- ' + message + '\n') # write the log message + a new line
        f.close()
    except:
        print('ERROR: Error writing the message to log. Please Investigate. Original Message: {}'.format(message))

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