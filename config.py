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
db_name = 'bitmo-01.db'

# Coin Market Cap API Environment
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
    with open('CMCApiKey.txt') as f:
        production_API_key = f.read()
    cmc_environment = {
        'environment': environment,
        'url': 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest',
        'APIkey': production_API_key
    }