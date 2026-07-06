# 0-50 arası sayılardan sadece 3'ün katlarını seç
# TODO: list comprehension kullan
multiples_of_3 = [x for x in range(51) if x % 3 == 0]

# İlk 5 elemanı slice ile al
first_five = multiples_of_3[:5]

print(first_five)
