#
#   connects to CoinMarketCap API and returns quotes requested
#       IF in OFFLINE mode, then we need to return an example Quote
#
#   Parameters:
#       mode - which mode or environment are we using?
#           production, sandbox, offline
#       maxCmcRank - what is the limit of quotes we want returned.
#           IF this is greater than 5000, then we need to make multiple API calls
#
#   Returns:
#       data - A dictionary of the API response
#           Keys:
#               status
#               data
#           Example: see the sampleData.json file

import log
import json
import config
from requests import Request, Session
# from requests.exceptions import ConnectionError, Timeout, TooManyRedirects



def getQuotes(mode, maxCmcRank):

    parameters = {
        'start':'1', # 1 is default so I don't believe this is needed. (where do you want to start in the returned list)
        'limit':str(maxCmcRank), # how many currencies do you want returned. (max is 5000)
        'convert':'USD' # comma separated list of what currency bases you'd like these returned in. ('USD,CAD,JPY,')
    }

    # determine the environment
    if (mode == 'production'):

        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        keyLocation = '{}/CMCApiKey.txt'.format(config.absolutePath)
        try:
            with open(keyLocation) as f:
                key = f.read()
        except:
            log.log('ERROR: Error reading CMC Api Key from file. Does the API Key file exist and is in the correct place?',1)
            exit()

    elif (mode == 'sandbox'):

        url = 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        key = 'b54bcf4d-1bca-4e8e-9a24-22ff2c3d462c'

    if (mode == 'offline'):

        try:
            f = open('{}/sampleData.json'.format(config.absolutePath))
            data = json.load(f)
        except Exception as e:
            log.log('FATAL ERROR reading or loading json file for offline mode: {}'.format(e))
            exit()

        # TODO later on, we might want to replace dates in this data with current datetimes
        # Also, will want to replace the contents of the sampleData.json with a real API response instead of from Sandbox

    else:

        # environment established, NOT offline mode, connect to API.

        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': key
            }
        
        session = Session()
        session.headers.update(headers)

        try:
            log.log('Attempting to connect to the API...',1)
            response = session.get(url, params=parameters)
            data = json.loads(response.text)

        except Exception as e:
            log.log('FATAL ERROR attempting to connect to the API. Check the log for a detailed error message.', 1)
            log.log('{}'.format(e))
            exit()

    return data



