from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from utilities import is_forex_market_open
import time
import csv
from datetime import datetime, timedelta
import os
import platform

# Get the URL from the environment variable
url = os.environ.get('SENTIMENT_URL')

# Setup the driver. This is the part that opens up a browser
driver = None

def scrape(driver):
    # Make a request to the website
    driver.get(url)

    # Wait for the JavaScript to load the data
    time.sleep(5)

    # Now the data should be loaded we can grab it
    headers = [header.text for header in driver.find_elements(By.CLASS_NAME, 'SentimentRowCaption')]
    values = [value.text for value in driver.find_elements(By.CLASS_NAME, 'SentimentValueCaptionLong')]

    # Get the next hour as the timestamp
    next_hour = (datetime.now() + timedelta(hours=1)).replace(minute=0, second=0)
    data_row = [next_hour.strftime('%Y-%m-%d %H:%M')] + values

    with open('Sentiment.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        if f.tell() == 0:  # file is empty, write headers
            writer.writerow(["Timestamp"] + headers)
        print(f"Writing item: {data_row}")  # Print each item before writing
        writer.writerow(data_row)  # adjust this depending on the structure of 'item'

while True:
    if is_forex_market_open():
        # Get current minutes
        current_min = datetime.now().minute
        # If it's 5 minutes to the next hour
        if current_min == 55:
            # Check if the driver is None
            if driver is None:
                # Detect the platform
                system = platform.system()
                if system == 'Windows':
                    # Use Brave on Windows
                    brave_path = 'C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe'
                    options = Options()
                    options.binary_location = brave_path
                    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
                elif system == 'Darwin':
                    # Use Chrome on macOS
                    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
                else:
                    print("Unsupported platform:", system)
                    exit(1)

            scrape(driver)
            # Remember to close the driver when done
            driver.quit()
            time.sleep(300)  # Sleep for 5 minutes to avoid duplicate entries for the same hour

    time.sleep(60)  # Check every minute