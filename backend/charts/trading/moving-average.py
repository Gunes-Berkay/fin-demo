import numpy as np
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "papers.sqlite3")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()
coin_symbol = 'ETHUSDT'
interval = '4h'
table_name = (f"{coin_symbol}on{interval}")
cursor.execute(f"SELECT datetime, close FROM {table_name} ORDER BY datetime")
data = cursor.fetchall()
conn.close()

dates, prices = zip(*data)
X = np.arange(len(dates))
Y = np.array(prices)


def optimized_std_devs(Y, window=14, alpha=0.84):
    """
    Zamanla daha yakın verilere ağırlık vererek optimize edilmiş standart sapma hesaplama.
    - window: standart sapmanın hesaplanacağı pencere boyutu
    - alpha: zaman ağırlığının katsayısı (0-1 arası, 1'e yaklaştıkça daha fazla ağırlık verir)
    """
    smoothed_std_devs = []
    global_std = np.std(Y)  

    for i in range(len(Y)):
        start_idx = max(0, i - window)
        window_data = Y[start_idx:i+1]
        
        # Pencere içindeki standart sapma
        window_std_dev = np.std(window_data)
        
        # Zamanla daha yakın verilere ağırlık verirken, global standart sapmayı da dikkate alır
        smoothed_std_dev = (alpha * window_std_dev) + ((1 - alpha) * global_std)
        smoothed_std_devs.append(smoothed_std_dev)

    return np.array(smoothed_std_devs)

std_devs = optimized_std_devs(Y)

# Hareketli Ortalama hesapla
def moving_average(Y, window=14):
    """
    Y: Zaman serisi verisi (fiyatlar vb.)
    window: Hareketli ortalama için pencere boyutu
    
    return: Hareketli ortalama
    """
    return np.convolve(Y, np.ones(window)/window, mode='valid')

ma = moving_average(Y)

# Hareketli ortalama ve standart sapmayı uyumlu hale getirmek için uzunluğu eşitleme
# Eğer ma dizisi daha kısa ise, başına sıfır ekleyebilirsiniz
if len(ma) < len(std_devs):
    ma = np.pad(ma, (len(std_devs) - len(ma), 0), 'constant', constant_values=0)

# Üst ve alt bantları hesapla
upper_band_1 = ma + std_devs
upper_band_2 = ma + 3.14 * std_devs
lower_band_1 = ma - std_devs
lower_band_2 = ma - 3.14 * std_devs

# Sonuçları yazdır
for i, date in enumerate(dates):
    print(f"Tarih: {date}")
    print(f"  Ortalama (Siyah Çizgi): {ma[i]:.4f}")
    print(f"  Açık Yeşil Bölge (Üst 1): {upper_band_1[i]:.4f}")
    print(f"  Koyu Yeşil Bölge (Üst 2): {upper_band_2[i]:.4f}")
    print(f"  Açık Kırmızı Bölge (Alt 1): {lower_band_1[i]:.4f}")
    print(f"  Koyu Kırmızı Bölge (Alt 2): {lower_band_2[i]:.4f}")
    print("-" * 40)
