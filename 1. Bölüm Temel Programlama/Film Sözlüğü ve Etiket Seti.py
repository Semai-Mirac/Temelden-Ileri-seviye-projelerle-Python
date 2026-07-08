# 1) film dictionary'si oluştur (title, year, rating)
film = {
    "title": "Inception",
    "year": 2010,
    "rating": 8.8,
}

# 2) tags set'i oluştur ve birkaç etiket ekle
tags = set()
tags.add("sci-fi")
tags.add("thriller")
tags.add("action")

# 3) Film bilgisini yazdır
print(film)

# 4) Tag sayısını yazdır (Tags: X)
print(f"Tags: {len(tags)}")
