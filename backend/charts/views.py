
from django.http import JsonResponse
from django.db import connections

import sqlite3
import requests
import os
import trading


API_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
API_KEY = "e58be2f2-404d-4d5a-893a-cb486e74024d"

def fetch_table_data(request, table_name):
    data = get_table_data(table_name, limit=50)  # Fetch 50 rows
    return JsonResponse({'table_data': data})


def get_table_data(table_name, limit=100):
    """
    Fetches data from a specified table in the `papers_db` database.

    Args:
        table_name (str): The name of the table to query.
        limit (int): The number of rows to return (default is 10).

    Returns:
        list: A list of rows from the table.
    """
    try:
        with connections['papers_db'].cursor() as cursor:
            query = f"SELECT * FROM {table_name} LIMIT {limit}"
            cursor.execute(query)
            rows = cursor.fetchall()
        return rows
    except Exception as e:
        print(f"Error querying table {table_name}: {e}")
        return []

def fetch_coins_names(request):
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": API_KEY,
    }
    params = {
        "start": "10",
        "limit": "50",
        "convert": "USD",
    }
    response = requests.get(API_URL, headers=headers, params=params)
    data = response.json()
    coins_dict = {coin['symbol']+'USDT': "BINANCE" for coin in data['data']}

    return coins_dict