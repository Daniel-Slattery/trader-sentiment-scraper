from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from utilities.isMarketOpen import is_forex_market_open
import time
import csv
from datetime import datetime, timedelta
import os
import platform
import requests

# Get the URLs from the environment variables
url = os.environ.get('SENTIMENT_URL')
monitoring_url = os.environ.get('MONITORING_URL')
headerMismatchURL = os.environ.get('HEADER_MISMATCH_URL')


def scrape(driver):
    # Make a request to the website
    driver.get(url)

    # Wait for the JavaScript to load the data
    time.sleep(10)

    # Now the data should be loaded we can grab it
    headers = [header.text for header in driver.find_elements(By.CLASS_NAME, 'SentimentRowCaption')]
    values = [value.text for value in driver.find_elements(By.CLASS_NAME, 'SentimentValueCaptionLong')]

    if len(headers) != len(values):
        print("Mismatch in number of headers and values.")
        return

    # Get the next hour as the timestamp
    next_hour = (datetime.now() + timedelta(hours=1)).replace(minute=0, second=0)

    # Convert data into dictionary
    data_dict = {"Timestamp": next_hour.strftime('%Y-%m-%d %H:%M')}
    for header, value in zip(headers, values):
        data_dict[header] = value

    # Check if file exists and headers match
    filename = 'Sentiment.csv'
    combined_headers = ["Timestamp"]  # Starting with just the Timestamp

    if os.path.exists(filename):
        with open(filename, 'r') as f:
            existing_headers = next(csv.reader(f))

            headers_mismatch = False

            # Handle missing headers
            for header in existing_headers[1:]:  # Exclude the "Timestamp"
                if header not in headers:  # If existing header is not in the new headers
                    headers_mismatch = True
                    data_dict[header] = '50.0%'

            # Handle new headers
            for header in headers:
                if header not in existing_headers:
                    headers_mismatch = True
                    data_dict.pop(header, None)  # Remove the new header from data_dict

            if headers_mismatch:
                print("Headers mismatch!")
                # Ping headerMismatchURL due to the mismatch
                try:
                    requests.get(headerMismatchURL)
                    print("Notified the headerMismatchURL due to headers mismatch.")
                except requests.exceptions.RequestException as e:
                    print("Error pinging headerMismatchURL:", e)

            combined_headers += existing_headers[1:]

    with open(filename, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=combined_headers)
        if f.tell() == 0:  # file is empty, write headers
            writer.writeheader()
        print(f"Writing item: {data_dict}")  # Print each item before writing
        writer.writerow(data_dict)

while True:
    if is_forex_market_open():
        # Get current minutes
        current_min = datetime.now().minute
        # If it's 5 minutes to the next hour
        if current_min == 55:
            # Detect the platform
            system = platform.system()
            driver = None  # Move the initialization here
            options = Options()
            # Trying Chrome
            try:
                driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            except WebDriverException:
                # If Chrome doesn't work, try Brave
                try:
                    brave_path = 'C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe'  # Path for Windows
                    options.binary_location = brave_path
                    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
                except WebDriverException:
                    # If Brave also doesn't work, revert to using Edge
                    try:
                        driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))
                    except WebDriverException:
                        print("All browsers (Chrome, Brave, and Edge) failed to initiate.")
                        exit(1)

            scrape(driver)
            # Remember to close the driver when done
            driver.quit()
            time.sleep(300)  # Sleep for 5 minutes to avoid duplicate entries for the same hour
    # Ping the monitoring URL
    try:
        requests.get(monitoring_url)
    except requests.exceptions.RequestException as e:
        print("Error pinging monitoring URL:", e)

    time.sleep(60)  # Check every minute