import csv
import random
from datetime import datetime, timedelta, date

# Define the headers of the CSV file
headers = ["Timestamp","AUD/CAD","AUD/JPY","AUD/NZD","AUD/USD","CAD/CHF","CAD/JPY","DAX","DJ30","EUR/AUD","EUR/CAD","EUR/CHF","EUR/GBP","EUR/JPY","EUR/NZD","EUR/USD","GBP/AUD","GBP/CAD","GBP/CHF","GBP/JPY","GBP/USD","NZD/CAD","NZD/USD","USD/CAD","USD/CHF","USD/JPY","XAU/USD"]

# Function to generate a random percentage
def random_percentage():
    return f"{random.uniform(10, 90):.1f}%"

# Get current year
current_year = datetime.now().year

# Start and end date of the current year
start_date = date(current_year, 1, 1)
end_date = date(current_year, 12, 31)

# Create the CSV file
with open('year_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headers)  # write the headers

    # For each day of the current year
    delta = end_date - start_date
    for day in range(delta.days + 1):
        date_str = (start_date + timedelta(days=day)).strftime("%Y-%m-%d")

        # For each hour of the day
        for hour in range(24):
            # Generate the timestamp
            timestamp_str = f"{date_str} {hour:02d}:00"

            # Generate the random data for the symbols
            data = [random_percentage() for _ in range(len(headers) - 1)]

            # Write the data to the CSV file
            writer.writerow([timestamp_str] + data)
