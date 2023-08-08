# from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver as wiredriver
from seleniumwire.utils import decode
import time
import json

print('all imported successfully')

PROXY_HOST = '149.215.113.110'
PROXY_PORT = '70'

print('starting Chrome...')

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--proxy-server=http://{}:{}'.format(PROXY_HOST, PROXY_PORT))
driver = wiredriver.Chrome(options=chrome_options)

# sleep 10 seconds
print('sleeping 5 seconds...')
time.sleep(5)

print('Go to web page')
driver.get("https://app.aada.finance/market")

print('sleeping 5 seconds...')
time.sleep(5)

print('getting http responses:')
for request in driver.requests:
    if (request.url == 'https://app.aada.finance/api/lending_and_borrowing/get_loan_requests'):
        # print(request.url, request.response.status_code, request.response.headers['Content-Type'])
        body = decode(request.response.body, request.response.headers.get('Content-Encoding', 'identity'))
        # response.body.decode('utf-8')
        body = json.loads(body)
        print('{}'.format(body))
        # print('request dir: \n{}\n\nrequest.response dir: \n{}\n'.format(dir(request), dir(request.response)))

print("Quitting Selenium WebDriver")
driver.quit()

'string'.format()