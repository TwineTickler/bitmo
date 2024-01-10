# config file for v2

import pathlib

absolutePath = str(pathlib.Path(__file__).parent.resolve()) # this is wherever THIS file is.
logPath = absolutePath + '/logs/'
dbPath = absolutePath + '/db/'