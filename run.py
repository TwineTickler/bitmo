# Execute this command to run the program

# import all the needed files

import config
import log
import db
import json
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

# 1. If log path doesn't exist, then create it.
log.check_log_path()

# 3. Connect to the Coin Market Cap API
log.log('connecting to Coin Market Cap using the ' + config.cmc_environment['environment'] + ' environment')

# set variables from config file:
url = config.cmc_environment['url']
APIkey = config.cmc_environment['APIkey']

parameters = {
  'start':'1',
  'limit':'10',
  'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': APIkey,
}

session = Session()
session.headers.update(headers)

try:
    response = session.get(url, params=parameters)
    log.log('Successful connection to CMC API')
    data = json.loads(response.text)
    log.log(str(data['status']))
    # print(data)
except (ConnectionError, Timeout, TooManyRedirects) as e:
    log.log('Error connecting to CMC API')
    log.log(e)
    print(e)

# save the status response in it's own table

print(data['status'])
# print(data['data'])

# db.initiate_db('insert_status_response', data['status'])
db.open_db_connection()
db.close_db_connection()

# End program
log.log('Program Complete')

