def metni_isle(metin):
    temiz_metin = metin.strip().lower()
    return len(temiz_metin.split())


metin = input()
print(metni_isle(metin))
