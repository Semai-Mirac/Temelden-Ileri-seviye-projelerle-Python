import sqlite3

def create_connection(db_path="customers.db"):
    """Veritabanı bağlantısı oluşturur."""
    try:
        conn = sqlite3.connect(db_path)
        # Verilerin sözlük (dict) formatında alınabilmesi için Row factory kullanıyoruz
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        # Hata durumunda ana akışın yakalayabilmesi için istisna fırlatıyoruz
        raise Exception(f"Veritabanı bağlantı hatası oluştu: {e}")

def fetch_active_customers(conn):
    """Aktif müşterileri veritabanından getirir. (Sadece statüsü aktif olanlar)"""
    try:
        cursor = conn.cursor()
        # Analiz SQL'de değil Python'da olmalı ancak iş mantığı gereği 'active' olanlar alınmalı
        query = """
            SELECT id, name, last_login_days, total_login, status 
            FROM customers 
            WHERE status = 'active'
            ORDER BY id ASC
        """
        cursor.execute(query)
        
        # list of dict yapısı ile döner
        return [dict(row) for row in cursor.fetchall()]
    except sqlite3.Error as e:
        raise Exception(f"Veri çekme işlemi (fetch_active_customers) sırasında SQL hatası: {e}")

def get_risky_customers(customers):
    """Müşteri risk analizi yapar: Son giris 60 gunden buyukse riskli"""
    # List comprehension zorunluluğu karşılanıyor
    return [c for c in customers if c.get('last_login_days', 0) > 60]

def filter_priority_review(customers):
    """Öncelikli inceleme filtresi: Hem riskli hem de düşük etkileşimli (toplam < 10) olanlar"""
    # filter() zorunluluğu karşılanıyor
    priority_customers = filter(
        lambda c: c.get('last_login_days', 0) > 60 and c.get('total_login', 0) < 10, 
        customers
    )
    return list(priority_customers)

def generate_report(active_customers, risky_customers, priority_customers):
    """Bulguları formatlayıp metin olarak rapor üretir."""
    report_lines = []
    report_lines.append("="*55)
    report_lines.append(" MÜŞTERİ SEGMENTASYONU VE DURUM RAPORU")
    report_lines.append("="*55)
    report_lines.append(f"[-] Aktif Müşteri Sayısı    : {len(active_customers)}")
    report_lines.append(f"[-] Riskli Müşteri Sayısı   : {len(risky_customers)}")
    report_lines.append(f"[-] Öncelikli İnceleme      : {len(priority_customers)}")
    
    # Sadece Öncelikli İnceleme Listesi
    report_lines.append("\n[ ÖNCELİKLİ İNCELEME LİSTESİ ]")
    if not priority_customers:
        report_lines.append(" > Öncelikli incelemeye takılan müşteri bulunmamaktadır.")
    else:
        for c in priority_customers:
            report_lines.append(
                f" > ID: {c['id']} | Müşteri: {c['name']:<15} "
                f"(Son Giriş: {c['last_login_days']} gün, Toplam: {c['total_login']} işlem)"
            )
            
    # Tüm Müşterilerin Müşteri Bazlı Durum Raporu
    report_lines.append("\n[ TÜM MÜŞTERİLERİN DURUM DETAYI ]")
    
    priority_ids = [c['id'] for c in priority_customers]
    risky_ids = [c['id'] for c in risky_customers]
    
    for c in active_customers:
        c_id = c['id']
        if c_id in priority_ids:
            status = "ÖNCELİKLİ İNCELEME"
        elif c_id in risky_ids:
            status = "RİSKLİ"
        elif c.get('total_login', 0) < 10:
            status = "DÜŞÜK ETKİLEŞİMLİ"
        else:
            status = "NORMAL"
            
        report_lines.append(f" > ID: {c_id:02d} | Müşteri: {c['name']:<15} | Durum: {status}")
        
    report_lines.append("="*55)
    return "\n".join(report_lines)

def main():
    # Global değişkenler kullanılmamış, tüm durumlar fonksiyonlara paslanmıştır
    conn = None
    try:
        # Gerçek üretim (production) veritabanına bağlanılır
        conn = create_connection("customers.db")
        
        # 1. Aktif müşterileri getir
        active_customers = fetch_active_customers(conn)
        
        # Boş veri/bağlantı anomalisi kontrolü
        if not active_customers:
            print("Uyarı: Veritabanından hiçbir aktif müşteri dönmedi. Bağlantıyı veya 'customers' tablosunu kontrol edin.")
            return
        
        # 2. Mantıksal Filtrelemeler (SQL değil Python tarafında)
        risky_customers = get_risky_customers(active_customers)
        priority_customers = filter_priority_review(active_customers)
        
        # 3. Rapor oluştur
        report_string = generate_report(active_customers, risky_customers, priority_customers)
        
        # print() yalnızca ana akış (main) içinde kullanıldı
        print(report_string)

    except Exception as e:
        # Detaylandırılmış hata mesajı kullanıcıya sunulur
        print(f"\n[!] SİSTEM HATASI: {e}\nLütfen veritabanı ayarlarını ve tabloları kontrol ediniz.")
    finally:
        # Her koşulda bağlantının güvenli bir şekilde kapatıldığından emin olunur
        if conn:
            conn.close()

if __name__ == "__main__":
    main()