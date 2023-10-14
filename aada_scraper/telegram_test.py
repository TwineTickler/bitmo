import credentials
import requests

'''
# run this with your token to get the Chat ID
# make sure to send a message to your bot first or this will return empty

TOKEN = credentials.TOKEN
url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
print(requests.get(url).json())
'''

TOKEN = credentials.TOKEN
chat_id = credentials.CHAT_ID
message = "hello from your telegram bot"
url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"

try:
    requests.get(url).json() # this sends the message
    print('message sent successfully')
except Exception as e:
    print(e)
