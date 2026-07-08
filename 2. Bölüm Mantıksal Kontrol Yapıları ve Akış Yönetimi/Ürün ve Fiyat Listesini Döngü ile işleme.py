products = ["Laptop", "Telefon", "Kulaklık"]
prices = [25000, 15000, 750]

max_product = ""
max_price = 0

for product, price in zip(products, prices):
    print(f"{product}: {price}")
    if price > max_price:
        max_price = price
        max_product = product

print(f"En pahalı: {max_product} - {max_price}")
