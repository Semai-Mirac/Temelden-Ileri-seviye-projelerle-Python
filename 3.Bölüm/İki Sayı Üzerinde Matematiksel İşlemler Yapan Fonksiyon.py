def hesapla(a, b):
    # TODO: toplam, fark ve çarpımı tuple olarak döndür
    return (a + b, a - b, a * b)

a = int(input())
b = int(input())

# TODO: fonksiyonu çağır ve sonuçları unpack et
toplam, fark, carpim = hesapla(a, b)
print(toplam)
print(fark)
print(carpim)