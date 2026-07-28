import sqlite3

conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

# customers tablosunu oluştur
cursor.execute('''
    CREATE TABLE customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        name TEXT, 
        city TEXT
    )
''')

# Kullanıcıdan kaç müşteri ekleneceğini oku
n = int(input().strip())

# n satır oku, her satır "isim,sehir" formatında
# Her birini tabloya INSERT et
for _ in range(n):
    line = input().strip()
    name, city = line.split(",")
    # Tabloya verileri ekle
    cursor.execute("INSERT INTO customers (name, city) VALUES (?, ?)", (name.strip(), city.strip()))

# Veritabanına kaydet
conn.commit()

# Verileri sorgulama ve yazdırma
cursor.execute("SELECT * FROM customers")
customers = cursor.fetchall()

for row in customers:
    print(f"{row[0]}, {row[1]}, {row[2]}")

print(f"Toplam: {len(customers)} musteri")

conn.close()