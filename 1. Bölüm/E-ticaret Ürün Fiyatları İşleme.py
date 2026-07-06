prices = [120, 340, 560, 80, 45, 999, 150]

# TODO:
# - 100 TL'den küçükleri hariç tut
# - kalanların %10 indirimli halini hesapla
# - sonucu küçükten büyüğe sırala
# ipucu: list comprehension + sorted(...)
discounted_sorted_prices = sorted([price * 0.9 for price in prices if price >= 100])

print(discounted_sorted_prices)
