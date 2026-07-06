sifre = input().strip()

# 1) Şifre uzunluğu 8 veya daha fazla mı?
# TODO: True / False üret (ipucu: len(...))
is_strong = len(sifre) >= 8
print(is_strong)

# 2) Şifre güçlü ise 'Güçlü', değilse 'Zayıf' yazdır
# TODO: if/else ile mesajı belirle
if is_strong:
    print("Güçlü")
else:
    print("Zayıf")
