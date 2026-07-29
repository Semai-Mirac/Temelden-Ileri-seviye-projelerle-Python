import sqlite3

# In-memory veritabani baglantisi olustur
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

# accounts tablosunu olustur (id INTEGER PRIMARY KEY, iban TEXT, balance REAL)
cursor.execute("""
    CREATE TABLE accounts (
        id INTEGER PRIMARY KEY,
        iban TEXT,
        balance REAL
    )
""")

# 3 hesap ekle: (1,'TR001',1500.0), (2,'TR002',3200.0), (3,'TR003',750.0)
accounts = [
    (1, "TR001", 1500.0),
    (2, "TR002", 3200.0),
    (3, "TR003", 750.0),
]
cursor.executemany("INSERT INTO accounts (id, iban, balance) VALUES (?, ?, ?)", accounts)

conn.commit()

# Kullanicidan minimum bakiye degerini oku
min_balance = float(input())

# balance >= min_balance olan hesaplari SELECT ile cek (parametreli sorgu kullan)
cursor.execute("SELECT id, iban, balance FROM accounts WHERE balance >= ?", (min_balance,))
rows = cursor.fetchall()

# Sonuclari "id, iban, balance" formatinda yazdir
for row in rows:
    print(f"{row[0]}, {row[1]}, {row[2]}")

conn.close()
