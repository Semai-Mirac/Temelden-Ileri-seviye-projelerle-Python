def komisyon_hesapla(tutar, islem_tipi):
    """TODO: islem_tipi'ne göre komisyonu 2 ondalık basamaklı string olarak döndür."""
    # ipucu:
    # - "havale" için oran 0.01
    # - "eft" için oran 0.005
    # - "kredi" için oran 0.02
    # - diğer tüm tipler için oran 0.0 olmalı
    #
    # komisyon = tutar * oran
    # return f"{komisyon:.2f}"
    
    islem_tipi_clean = islem_tipi.strip().lower()
    
    if islem_tipi_clean == "havale":
        oran = 0.01
    elif islem_tipi_clean == "eft":
        oran = 0.005
    elif islem_tipi_clean == "kredi":
        oran = 0.02
    else:
        oran = 0.0
        
    komisyon = tutar * oran
    return f"{komisyon:.2f}"

if __name__ == "__main__":
    try:
        tutar_girdisi = float(input())
        islem_tipi_girdisi = input()
        
        komisyon_str = komisyon_hesapla(tutar_girdisi, islem_tipi_girdisi)
        print(komisyon_str)
    except ValueError:
        pass