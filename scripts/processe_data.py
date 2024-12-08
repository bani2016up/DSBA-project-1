import os
import pandas
import requests

import numpy as np

from typing import Final
from dateutil import parser
from functools import  cache
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("EXCHANGERATE_API_KEY")
if not API_KEY:
    raise ValueError("Exchange rate API key not found in environment variables. Use EXCHANGERATE_API_KEY.")

path_to_dataset: Final[str] = "synthetic_fraud_data.csv"
exchange_rate_cache = {}


dataset = pandas.read_csv(path_to_dataset)


@cache
def get_exchange_rate(currency: str):

    url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{currency.upper()}'
    print(url)

    try:
        response = requests.get(url)
        data = response.json()

        if data['result'] != 'success':
            raise ValueError(f"Error fetching exchange rate: {data.get('error-type', 'Unknown error')}")


        rates = data['conversion_rates']

        usd_rate = rates.get('USD')
        if usd_rate is None:
            print("USD rate not found in response.")
            return None

        return usd_rate
    except Exception as e:
        print(f"Exception occurred: {e}")
        return None

def convert_to_usd(row):
    amount = row['amount']
    currency = row['currency']
    timestamp = row['timestamp']


    # TODO: Use timestamp to parse money, and history api. [Needs not free subscription]
    # Format the date for the API ('YYYY-MM-DD')
    # if isinstance(timestamp, str):
    #     try:
    #         timestamp_dt = parser.parse(timestamp)
    #     except ValueError:
    #         return None
    # else:
    #     return None

    rate = get_exchange_rate(currency)
    if rate is None:
        return None

    amount_usd = amount * rate
    return amount_usd


dataset['amount_usd'] = dataset.apply(convert_to_usd, axis=1)
dataset.to_csv("processed_data.csv")
