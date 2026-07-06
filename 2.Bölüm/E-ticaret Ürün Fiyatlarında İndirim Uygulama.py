prices = {
    "laptop": 25000,
    "telefon": 15000,
    "kulaklik": 1500,
}

indirimli_fiyatlar = {product: price * 0.9 for product, price in prices.items()}

for product, old_price in prices.items():
    print(f"{product}: {old_price} -> {indirimli_fiyatlar[product]}")
