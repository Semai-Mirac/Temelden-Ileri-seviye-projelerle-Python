musteriler = {
    1001: {"ad": "Ada Yılmaz", "segment": "Bireysel"},
    1002: {"ad": "Mert Kaya", "segment": "Ticari"},
}

musteri_no = int(input())

musteri = musteriler.get(musteri_no)

if musteri:
    print(f"{musteri['ad']} - {musteri['segment']}")
else:
    print("Müşteri bulunamadı")
