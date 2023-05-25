# Execute this command to run the program
print('Beginning Program...')

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
  'start':'1', # 1 is default so I don't believe this is needed.
  'limit':'180',
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
    exit() # end the program here.

# the following is only used for troubleshooting:
# print(data['status'])
# print(data['data'])
# print('number of currencies is: ' + str(len(data['data'])) + '\n')
# print(str(data['data'][0]) + '\n')
# print(str(data['data'][1]) + '\n')
# print(str(data['data'][2]) + '\n')
# print(str(data['data'][3]) + '\n')
# print(str(data['data'][4]) + '\n')
# print(str(data['data'][5]))

# save data to the database
conn = db.open_db_connection() # open db connection
db.create_tables(conn) # insure tables are created if not already
db.insert_response_status(conn, data['status']) # store response status
# store currency info TODO

currency_count = str(len(data['data']))
log.log('storing ' + currency_count + ' currency entries')
print('storing ' + currency_count + ' currency entries')
error_occurred = False
for c in data['data']:
    # print(str(c) + '\n')
    success = db.save_currency(conn, c)
    if (not success):
        error_occurred = True
if (error_occurred):
    s = 'one or more errors occurred during saving to currency table, please check the log for details'
    log.log(s)
    print(s)
# TODO: store quote info

db.close_db_connection(conn) # close db connection

# End program
log.log('Program Complete')

