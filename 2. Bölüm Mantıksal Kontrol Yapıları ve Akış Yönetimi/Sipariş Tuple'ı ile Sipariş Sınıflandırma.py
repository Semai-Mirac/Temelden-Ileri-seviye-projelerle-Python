order = (1234, 5678, 2450.0)

order_id, customer_id, total = order
print("Yüksek" if total > 1000 else "Düşük")
