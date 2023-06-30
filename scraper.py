from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import csv
from datetime import datetime
import os

# Get the URL from the environment variable
url = os.environ.get('SENTIMENT_URL')

# Setup the driver. This is the part that opens up a browser
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

def scrape():
    # Make a request to the website
    driver.get(url)

    # Wait for the JavaScript to load the data
    time.sleep(5)

    # Now the data should be loaded we can grab it
    headers = [header.text for header in driver.find_elements(By.CLASS_NAME, 'SentimentRowCaption')]
    values = [value.text for value in driver.find_elements(By.CLASS_NAME, 'SentimentValueCaptionLong')]

    data_row = [str(datetime.now())] + values

    with open('Sentiment.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        if f.tell() == 0:  # file is empty, write headers
            writer.writerow(["Timestamp"] + headers)
        print(f"Writing item: {data_row}")  # Print each item before writing
        writer.writerow(data_row)  # adjust this depending on the structure of 'item'

while True:
    scrape()
    time.sleep(3600)  # Wait for 1 hour

# Remember to close the driver when done
driver.quit()
