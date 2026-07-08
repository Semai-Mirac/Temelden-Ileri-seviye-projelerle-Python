import json
import os

# Verilerin kalıcı olarak saklanacağı JSON dosyasının varsayılan konumu.
DEFAULT_DATA_FILE = os.path.join(os.path.dirname(__file__), "izleme_listesi.json") if __file__ else "izleme_listesi.json"

# =====================================================================
# 1. VERİ ERİŞİMİ VE KALICI DEPOLAMA (Dependency Injection Uygulandı)
# =====================================================================

def verileri_yukle(dosya_yolu=DEFAULT_DATA_FILE):
    """
    Belirtilen JSON dosyasından önceden kaydedilmiş izleme listesi verilerini yükler.
    'dosya_yolu' parametresi dışarıdan enjekte edilerek (Dependency Injection) test edilebilirlik artırılmıştır.
    """
    if os.path.exists(dosya_yolu):
        try:
            with open(dosya_yolu, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def verileri_kaydet(liste, dosya_yolu=DEFAULT_DATA_FILE):
    """
    Mevcut izleme listesini belirtilen JSON dosyası konumuna kalıcı olarak kaydeder.
    """
    try:
        with open(dosya_yolu, "w", encoding="utf-8") as f:
            json.dump(liste, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"Hata: Veriler kaydedilemedi: {e}")
        return False

# =====================================================================
# 2. İŞ MANTIĞI VE VALIDASYON FONKSİYONLARI (Core Logic)
# =====================================================================

def icerik_ekle(liste, title, content_type, status, rating=None, note="", dosya_yolu=DEFAULT_DATA_FILE):
    """
    Yeni bir dizi/film içeriği ekler ve validasyonları yapar.
    Hata durumunda (False, hata_mesaji), başarı durumunda (True, basari_mesaji) döner.
    """
    title = title.strip()
    if not title:
        return False, "Hata: İçerik adı boş bırakılamaz!"
        
    # Başlığın benzersiz olması gerekir (Büyük/küçük harf duyarsız)
    for icerik in liste:
        if icerik["title"].lower() == title.lower():
            return False, f"Hata: '{title}' adlı içerik zaten listenizde mevcut!"

    content_type = content_type.strip().lower()
    if content_type not in ["film", "dizi"]:
        return False, "Hata: Tür sadece 'film' veya 'dizi' olabilir!"

    status = status.strip().lower()
    if status not in ["izlendi", "izlenecek"]:
        return False, "Hata: Durum sadece 'izlendi' veya 'izlenecek' olabilir!"

    if status == "izlenecek":
        if rating is not None:
            return False, "Hata: Durumu 'izlenecek' olan içeriklere puan verilemez!"
        rating_value = None
    else:  # status == "izlendi"
        if rating is None:
            return False, "Hata: Durumu 'izlendi' olan içerikler için puan (1-10) verilmesi zorunludur!"
        try:
            rating_value = float(rating)
            if not (1 <= rating_value <= 10):
                return False, "Hata: Puan 1 ile 10 arasında bir sayı olmalıdır!"
            if rating_value.is_integer():
                rating_value = int(rating_value)
        except (ValueError, TypeError):
            return False, "Hata: Puan geçerli bir sayı olmalıdır!"

    note = note.strip() if note else ""
    if len(note) > 200:
        return False, f"Hata: Açıklama notu en fazla 200 karakter olabilir! (Mevcut: {len(note)} karakter)"

    yeni_kayit = {
        "title": title,
        "type": content_type,
        "status": status,
        "rating": rating_value,
        "note": note
    }
    
    liste.append(yeni_kayit)
    # Bağımlılık olarak verilen dosya yoluna verileri kalıcı kaydederiz
    verileri_kaydet(liste, dosya_yolu)
    return True, f"Tebrikler! '{title}' başarıyla listenize eklendi."

def basliga_gore_ara(liste, arama_ifadesi):
    """
    Başlığa göre büyük/küçük harf duyarsız arama yapar.
    """
    arama_ifadesi = arama_ifadesi.strip().lower()
    if not arama_ifadesi:
        return []
    
    return [icerik for icerik in liste if arama_ifadesi in icerik["title"].lower()]

def izlenenleri_listele(liste):
    """
    Durumu 'izlendi' olan tüm içerikleri döndürür.
    """
    return [icerik for icerik in liste if icerik["status"] == "izlendi"]

def ortalama_puan_hesapla(liste):
    """
    Sadece rating değeri olan içeriklerin matematiksel ortalama puanını hesaplar.
    """
    puanli_icerikler = [icerik["rating"] for icerik in liste if icerik["rating"] is not None]
    if not puanli_icerikler:
        return None
    return sum(puanli_icerikler) / len(puanli_icerikler)

# =====================================================================
# 3. GÖRSEL SUNUM VE TABLOLAMA (Dinamik Sütun Genişliği Uygulandı)
# =====================================================================

def tablo_olustur(icerikler):
    """
    Gösterilecek içerikleri sütun genişliklerini dinamik olarak hesaplayarak
    ekrana son derece şık, çizgisel ve hizalı bir tablo yapısında yazdırır.
    """
    if not icerikler:
        print("\n--- Gösterilecek içerik bulunamadı ---")
        return

    # Sütun başlıkları ve varsayılan etiketleri tanımlıyoruz
    headers = {
        "title": "İçerik Adı",
        "type": "Tür",
        "status": "Durum",
        "rating": "Puan",
        "note": "Not"
    }

    # Dinamik kolon genişliği hesaplama: Her kolonun başlık ve değerlerinden maksimum uzunluğu buluruz
    widths = {
        "title": max(len(headers["title"]), max(len(i["title"]) for i in icerikler)),
        "type": max(len(headers["type"]), max(len(i["type"]) for i in icerikler)),
        "status": max(len(headers["status"]), max(len(i["status"]) for i in icerikler)),
        "rating": max(len(headers["rating"]), max(len(str(i["rating"] if i["rating"] is not None else "-")) for i in icerikler)),
        "note": max(len(headers["note"]), max(len(i["note"] if i["note"] else "-") for i in icerikler))
    }

    # Not alanının sütunu tablonun çok genişleyip ekrandan taşmaması için maksimum 50 karakterle sınırlandırılır
    if widths["note"] > 50:
         widths["note"] = 50

    # Toplam şerit çizgi uzunluğu (Sütunlar arasındaki ' | ' dikey çizgileri ve kenar boşlukları dahil)
    total_width = sum(widths.values()) + (3 * (len(widths) - 1)) + 4

    print("-" * total_width)
    # Sütun Başlıkları
    print(f"| {headers['title']:<{widths['title']}} | {headers['type'].capitalize():<{widths['type']}} | {headers['status'].capitalize():<{widths['status']}} | {headers['rating']:<{widths['rating']}} | {headers['note']:<{widths['note']}} |")
    print("-" * total_width)
    
    # Satır Verileri
    for icerik in icerikler:
        puan = str(icerik['rating']) if icerik['rating'] is not None else "-"
        not_alani = icerik['note'] if icerik['note'] else "-"
        
        # Eğer not alanı sınırlandırdığımız dinamik not sütun genişliğinden uzunsa kesip üç nokta koyarız
        if len(not_alani) > widths["note"]:
             not_alani = not_alani[:widths["note"] - 3] + "..."
            
        print(f"| {icerik['title']:<{widths['title']}} | {icerik['type'].capitalize():<{widths['type']}} | {icerik['status'].capitalize():<{widths['status']}} | {puan:<{widths['rating']}} | {not_alani:<{widths['note']}} |")
    print("-" * total_width)

# =====================================================================
# 4. KULLANICI ETKİLEŞİM KATMANI (Tekrarlayan input() Kodları Fonksiyonlaştırıldı)
# =====================================================================

def input_baslik(liste):
    """Kullanıcıdan geçerli ve benzersiz bir başlık girişi alır."""
    while True:
        title = input("İçerik Adı: ").strip()
        if not title:
            print("Hata: İçerik adı boş bırakılamaz!")
            continue
        # Başlık benzersizlik kontrolünü kullanıcı yazarken hızlı bildirmek için burada da doğrularız
        if any(icerik["title"].lower() == title.lower() for icerik in liste):
            print(f"Hata: '{title}' adlı içerik zaten listenizde mevcut!")
            continue
        return title

def input_secenek(mesaj, gecerli_secenekler):
    """Kullanıcıdan önceden tanımlanmış seçenekler dahilinde bir giriş almayı zorunlu kılar (örn: film/dizi)."""
    secenek_str = " / ".join(gecerli_secenekler)
    while True:
        deger = input(f"{mesaj} ({secenek_str}): ").strip().lower()
        if deger in gecerli_secenekler:
            return deger
        print(f"Hata: Lütfen geçerli bir seçim yazın ({secenek_str}).")

def input_puan(status):
    """Eğer içerik 'izlendi' durumundaysa kullanıcıdan 1-10 arası geçerli puan alır."""
    if status != "izlendi":
        return None
        
    while True:
        rating_input = input("Puan (1-10 arası): ").strip()
        try:
            rating = float(rating_input)
            if 1 <= rating <= 10:
                return rating
            print("Hata: Puan 1 ile 10 arasında bir sayı olmalıdır!")
        except ValueError:
            print("Hata: Lütfen geçerli bir sayısal değer girin!")

def input_not(maks_karakter=200):
    """Kullanıcıdan sınırlandırılmış karakter boyutunda açıklamalı bir not alır."""
    while True:
        note = input("Özel Not (Opsiyonel, maks 200 karakter): ").strip()
        if len(note) > maks_karakter:
            print(f"Hata: Açıklama notu en fazla {maks_karakter} karakter olabilir! (Mevcut: {len(note)} karakter)")
            continue
        return note

# =====================================================================
# 5. MENÜ SEÇENEK AKSİYONLARI (Single Responsibility Sorumlulukları Dağıtıldı)
# =====================================================================

def menu_yeni_icerik_ekle(liste):
    """Yeni içerik ekleme akışını ve kullanıcı bilgi istemlerini yönetir."""
    print("\n>>> YENİ İÇERİK EKLEME")
    title = input_baslik(liste)
    content_type = input_secenek("Tür", ["film", "dizi"])
    status = input_secenek("Durum", ["izlendi", "izlenecek"])
    rating = input_puan(status)
    note = input_not()
    
    basarili, mesaj = icerik_ekle(liste, title, content_type, status, rating, note)
    print("\n" + mesaj)

def menu_icerik_ara(liste):
    """Arama motoru akışını ve görsel listenmesini sağlar."""
    print("\n>>> BAŞLIĞA GÖRE İÇERİK ARAMA")
    arama_ifadesi = input("Aramak istediğiniz başlık veya kelime: ").strip()
    sonuclar = basliga_gore_ara(liste, arama_ifadesi)
    print(f"\nArama Sonucu: {len(sonuclar)} eşleşen kayıt bulundu.")
    tablo_olustur(sonuclar)

def menu_izlenenleri_goster(liste):
    """Sadece izlenmiş içerikleri tablolayarak listeler."""
    print("\n>>> İZLENEN İÇERİKLERİNİZ")
    izlenenler = izlenenleri_listele(liste)
    print(f"\nToplam {len(izlenenler)} izlenen içerik bulundu.")
    tablo_olustur(izlenenler)

def menu_tum_listeyi_goster(liste):
    """Kullanıcının veri tabanındaki tüm izleme arşivini tablolayarak gösterir."""
    print("\n>>> TÜM İZLEME LİSTENİZ")
    print(f"Toplam {len(liste)} içerik bulunuyor.")
    tablo_olustur(liste)

def menu_ortalama_puan_goster(liste):
    """Puanlama istatistiklerini hesaplayıp ortalamayı ekrana yazar."""
    print("\n>>> ORTALAMA PUAN")
    ort_puan = ortalama_puan_hesapla(liste)
    if ort_puan is None:
        print("Listenizde henüz puanlanmış (izlenmiş) bir içerik bulunmuyor.")
    else:
        print(f"Puanlanmış içeriklerinizin genel ortalaması: {ort_puan:.2f} / 10")

# =====================================================================
# 6. ANA MENÜ AKIŞI (Seçim Yönlendirici)
# =====================================================================

def ana_menu():
    """
    Sistemin ana kontrol merkezidir. İş mantıklarına bölünen parçaları
    koordineli bir şekilde çağırarak döngüyü sürdürür.
    """
    print("\n" + "="*50)
    print("   🎬 DİZİ & FİLM TAKİP SİSTEMİNE HOŞ GELDİNİZ 🍿")
    print("="*50)
    
    # Varsayılan konuma bağımlı olarak verileri yüklüyoruz.
    liste = verileri_yukle()
    
    # Menü eylem eşlemeleri (Dictionary mapping ile kodun karmaşıklığı düşürülmüştür)
    eylemler = {
        "1": lambda: menu_yeni_icerik_ekle(liste),
        "2": lambda: menu_icerik_ara(liste),
        "3": lambda: menu_izlenenleri_goster(liste),
        "4": lambda: menu_tum_listeyi_goster(liste),
        "5": lambda: menu_ortalama_puan_goster(liste)
    }
    
    while True:
        print("\n--- MENÜ ---")
        print("1. Yeni İçerik Ekle")
        print("2. İçerik Ara (Başlığa Göre)")
        print("3. İzlenen İçerikleri Listele")
        print("4. Tüm Listenizi Göster")
        print("5. Ortalama Puanı Hesapla")
        print("6. Çıkış")
        print("-" * 12)
        
        secim = input("Lütfen yapmak istediğiniz işlemin numarasını girin (1-6): ").strip()
        
        if secim in eylemler:
            eylemler[secim]()
        elif secim == "6":
            print("\nSistemden çıkış yapılıyor... İyi seyirler dileriz! 🎬🍿")
            break
        else:
            print("\nHatalı Seçim! Lütfen 1 ile 6 arasında geçerli bir numara girin.")

if __name__ == '__main__':
    ana_menu()
