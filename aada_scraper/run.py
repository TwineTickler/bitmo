from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import json

# Enable Performance Logging of Chrome.
desired_capabilities = DesiredCapabilities.CHROME
desired_capabilities["goog:loggingPrefs"] = {"performance": "ALL"}

# Create the webdriver object and pass the arguments
options = webdriver.ChromeOptions()

# Chrome will start in Headless mode
options.add_argument('headless')

# Ignores any certificate errors if there is any
options.add_argument("--ignore-certificate-errors")

print(desired_capabilities)
print(options)

# Startup the chrome webdriver with executable path and
# pass the chrome options and desired capabilities as
# parameters.
driver = webdriver.Chrome(
    # executable_path="C:/chromedriver.exe",
    chrome_options=options,
    desired_capabilities=desired_capabilities
    )

# sleep 10 seconds
print('sleeping 10 seconds...')
time.sleep(10)

print("Quitting Selenium WebDriver")
driver.quit()

