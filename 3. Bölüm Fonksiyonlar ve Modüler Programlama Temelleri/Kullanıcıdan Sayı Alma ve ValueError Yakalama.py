deger = input().strip()

try:
    # TODO: deger'i int'e çevir ve karesini yazdır
    sayi = int(deger)
    print(sayi ** 2)
except ValueError:
    # TODO: hata mesajını yazdır
    print("Lütfen sayı gir")