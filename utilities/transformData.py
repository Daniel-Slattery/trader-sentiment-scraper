import os
import pandas as pd
from datetime import datetime

def transform_data_and_append(data_dict):
    """
    Transforms the provided data dictionary according to the specified criteria and appends the result
    to a monthly CSV file in the AverageSentiment directory.
    """
    # Convert the data dictionary into a DataFrame for easier processing
    row_df = pd.DataFrame([data_dict])

    # Create a new DataFrame for the result
    result = pd.DataFrame([row_df['Timestamp'].iloc[0]], columns=['Timestamp'])

    # Iterate through the specified currencies and apply the processing steps
    for currency in ['GBP', 'EUR', 'USD', 'JPY', 'AUD', 'CHF']:
        # Identify columns containing the currency pair
        currency_columns = [col for col in row_df.columns if currency in col]

        # Process each column to get the appropriate value
        values = []
        for col in currency_columns:
            value = row_df[col].iloc[0].rstrip('%')
            if col.split('/')[-1] == currency:
                values.append(1 - float(value) / 100)
            else:
                values.append(float(value) / 100)

        # Calculate the average for these values
        result[currency] = sum(values) / len(values)

    # Base directory for AverageSentiment data
    base_directory = r'C:\Users\danie\OneDrive\DataScraping\sentimentData\AverageSentiment'

    # Ensure the directory exists
    if not os.path.exists(base_directory):
        os.makedirs(base_directory)

    # Determine the filename based on current month and year
    current_time = datetime.now()
    filename = f'{current_time.strftime("%b-%Y").lower()}-averagesentiment.csv'

    # Full path of the file
    full_file_path = os.path.join(base_directory, filename)

    # Append the result to the appropriate CSV file
    result.to_csv(full_file_path, mode='a', header=not os.path.exists(full_file_path), index=False)
