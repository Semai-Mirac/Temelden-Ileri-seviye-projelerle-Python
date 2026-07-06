# -*- coding: utf-8 -*-
"""
Finansal Analiz Motoru
Bu modül, kullanıcıların gelir ve gider işlemlerini kaydedip, finansal analizler
ve bakiye takipleri yapmalarını sağlayan bir simülasyon motorudur.
"""

# Tip ipuçları (Type Hints) için standart kütüphaneden gerekli yapıların içe aktarılması
from typing import List, Tuple, Any, Dict


def turkce_kucult_ve_temizle(s: Any) -> str:
    """
    Türkçe karakterleri İngilizce karşılıklarına dönüştürür ve küçük harfe çevirir.
    Unicode birleştirici karakterleri ve büyük/küçük harf dönüştürme uyumsuzluklarını çözer.
    """
    # Gelen parametreyi stringe dönüştürüp başındaki ve sonundaki boşlukları temizler
    text = str(s).strip()
    
    # Türkçe büyük 'İ' ve 'I' harflerini karakter dönüşümü öncesinde manuel olarak değiştirir.
    # Bu adım, bazı sistemlerdeki unicode dönüştürme hatalarını ve veri kayıplarını engellemek için önemlidir.
    text = text.replace('İ', 'i').replace('I', 'ı')
    
    # Tüm metni genel küçük harf haline getirir
    text = text.lower()
    
    # Türkçe noktalı harflerde oluşabilecek ek unicode birleştirici nokta işaretlerini kaldırır
    text = text.replace('\u0307', '')
    
    # Türkçe harflerin İngilizce (ASCII) karakter dönüşüm tablosu (örneğin 'ş' -> 's')
    mapping = {
        'ğ': 'g', 'ü': 'u', 'ş': 's', 'ı': 'i', 'ö': 'o', 'ç': 'c'
    }
    
    # Sözlükteki her bir Türkçe karakteri sırayla İngilizce karşılığı ile değiştirir
    for tr_char, eng_char in mapping.items():
        text = text.replace(tr_char, eng_char)
        
    # Temizlenmiş ve standardize edilmiş metni döndürür
    return text


def islem_ekle_ve_dogrula(islemler: List[Dict[str, Any]], description: str, amount: Any, islem_tipi: str, kategori: str) -> Tuple[bool, str]:
    """
    Yeni bir işlemi doğrular ve geçerliyse listeye ekler.
    
    Parametreler:
        islemler (list): Mevcut işlemler listesi.
        description (str): İşlem açıklaması.
        amount (any): İşlem tutarı (pozitif olmalıdır).
        islem_tipi (str): 'gelir' veya 'gider'.
        kategori (str): 'sabit' veya 'degisken'.
        
    Geri Dönüş:
        tuple: (durum (bool), mesaj (str))
    """
    # Girilen açıklamanın boş olup olmadığını ve sadece boşluktan ibaret olup olmadığını kontrol eder
    if not description or not str(description).strip():
        return False, "Hata: Açıklama alanı boş bırakılamaz."
    
    # Girilen tutarın geçerli bir ondalıklı (float) sayıya dönüştürülebilir olup olmadığını doğrular
    try:
        # Kullanıcının ondalık ayırıcı olarak virgül (,) yazması durumunda bunu noktaya (.) çevirir
        amount_clean = str(amount).replace(",", ".")
        tutar_float = float(amount_clean)
    except (ValueError, TypeError):
        # Dönüştürme başarısız olursa (örneğin kullanıcı harf girerse) hata mesajı döndürür
        return False, "Hata: Tutar geçerli bir sayı olmalıdır."
    
    # İşlem tutarının sıfırdan büyük (pozitif) olup olmadığını kontrol eder
    if tutar_float <= 0:
        return False, "Hata: Tutar sıfırdan büyük (pozitif) olmalıdır."
        
    # İşlem tipini Türkçe karakterlerden ve büyük harflerden arındırır
    islem_tipi_temiz = turkce_kucult_ve_temizle(islem_tipi)
    # Sadece belirlenen "gelir" veya "gider" türlerinin seçilmesini şart koşar
    if islem_tipi_temiz not in ["gelir", "gider"]:
        return False, "Hata: İşlem tipi yalnızca 'gelir' veya 'gider' olabilir."
        
    # Kategori ismini standartlaştırır ve temizler
    kategori_temiz = turkce_kucult_ve_temizle(kategori)

    # İşletme kurallarına göre kategori ve işlem tipi uyumluluğunu denetler
    if islem_tipi_temiz == "gelir":
        # Gelir işlemleri finansal kural gereğince sadece 'sabit' olabilir
        if kategori_temiz != "sabit":
            return False, "Hata: Gelir işlemleri için kategori zorunlu olarak 'sabit' olmalıdır."
    else:  # gider
        # Gider işlemleri ise sadece 'sabit' veya 'degisken' olabilir
        if kategori_temiz not in ["sabit", "degisken"]:
            return False, "Hata: Gider işlemleri için kategori yalnızca 'sabit' veya 'degisken' olabilir."
            
    # Mükerrer veri eklenmesini önlemek için ardışık aynı işlem kontrolü yapar
    if islemler:
        # Son eklenen işlemi alır
        son_islem = islemler[-1]
        # Eğer yeni eklenmek istenen açıklama ve tip bir önceki ile tamamen aynıysa eklemeyi engeller
        if (son_islem["description"].strip().lower() == str(description).strip().lower() and 
            son_islem["type"] == islem_tipi_temiz):
            return False, f"Hata: Arka arkaya aynı açıklama ('{description.strip()}') ve işlem tipi ('{islem_tipi_temiz}') kombinasyonu eklenemez."
            
    # Tüm kural ve doğrulama aşamaları geçildiyse yeni işlem sözlüğünü oluşturur
    yeni_islem = {
        "description": str(description).strip(),
        "amount": tutar_float,
        "type": islem_tipi_temiz,
        "category": kategori_temiz
    }
    # Yeni işlemi mevcut işlemler listesine ekler
    islemler.append(yeni_islem)
    return True, "İşlem başarıyla eklendi."


