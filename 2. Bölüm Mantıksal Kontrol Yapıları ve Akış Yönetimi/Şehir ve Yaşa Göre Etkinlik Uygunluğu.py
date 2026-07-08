sehir = input().strip()
yas = int(input())

# Şehir karşılaştırmasını büyük/küçük harf duyarsız olacak şekilde yapıyoruz.
# Standard Python'da "İstanbul".lower() -> "i\u0307stanbul" (combining dot) ürettiği için,
# Türkçe büyük/küçük harf uyumsuzluklarını da (I/ı, İ/i) kapsayacak şekilde normalleştirme yapıyoruz.
sehir_lower = sehir.lower().replace('ı', 'i').replace('\u0307', '')

if sehir_lower == "istanbul" and yas >= 18:
    print("Etkinlik uygun")
else:
    print("Uygun değil")
