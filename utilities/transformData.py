import os
import pandas as pd

def transform_data_and_append(data_dict):
    """
    Transforms the provided data dictionary according to the specified criteria and appends the result
    to AverageSentiment.csv.
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
            # If the currency is the second part of the pair, use 1 - value, else use the value directly
            if col.split('/')[-1] == currency:
                values.append(1 - float(value) / 100)
            else:
                values.append(float(value) / 100)

        # Calculate the average for these values
        result[currency] = sum(values) / len(values)

    # Append the result to AverageSentiment.csv
    result.to_csv('AverageSentiment.csv', mode='a', header=not os.path.exists('AverageSentiment.csv'), index=False)
