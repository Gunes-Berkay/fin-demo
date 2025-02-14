
from django.http import JsonResponse
from django.db import connections

import sqlite3
import requests
import os
import trading
import json

INTERVALS = ['15m', '1h', '4h', '1d']
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "veri.json") 


def fetch_table_data(request, table_name, INTERVAL):
     data = get_table_data(table_name, INTERVAL, limit=100)
     return JsonResponse({'table_data': data}, json_dumps_params={'ensure_ascii': False})

def get_table_data(table_name, INTERVAL, limit=100):

    if not table_name.isalnum() or not INTERVAL.isalnum():
        return []

    try:
        with connections['papers_db'].cursor() as cursor:
            query = f"SELECT * FROM `{table_name}on{INTERVAL}` LIMIT %s"
            cursor.execute(query, [limit])
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()

        # JSON uyumlu hale getirme
        result = [
            {col: (str(value) if isinstance(value, (bytes, memoryview)) else value) for col, value in zip(columns, row)}
            for row in rows
        ]
        return result

    except Exception as e:
        print(f"Error querying table {table_name}{INTERVAL}: {e}")
        return []



def fetch_coins_names(request):
    with open(db_path, 'r', encoding="utf-8") as json_file:
        data = json.load(json_file)

    data = data['data']
    
    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})


def get_analysis(request, symbol):

    for interval in INTERVALS:
        try:
            with connections['papers_db'].cursor() as cursor:
                query = f"SELECT * FROM `{symbol}on{interval}` LIMIT 1"
                cursor.execute(query)
                row = cursor.fetchone()
                column_dict = {desc[0]: index for index, desc in enumerate(cursor.description)}
                rsi = row[column_dict.get('rsi_14')]
                volume = row[column_dict.get('volume')]
                bull_total = row[column_dict.get('bull_total')]

                

            

        except Exception as e:
            print(f"Error querying table {symbol}{interval}: {e}")
            return []
    




    