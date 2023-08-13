# import pywhatkit

# pywhatkit.sendwhatmsg_instantly(
#     phone_no="+15125607878", 
#     message="Howdy! This message will be sent instantly!",
# )

import time 
import pywhatkit
import pyautogui
from pynput.keyboard import Key, Controller

keyboard = Controller()


def send_whatsapp_message(msg: str):
    try:
        pywhatkit.sendwhatmsg_instantly(
            phone_no="+15125607878", 
            message=msg,
            tab_close=True
        )
        time.sleep(1)
        pyautogui.click()
        time.sleep(1)
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        print("Message sent!")
    except Exception as e:
        print(str(e))


# if __name__ == "__main__":
#     send_whatsapp_message(msg="Test message from a Python script!")