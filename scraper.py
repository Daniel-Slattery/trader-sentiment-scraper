from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import WebDriverException
from utilities.isMarketOpen import is_forex_market_open
from utilities.transformData import transform_data_and_append
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
    driver.get(url)
    time.sleep(10)  # Wait for JavaScript to load data

    headers = [header.text for header in driver.find_elements(By.CLASS_NAME, 'SentimentRowCaption')]
    values = [value.text for value in driver.find_elements(By.CLASS_NAME, 'SentimentValueCaptionLong')]

    if len(headers) != len(values):
        return None

    next_hour = (datetime.now() + timedelta(hours=1)).replace(minute=0, second=0)
    base_directory = r'C:\Users\danie\OneDrive\DataScraping\sentimentData'
    if not os.path.exists(base_directory):
        os.makedirs(base_directory)

    filename = f'{datetime.now().strftime("%b-%Y").lower()}-sentiment.csv'
    full_file_path = os.path.join(base_directory, filename)

    data_dict = {"Timestamp": next_hour.strftime('%Y-%m-%d %H:%M')}
    for header, value in zip(headers, values):
        data_dict[header] = value

    # Check if file exists and headers match
    if not os.path.exists(full_file_path):
        with open(full_file_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["Timestamp"] + headers)
            writer.writeheader()

    with open(full_file_path, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["Timestamp"] + headers)
        writer.writerow(data_dict)

    return data_dict

def run_scraping_task():
    if is_forex_market_open():
        driver = None
        options = Options()

        try:
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        except WebDriverException:
            try:
                brave_path = 'C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe'
                options.binary_location = brave_path
                driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
            except WebDriverException:
                try:
                    driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
                except WebDriverException:
                    return

        data_dict = scrape(driver)
        if data_dict:
            transform_data_and_append(data_dict)
        if driver:
            driver.quit()

        try:
            requests.get(monitoring_url)
        except requests.exceptions.RequestException as e:
            print("Error pinging monitoring URL")

if __name__ == "__main__":
    run_scraping_task()