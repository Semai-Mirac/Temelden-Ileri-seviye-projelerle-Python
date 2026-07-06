total = float(input())
city = input()

# Şehir kontrolü büyük/küçük harf duyarsız olmalıdır.
# Türkçe büyük/küçük harf uyumsuzluklarını (I/ı, İ/i) ve Unicode birleştirme karakterlerini (\u0307) normalize ediyoruz.
city_lower = city.lower().replace('ı', 'i').replace('\u0307', '')

if total >= 750:
    kargo_ucreti = 0
elif city_lower == "istanbul":
    kargo_ucreti = 39
elif city_lower == "izmir" or city_lower == "ankara":
    kargo_ucreti = 49
else:
    kargo_ucreti = 59

print(f"Kargo ücreti: {kargo_ucreti} TL")
