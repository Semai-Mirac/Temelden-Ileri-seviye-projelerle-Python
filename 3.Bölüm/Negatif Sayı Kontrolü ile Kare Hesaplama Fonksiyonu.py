def kare_al(sayi):
    # Negatifse None, değilse karesini döndürür
    if sayi < 0:
        return None
    return sayi ** 2

for _ in range(3):
    sayi = int(input())
    sonuc = kare_al(sayi)
    # Sonuca göre "Geçersiz" ya da sonucu yazdırır
    if sonuc is None:
        print("Geçersiz")
    else:
        print(sonuc)