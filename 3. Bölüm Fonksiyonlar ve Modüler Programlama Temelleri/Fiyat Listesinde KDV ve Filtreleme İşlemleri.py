# Başlangıç fiyat listesi
prices = [50, 120, 75, 200, 30, 150]

# TODO: map + lambda ile %18 KDV ekle, listeye çevir
kdv_li_fiyatlar = list(map(lambda p: p * 1.18, prices))  # lambda'yı düzenle

# TODO: filter + lambda ile 100 TL üzerini seç, listeye çevir
pahali_fiyatlar = list(filter(lambda p: p > 100, kdv_li_fiyatlar))  # lambda'yı düzenle

print(kdv_li_fiyatlar)
print(pahali_fiyatlar)