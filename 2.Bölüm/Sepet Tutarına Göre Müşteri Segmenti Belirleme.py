sepet_tutari = float(input())

if sepet_tutari < 500:
    segment = "Standart"
elif sepet_tutari < 1500:
    segment = "Ücretsiz Kargo"
else:
    segment = "VIP İndirim"

print(segment)
