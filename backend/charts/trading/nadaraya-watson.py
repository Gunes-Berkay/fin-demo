import sqlite3
import numpy as np
import pandas as pd
import os 

def fetch_data(db_path, table_name):
    conn = sqlite3.connect(db_path)
    query = f"SELECT close, high, low FROM {table_name} ORDER BY datetime"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Rational Quadratic Kernel Regression (Nadaraya-Watson)
def rational_quadratic_kernel(x, y, h, alpha):
    n = len(x)
    y_hat = np.zeros(n)

    for i in range(n):
        weights = (1 + ((x[i] - x) ** 2) / (alpha * h ** 2)) ** (-alpha)
        weights /= np.sum(weights)
        y_hat[i] = np.sum(weights * y)

    return y_hat

# ATR Hesaplama
def compute_atr(high, low, close, length=60):
    tr = np.maximum(high - low, np.maximum(abs(high - np.roll(close, 1)), abs(low - np.roll(close, 1))))
    tr[0] = np.nan  # İlk değer NaN olacak
    atr = pd.Series(tr).rolling(window=length, min_periods=1).mean().to_numpy()
    return atr

# Üst ve Alt Bantları Hesaplama
def compute_bounds(yhat, atr, near_factor=1.5, far_factor=6.0, top_factor=9.5):
    upper_near = yhat + near_factor * atr
    upper_far = yhat + far_factor * atr
    upper_top = yhat + top_factor *atr 
    lower_near = yhat - near_factor * atr
    lower_far = yhat - far_factor * atr
    lower_top = yhat - top_factor *atr 
    return upper_near, upper_far, upper_top, lower_near, lower_far, lower_top

# 📌 **Ana İşlem**
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "papers.sqlite3")

# Veriyi çek
df = fetch_data(db_path, "BTCUSDTon4h")

# Nadaraya-Watson tahmini uygula
h, alpha = 8, 8  # Kernel parametreleri
df["yhat"] = rational_quadratic_kernel(np.arange(len(df)), df["close"].values, h, alpha)

# ATR Hesapla
df["atr"] = compute_atr(df["high"].values, df["low"].values, df["close"].values)

# Bantları hesapla
df["upper_near"], df["upper_far"], df["upper_top"], df["lower_near"], df["lower_far"], df["lower_top"] = compute_bounds(df["yhat"], df["atr"])

# Sonuçları göster
print(df[["upper_near", "upper_far","upper_top", "lower_near", "lower_far", "lower_top"]].dropna())
