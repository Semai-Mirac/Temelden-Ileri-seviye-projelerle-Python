cumle = input()

# Boşluk karakterlerini hesaba katmadan harf frekanslarını sayalım
frekanslar = {}
for karakter in cumle:
    if not karakter.isspace():
        harf = karakter.lower()
        frekanslar[harf] = frekanslar.get(harf, 0) + 1

# En çok geçen 3 harfi belirleyelim
en_cok_gecenler = sorted(frekanslar.items(), key=lambda x: x[1], reverse=True)[:3]

# Sonuçları yazdıralım
for harf, frekans in en_cok_gecenler:
    print(f"{harf}: {frekans}")