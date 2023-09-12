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

        # pywhatkit.sendwhatmsg("+910123456789", "Hi", 13, 30)
        pywhatkit.sendwhatmsg_instantly(
            "+15125607878", 
            str, 
            1, 
            True, 
            1
        ) # sendwhatmsg_instantly(phone_no: str, message: str, wait_time: int = 15, tab_close: bool = False, close_time: int = 3) -> None

        time.sleep(3)
        
        pyautogui.click()
        
        time.sleep(3)
        
        keyboard.press(Key.enter)
        
        keyboard.release(Key.enter)
        
        print("Message sent!")
    except Exception as e:
        print(str(e))


# if __name__ == "__main__":
#     send_whatsapp_message(msg="Test message from a Python script!")