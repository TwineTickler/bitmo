# gets:
#        - quote data from coin market cap API
#
# parameters:
#        - start
#             Same as the parameter['start'] set in config file.
#             This should be different each time through the loop (if using the loop)
#
# returns:
#        - data['status']['credit_count']
#             number of credits it took to complete the request (from the API)
#             we want to know when it reaches 0, because that is when there are no more currencies to save

import config
import log
import db
import json
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

def get_quote(start):

    # Verify Database is connected and setup:
    conn = db.open_db_connection() # open db connection
    db.create_tables(conn) # insure tables are created if not already

    # set variables from config file:
    url = config.cmc_environment['url']
    APIkey = config.cmc_environment['APIkey']
    parameters = config.parameters
    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': APIkey,
    }

    parameters['start'] = start # override start parameter with what is sent via the loop.

    session = Session()
    session.headers.update(headers)

    # Connect to the Coin Market Cap API
    log.log('connecting to Coin Market Cap using the ' + config.cmc_environment['environment'] + ' environment')

    try:
        response = session.get(url, params=parameters)
        log.log('Successful connection to CMC API')
        data = json.loads(response.text)
        log.log(str(data['status']))

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        log.log(str(e))
        print(e)
        s = 'ERROR: Error connecting to CMC API. Aborting program.'
        log.log(s)
        print(s)
        exit() # end the program here.

    # save data to the database
    db.insert_response_status(conn, data['status']) # store response status

    # if Error code in the status is anything but 0 then we have an error from API. Quit the program and throw the error.
    if (not data['status']['error_code'] == 0):
        s = 'ERROR: Error code received from API: {}: {}. Terminating the program.'.format(data['status']['error_code'], data['status']['error_message'])
        log.log(s)
        print(s)
        exit()

    # store currency info
    currency_count = str(len(data['data']))
    s = 'saving ' + currency_count + ' currency entries'
    log.log(s)
    print(s)
    error_occurred = False
    for c in data['data']:
        success = db.save_currency(conn, c) # success used to track if an error occurred during save.
        if (not success):
            error_occurred = True
    if (error_occurred):
        s = 'ERROR: one or more errors occurred during saving to currency table, please check the log for details'
        log.log(s)
        print(s)
    else:
        s = 'saving to currency table completed successfully'
        log.log(s)
        print(s)

    # by now we should have a currency added for each quote. Store the quote info.
    # TODO: fix this little bug later on next line
    s = 'saving {} quotes'.format(currency_count) # this is actually incorrect if using more than one quote per currency call. EX: convert: USD, CAD
    log.log(s)
    print(s)
    error_occurred = False

    for q in data['data']:
        success = db.save_quote(conn, q) # success used to track if an error occurred during save.
        if (not success):
            error_occurred = True

    if (error_occurred):
        s = 'ERROR: one or more errors occurred during saving to quote table, please check the log for details'
        log.log(s)
        print(s)

    else:
        s = 'saving to quote table completed successfully'
        log.log(s)
        print(s)

    db.close_db_connection(conn) # close db connection

    # all the other errors should have already been handled at this point.
    # so we should return a valid integer here.
    return data['status']['credit_count']