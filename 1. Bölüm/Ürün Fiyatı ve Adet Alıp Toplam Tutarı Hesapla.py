# Kullanıcıdan fiyat (float) ve adet (int) al
fiyat = float(input().strip())
adet = int(input().strip())

# KDV %20 ekleyerek toplam tutarı hesapla
# ipucu: toplam = (fiyat * adet) * 1.20
toplam = (fiyat * adet) * 1.20

# Sonucu 2 ondalık basamakla yazdır
# 2 ondalık basamak ile yazdır (örn: 240.00)
print(f"{toplam:.2f}")
