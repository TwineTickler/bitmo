# Execute this command to run the program

# import all the needed files

import config
import log
import sqlite3
import json
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

# 1. If log path doesn't exist, then create it.
log.check_log_path()

# 2. Connect to the database
database_path = config.absolute_path + config.db_path + config.db_name # build the path based off the config file
log.log('database is: ' + database_path)

try:
    conn = sqlite3.connect(database_path)
    log.log('connected to database')
except:
    log.log('Error connecting to database')
    print('Error connecting to database')

# close the connection to the database
try:
    conn.close()
    log.log('closed connection to database')
except:
    log.log('Error closing connection to database')

# 3. Connect to the Coin Market Cap API
log.log('connecting to Coin Market Cap using the ' + config.cmc_environment['environment'] + ' environment')

# set variables from config file:
url = config.cmc_environment['url']
APIkey = config.cmc_environment['APIkey']

parameters = {
  'start':'1',
  'limit':'5000',
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
    data = json.loads(response.text)
    log.log(str(data))
    print(data)
except (ConnectionError, Timeout, TooManyRedirects) as e:
    log.log(e)
    print(e)

# End program
log.log('Program Complete')

