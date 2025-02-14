import ccxt
import pandas as pd
exchange = ccxt.binance()
markets = exchange.load_markets()
# print(markets.get('PENDLE/USDT:USDT'))
# # print(markets.get('GODS/USDT:USDT'))
ticker = exchange.fetch_ticker('PENDLE/USDT:USDT')
print(ticker)
# Swap piyasalarını bul
# swap_markets = [symbol for symbol in markets if markets[symbol]['swap']]

# print("Swap piyasaları:", swap_markets)

# swap_tickers = {}

# for symbol in swap_markets:  # Sadece swap piyasaları için
#     try:
#         ticker = exchange.fetch_ticker(symbol)
#         swap_tickers[symbol] = ticker
#     except Exception as e:
#         print(f"Hata {symbol}: {e}")

# # Swap verisi geldiyse max hesapla
# if swap_tickers:
#     most_gained = max(
#     (item for item in swap_tickers.items() if item[1].get('percentage') is not None),
#     key=lambda x: x[1].get('percentage', 0)
#     )
#     print(f"En çok artan swap çifti: {most_gained[0]}")
#     print(f"Değişim yüzdesi: {most_gained[1].get('percentage', 0)}%")
# else:
#     print("Hiçbir swap tick verisi alınamadı.")
