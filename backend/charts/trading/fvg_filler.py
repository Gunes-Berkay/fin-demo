import os 
import sqlite3
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "papers.sqlite3")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def control(symbol, interval):
    full_df = pd.read_sql_query(f"""
    SELECT * FROM {symbol}on{interval}
    ORDER BY datetime ASC
    """, conn)

    fvg_df = pd.read_sql_query(f"""
    SELECT * FROM {symbol}on{interval}_fvg
    ORDER BY datetime ASC
    """, conn)

    for i in range(len(fvg_df)-1):

        datetime = fvg_df.iloc[i]['datetime']
        direction = fvg_df.iloc[i]['direction']
        start_price = fvg_df.iloc[i]['start_price']
        end_price = fvg_df.iloc[i]['end_price']
        touch_start, touch_half, touch_end = 0,0,0
        half_price = (start_price+end_price)/2

        df = pd.read_sql_query(f"""
        SELECT * FROM {symbol}on{interval}
        WHERE datetime>'{datetime}'
        """, conn)

        if direction == "up" and not (touch_start or touch_half or touch_end):
            for index, row in df.iterrows():
                if row['low'] <= end_price:
                    touch_start, touch_half, touch_end = 1,1,1
                elif row['low'] <= half_price:
                    touch_half, touch_start = 1,1
                elif row['low'] <= start_price:
                    touch_start = 1
        
        elif direction == "bottom" and not (touch_start or touch_half or touch_end):
            for index, row in df.iterrows():
                if row['high'] >= end_price:
                    touch_start, touch_half, touch_end = 1,1,1
                elif row['high'] >= half_price:
                    touch_half, touch_start = 1,1
                elif row['high'] >= start_price:
                    touch_start = 1
        
        cursor.execute(f"""
        UPDATE {symbol}on{interval}_fvg
        SET touch_start = ?, touch_half = ?, touch_end = ?
        WHERE datetime = ?
        """, (touch_start, touch_half, touch_end, datetime))

        conn.commit()


control('DOGEUSDT', '4h')
         
