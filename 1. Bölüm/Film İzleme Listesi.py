films = []

# TODO: kullanıcıdan 3 film adı al ve append ile listeye ekle
for _ in range(3):
    film = input().strip()
    films.append(film)

# TODO: en son eklenen filmi pop ile çıkar ve yazdır
last_film = films.pop()
print(last_film)
