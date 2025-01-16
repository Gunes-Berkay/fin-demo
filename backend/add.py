import sqlite3
import requests
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "db.sqlite3") # Django veritabanı dosyanızın yolu
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# CoinMarketCap API'den veri çekme
API_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
API_KEY = "e58be2f2-404d-4d5a-893a-cb486e74024d"

def fetch_top_100_coins():
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": API_KEY,
    }
    params = {
        "start": "1",
        "limit": "100",
        "convert": "USD",
    }
    response = requests.get(API_URL, headers=headers, params=params)
    data = response.json()
    return data["data"]

# Veritabanına verileri ekleme
def insert_coins_into_db():
    coins = fetch_top_100_coins()
    for coin in coins:
        paper_id = coin["id"]
        name = coin["name"]
        try:
            # Veriyi tabloya ekle
            cursor.execute(
                "INSERT INTO wallet_paper (paper_id, name) VALUES (?, ?)",
                (paper_id, name),
            )
        except sqlite3.IntegrityError:
            print(f"'{name}' zaten eklenmiş, atlanıyor...")
    conn.commit()
    print("İlk 100 coin başarıyla veritabanına eklendi.")

# Scripti çalıştırma
if __name__ == "__main__":
    print()
    insert_coins_into_db()

# Bağlantıyı kapat
conn.close()
