# FX Trading Sentiment Data Scraper
source venv/Scripts/activate

This project scrapes forex trading sentiment data and saves it to a CSV file.

## Installation

1. Clone this repository.
2. Install the project's dependencies by running `pip install -r requirements.txt`.

## Usage

1. Create a `.env` file in the project's root directory.
2. Add the following line to the `.env` file, replacing `SENTIMENT_URL` with the URL of the sentiment data page.
3. If you have a URL to ping for monitoring purposes, you can add it to the `.env` file with the variable `MONITORING_URL`.
4. Run the script with the command `python scraper.py`.

## Dummy Data Generation

If you wish to generate dummy data with the same format as the output of `scraper.py`, you can use the `generateDummyCSV.py` script located in the `utilities` folder. Run it with the command `python utilities/generateDummyCSV.py`.

## Output

A CSV file named `sentiment.csv` will be created in the project's root directory.
![CSV File Output](images/csv_output.png)
