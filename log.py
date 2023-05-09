# used by run.py for logging
#
# import all needed files

import config
import os



# if Log path does not exist, then create it.
def check_log_path():
    full_log_path =  config.absolute_path + config.log_path
    if (os.path.exists(full_log_path)):
        return True
    else:
        return False

