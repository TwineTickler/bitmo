# global settings used by the app

# import all necessary libraries and files

import pathlib

# everything will be based of this parent path:
absolute_path = str(pathlib.Path(__file__).parent.resolve()) # this is where THIS file is

# relative paths
log_path = '/logs/'
db_path = '/db/'

# files
db_name = 'test01.db'