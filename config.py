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
db_name = 'bitmo-03.db'
API_key_file_name = '/' + 'CMCApiKey.txt'

# Coin Market Cap API Environment (comment out the one you do not want and the rest of the script will set the correct values)
environment = 'sandbox'
# environment = 'production'

if (environment == 'sandbox'):
    cmc_environment = {
        'environment': environment,
        'url': 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest',
        'APIkey': 'b54bcf4d-1bca-4e8e-9a24-22ff2c3d462c'
    }
elif (environment == 'production'):
    # get the API key from the file
    key_location = absolute_path + API_key_file_name
    try:
        with open(key_location) as f:
            production_API_key = f.read()
    except:
        print('error reading CMC Api Key from file. Does the API Key file exist and is in the correct place?')
        production_API_key = '0'
    cmc_environment = {
        'environment': environment,
        'url': 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest',
        'APIkey': production_API_key
    }