# global settings used by the app
# you will need to add a text file named 'CMCApiKey.txt' to the root folder that contains your production API Key

# import all necessary libraries and files

import pathlib

# everything will be based of this parent path:
absolute_path = str(pathlib.Path(__file__).parent.resolve()) # this is wherever THIS file is.

# relative paths
log_path = '/logs/'
db_path = '/db/'

# files
db_prefix = 'bitmo-01'
API_key_file_name = '/' + 'CMCApiKey.txt'

# Coin Market Cap API Environment (comment out the one you do not want and the rest of the script will set the correct values)
environment = 'sandbox'
#environment = 'production'

# make only 1 call to the API to get 1 set of data or loop through all the records to get EACH currency
# 0 = just once (some)
# 1 = ALL
all_or_some = 1

parameters = {
  'start':'1', # 1 is default so I don't believe this is needed.
  'limit':'5000', # how many currencies do you want returned. (max is 5000)
  'convert':'USD' # comma separated list of what currency bases you'd like these returned in. ('USD,CAD,JPY,')
}

if (environment == 'sandbox'):
    db_name = db_prefix + '-sandbox.db'
    cmc_environment = {
        'environment': environment,
        'url': 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest',
        'APIkey': 'b54bcf4d-1bca-4e8e-9a24-22ff2c3d462c'
    }
elif (environment == 'production'):
    db_name = db_prefix + '-prod.db'
    # get the API key from the file
    key_location = absolute_path + API_key_file_name
    try:
        with open(key_location) as f:
            production_API_key = f.read()
    except:
        print('ERROR: Error reading CMC Api Key from file. Does the API Key file exist and is in the correct place?')
        exit() # exit the program if we cannot read the API key.
    cmc_environment = {
        'environment': environment,
        'url': 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest',
        'APIkey': production_API_key
    }