def gelir_gider_ayristir(islemler: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    İşlemleri gelirler ve giderler olarak iki gruba ayırır.
    
    Geri Dönüş:
        tuple: (gelirler (list), giderler (list))
    """
    # List comprehension (liste kavrayışı) kullanarak tipi 'gelir' olan işlemler filtrelenir
    gelirler = [islem for islem in islemler if islem["type"] == "gelir"]
    # List comprehension (liste kavrayışı) kullanarak tipi 'gider' olan işlemler filtrelenir
    giderler = [islem for islem in islemler if islem["type"] == "gider"]
    # Filtrelenmiş listeleri tuple olarak döndürür
    return gelirler, giderler


def toplam_gelir_gider_hesapla(islemler: List[Dict[str, Any]]) -> Tuple[float, float]:
    """
    Toplam gelir ve toplam gider tutarlarını hesaplar.
    
    Geri Dönüş:
        tuple: (toplam_gelir (float), toplam_gider (float))
    """
    # Gelir ve giderleri ayıklamak için ilgili fonksiyon çağrılır
    gelirler, giderler = gelir_gider_ayristir(islemler)
    # Gelir listesindeki tüm tutarlar sum fonksiyonu ve üreteç ifadesi ile toplanır
    toplam_gelir = sum(islem["amount"] for islem in gelirler)
    # Gider listesindeki tüm tutarlar sum fonksiyonu ile toplanır
    toplam_gider = sum(islem["amount"] for islem in giderler)
    return toplam_gelir, toplam_gider


def net_bakiye_hesapla(toplam_gelir: float, toplam_gider: float) -> float:
    """
    Net bakiyeyi hesaplar (Gelir - Gider).
    
    Geri Dönüş:
        float: net_bakiye
    """
    # Toplam gelirden toplam gider çıkarılarak kalan net bakiye bulunur
    return toplam_gelir - toplam_gider


def kategori_bazli_gider_topla(islemler: List[Dict[str, Any]]) -> Tuple[float, float]:
    """
    Giderlerin sabit ve değişken kategorilerine göre toplamlarını hesaplar.
    
    Geri Dönüş:
        tuple: (sabit_gider_toplami (float), degisken_gider_toplami (float))
    """
    # İşlemler arasından sadece gider olanları elde eder (gelirler göz ardı edilir)
    _, giderler = gelir_gider_ayristir(islemler)
    # Kategorisi 'sabit' olan giderlerin toplam tutarı hesaplanır
    sabit_gider_toplami = sum(islem["amount"] for islem in giderler if islem["category"] == "sabit")
    # Kategorisi 'degisken' olan giderlerin toplam tutarı hesaplanır
    degisken_gider_toplami = sum(islem["amount"] for islem in giderler if islem["category"] == "degisken")
    return sabit_gider_toplami, degisken_gider_toplami


def finansal_durum_degerlendir(toplam_gelir: float, toplam_gider: float, degisken_gider: float) -> str:
    """
    Finansal durumu kurallara göre değerlendirir.
    
    Kurallar:
    - Net bakiye < 0 ise "Riskli"
    - Değişken gider / gelir > %40 ise "Kontrol Edilmeli"
    - Diğer durumlar "Sağlıklı"
    
    Geri Dönüş:
        str: "Riskli" | "Kontrol Edilmeli" | "Sağlıklı"
    """
    # Güncel net bakiyeyi hesaplar
    net_bakiye = net_bakiye_hesapla(toplam_gelir, toplam_gider)
    
    # Harcamalar geliri aştıysa durum 'Riskli' olarak tanımlanır
    if net_bakiye < 0:
        return "Riskli"
    
    # Gelir sıfırdan büyükse ve esnek (değişken) harcamalar toplam gelirin %40'ından fazlaysa uyarı verilir
    if toplam_gelir > 0 and (degisken_gider / toplam_gelir) > 0.40:
        return "Kontrol Edilmeli"
        
    # Bakiye pozitif ve harcama dengesi idealse durum 'Sağlıklı' olarak tanımlanır
    return "Sağlıklı"


def main() -> None:
    # Program boyunca tüm finansal verileri tutacak ana işlem listesi
    islemler = []
    
    # Kullanıcı çıkış seçeneğini (5) seçene kadar çalışan sonsuz menü döngüsü
    while True:
        # Menü arayüzü çizimi
        print("\n" + "="*45)
        print("         FİNANSAL ANALİZ MOTORU")
        print("="*45)
        print("1. Yeni İşlem Ekle")
        print("2. Finansal Özet Göster")
        print("3. Tüm İşlemleri Listele")
        print("4. Hazır Örnek İşlemleri Yükle")
        print("5. Çıkış")
        print("-"*45)
        
        # Kullanıcıdan menü tercihi alma ve olası boşlukları temizleme
        secim = input("Lütfen yapmak istediğiniz işlemi seçin (1-5): ").strip()
        
        # --- 1. SEÇENEK: Yeni İşlem Ekleme ---
        if secim == "1":
            print("\n--- Yeni İşlem Ekleme ---")
            aciklama = input("İşlem Açıklaması (örn. Maaş, Kira, Market): ")
            tutar_raw = input("Tutar (pozitif sayı): ")
            islem_tipi = input("İşlem Tipi (gelir / gider): ")
            kategori = input("Kategori (sabit / degisken): ")
            
            # Girilen verileri doğrulama ve listeye ekleme fonksiyonuna gönderir
            basari, mesaj = islem_ekle_ve_dogrula(islemler, aciklama, tutar_raw, islem_tipi, kategori)
            if basari:
                print(f"\n[BAŞARILI] {mesaj}")
            else:
                print(f"\n[HATA] İşlem eklenemedi! Nedeni: {mesaj}")
                
        # --- 2. SEÇENEK: Finansal Rapor Gösterimi ---
        elif secim == "2":
            # İşlem listesi boşken raporlama yapılmayacağını bildirir
            if not islemler:
                print("\n[BİLGİ] Henüz kayıtlı işlem bulunmamaktadır. Özet gösterilemez.")
                continue
                
            # Finansal metrikleri hesaplama fonksiyonları üzerinden alır
            toplam_gelir, toplam_gider = toplam_gelir_gider_hesapla(islemler)
            net_bakiye = net_bakiye_hesapla(toplam_gelir, toplam_gider)
            sabit_gider, degisken_gider = kategori_bazli_gider_topla(islemler)
            durum = finansal_durum_degerlendir(toplam_gelir, toplam_gider, degisken_gider)
            
            # Raporun ekrana yazdırılması (Binlik ayraçlı ve 2 ondalık basamaklı f-string biçimlendirmesiyle)
            print("\n" + "*"*45)
            print("            FİNANSAL ÖZET RAPORU")
            print("*"*45)
            print(f"Toplam Gelir         : {toplam_gelir:,.2f} TL")
            print(f"Toplam Gider         : {toplam_gider:,.2f} TL")
            print(f"Net Bakiye           : {net_bakiye:,.2f} TL")
            print("-"*45)
            print("Kategori Bazlı Giderler:")
            print(f" - Sabit Giderler    : {sabit_gider:,.2f} TL")
            print(f" - Değişken Giderler : {degisken_gider:,.2f} TL")
            print("-"*45)
            
            # Değişken giderlerin gelire oranını hesaplayıp yüzde olarak gösterir
            if toplam_gelir > 0:
                oran_yuzde = (degisken_gider / toplam_gelir) * 100
                print(f"Değişken Gider / Gelir Oranı: %{oran_yuzde:.1f}")
            else:
                print("Değişken Gider / Gelir Oranı: Belirlenemiyor (Gelir 0)")
                
            print(f"Finansal Durum Yorumu: {durum}")
            print("*"*45)
            
        # --- 3. SEÇENEK: Tüm İşlemleri Tablo Olarak Listeleme ---
        elif secim == "3":
            if not islemler:
                print("\n[BİLGİ] Kayıtlı işlem bulunmamaktadır.")
                continue
                
            # Hizalanmış tablo başlıklarını yazdırır
            print("\n" + "-"*66)
            print(f"{'No':<4} | {'Açıklama':<20} | {'Tutar':<12} | {'Tip':<8} | {'Kategori':<10}")
            print("-"*66)
            # Tüm işlemleri indeks numarasıyla beraber döngüye sokar (1'den başlatır)
            for i, islem in enumerate(islemler, 1):
                desc = islem['description']
                # Tablo görsel düzeninin bozulmaması için çok uzun açıklamaları 17. karakterde kesip "..." ekler
                desc_gosterim = desc[:17] + "..." if len(desc) > 20 else desc
                # Sütun hizalamalarıyla satırı ekrana basar
                print(f"{i:<4} | {desc_gosterim:<20} | {islem['amount']:<12,.2f} | {islem['type']:<8} | {islem['category']:<10}")
            print("-"*66)
            
        # --- 4. SEÇENEK: Hazır Örnek Senaryo Yükleme ---
        elif secim == "4":
            # Hızlı test ve analiz için önceden tanımlanmış finansal işlemler listesi
            ornekler = [
                ("Maaş", 30000, "gelir", "sabit"),
                ("Kira", 12000, "gider", "sabit"),
                ("Market", 4000, "gider", "degisken"),
                ("Fatura", 2000, "gider", "sabit"),
                ("Dışarıda Yemek", 3000, "gider", "degisken")
            ]
            print("\n--- Örnek Veriler Yükleniyor ---")
            yuklenen = 0
            # Her bir örnek işlem elemanını teker teker doğrulayarak eklemeyi dener
            for aciklama, tutar, islem_tipi, kategori in ornekler:
                basari, mesaj = islem_ekle_ve_dogrula(islemler, aciklama, tutar, islem_tipi, kategori)
                if basari:
                    print(f"Eklendi: {aciklama} ({tutar} TL, {islem_tipi}, {kategori})")
                    yuklenen += 1
                else:
                    print(f"Hata ({aciklama}): {mesaj}")
            print(f"\n{yuklenen} adet örnek veri başarıyla yüklendi.")
            
        # --- 5. SEÇENEK: Uygulamadan Çıkış ---
        elif secim == "5":
            print("\nFinansal Analiz Motorundan çıkılıyor. İyi günler dileriz!")
            break # Sonsuz while döngüsünü kırarak programı sonlandırır
            
        # --- HATALI GİRİŞ: 1-5 dışındaki girdiler ---
        else:
            print("\n[HATA] Geçersiz seçim! Lütfen 1 ile 5 arasında bir sayı girin.")


# Programın terminal üzerinden interaktif olarak çalıştırılmasını sağlayan ana giriş noktası
if __name__ == "__main__":
    main()
