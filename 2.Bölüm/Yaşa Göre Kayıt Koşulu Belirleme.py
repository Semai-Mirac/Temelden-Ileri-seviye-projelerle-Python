age = int(input())

if age < 18:
    durum = "Kayıt olamaz"
elif age <= 65:
    durum = "Kayıt olabilir"
else:
    durum = "Manuel onay gerekli"

print(durum)
