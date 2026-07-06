toplam = 0

while True:
    # kullanıcıdan sayı al
    # kurallara göre break / continue kullan
    sayi = int(input())
    
    if sayi == 0:
        break
        
    if sayi < 0:
        continue
        
    toplam += sayi

print(toplam)