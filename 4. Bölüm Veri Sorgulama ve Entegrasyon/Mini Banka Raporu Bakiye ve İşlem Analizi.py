import sqlite3

conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

# Tabloları oluştur
cursor.execute("CREATE TABLE accounts (id INTEGER PRIMARY KEY, name TEXT, balance REAL)")
cursor.execute(
    "CREATE TABLE transactions (id INTEGER PRIMARY KEY, account_id INTEGER, amount REAL, description TEXT)"
)

# Verileri ekle
cursor.executemany(
    "INSERT INTO accounts VALUES (?, ?, ?)",
    [(1, "Ada", 1500.0), (2, "Mert", 3200.0), (3, "Zeynep", 800.0)],
)
cursor.executemany(
    "INSERT INTO transactions VALUES (?, ?, ?, ?)",
    [
        (1, 1, 200.0, "Market"),
        (2, 1, -50.0, "Kargo"),
        (3, 2, 500.0, "Maas"),
        (4, 2, -100.0, "Fatura"),
        (5, 2, -200.0, "Market"),
        (6, 3, 150.0, "Havale"),
    ],
)
conn.commit()

# TODO: 1) Toplam bakiye - SUM(balance) hesapla ve "Toplam bakiye: X" yazdır
cursor.execute("SELECT SUM(balance) FROM accounts")
toplam_bakiye = cursor.fetchone()[0]
print(f"Toplam bakiye: {toplam_bakiye}")

# TODO: 2) En aktif hesap - En çok işlem yapan account_id'yi bul,
#          accounts tablosundan adını çek ve "En aktif hesap: X" yazdır
cursor.execute("""
    SELECT a.name 
    FROM accounts a
    JOIN transactions t ON a.id = t.account_id
    GROUP BY a.id 
    ORDER BY COUNT(t.id) DESC 
    LIMIT 1
""")
en_aktif_hesap = cursor.fetchone()[0]
print(f"En aktif hesap: {en_aktif_hesap}")

# TODO: Kullanıcıdan kaç işlem gösterileceğini oku
n = int(input())

# TODO: 3) Son n işlem - id DESC sıralı ilk n transaction'ı çek
#          ve her birini "description: amount" formatında yazdır
cursor.execute("SELECT description, amount FROM transactions ORDER BY id DESC LIMIT ?", (n,))
rows = cursor.fetchall()
for row in rows:
    print(f"{row[0]}: {row[1]}")

conn.close()
