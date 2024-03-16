# purpose of this is to check my database every night at 9:10 and verify Bitmo successfully ran.

import credentials
import pause, sqlite3, requests
from datetime import datetime as dt
from datetime import timedelta as td

# if current hour is less than 21 run for today, if not, run for tomorrow.

now = dt.now()
nextCheck = ''
conn = sqlite3.connect('/Users/sean/bitmo/db/bitmo-01-prod.db')
c = conn.cursor()
TELEGRAM_TOKEN = credentials.TOKEN
TELEGRAM_CHAT_ID = credentials.CHAT_ID

if now.hour > 20:

    # run tomorrow - otherwise run today
    nextCheck = now + dt.timedelta(day=1) # add 1 day to today

nextCheck = now.replace(hour=21, minute=10, second=0) # replace hour, minute, and second
# nextCheck = now.replace(hour=1, minute=32, second=0) # FOR TESTING

while True:

    print('\nNext check scheduled for: {}'.format(nextCheck))

    sql = 'select COUNT(*) from response_status rs WHERE insert_date > \'{}\' AND error_code = 0 AND error_message IS NULL AND credit_count > 0'.format(nextCheck.strftime('%Y-%m-%d %H:%M:%S'))
    # sql = 'select COUNT(*) from response_status rs WHERE insert_date > \'2024-03-15 21:00:00\' AND error_code = 0 AND error_message IS NULL AND credit_count > 0' # FOR TESTING
    
    pause.until(nextCheck)

    print('\n{} - time to verify bitmo'.format(dt.now()))

    c.execute(sql)
    r = c.fetchall()
    print('db result is: {}'.format(r[0][0]))

    if r[0][0] > 1: # currently expecting 2 results, but later this might be 1, or 3 depending on the number of currencies tracked by CMC (1 result for ever 5,000 currencies)

        s = 'Bitmo Successful'

    else:

        s = 'Bitmo FAILURE - investigate!'

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={TELEGRAM_CHAT_ID}&text={s}"
    requests.get(url).json()

    nextCheck = nextCheck + td(days=1)


