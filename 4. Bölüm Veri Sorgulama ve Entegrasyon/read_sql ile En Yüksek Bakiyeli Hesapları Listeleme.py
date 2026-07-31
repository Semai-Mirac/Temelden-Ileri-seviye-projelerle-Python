import sqlite3
import pandas as pd

conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

cursor.execute("CREATE TABLE accounts (id INTEGER PRIMARY KEY, name TEXT, balance REAL)")
cursor.executemany(
    "INSERT INTO accounts VALUES (?, ?, ?)",
    [
        (1, "Ecem", 1500.0),
        (2, "Terzioğlu", 800.0),
        (3, "Zehra Nur", 5200.0),
        (4, "Zerrin", 3100.0),
        (5, "Hatice", 4700.0),
    ],
)
conn.commit()

# read_sql ile tüm veriyi DataFrame'e al
df = pd.read_sql("SELECT * FROM accounts", conn)

# balance sütununa göre azalan sırala
df = df.sort_values("balance", ascending=False)

# İlk 3 satırı al
top3 = df.head(3)

# Her satırı "name: balance" formatında yazdır
for _, row in top3.iterrows():
    print(f"{row['name']}: {row['balance']}")

conn.close()
