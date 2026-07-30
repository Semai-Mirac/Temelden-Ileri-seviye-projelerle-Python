import sqlite3

conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

cursor.execute("CREATE TABLE accounts (id INTEGER PRIMARY KEY, name TEXT, balance REAL)")

accounts = [
    (1, "Ecem", 1500.0),
    (2, "Terzioğlu", 8800.0),
    (3, "Semai", 3200.0),
    (4, "Miraç", 450.0),
]
cursor.executemany("INSERT INTO accounts (id, name, balance) VALUES (?, ?, ?)", accounts)

conn.commit()

min_balance = float(input())

cursor.execute("SELECT id, name, balance FROM accounts WHERE balance >= ?", (min_balance,))
rows = cursor.fetchall()

for row in rows:
    print(f"{row[0]}, {row[1]}, {row[2]}")

conn.close()
