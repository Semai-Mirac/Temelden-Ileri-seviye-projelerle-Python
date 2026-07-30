import sqlite3

conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

# Tablo olustur
cursor.execute("CREATE TABLE accounts (id INTEGER PRIMARY KEY, name TEXT, balance REAL)")


def print_table(cur):
    """Tablodaki tum kayitlari yazdir, bossa 'Tablo bos' yazdir."""
    cur.execute("SELECT * FROM accounts")
    rows = cur.fetchall()
    if not rows:
        print("Tablo bos")
    else:
        for row in rows:
            print(f"{row[0]}, {row[1]}, {row[2]}")


initial_balance = float(input())
updated_balance = float(input())

cursor.execute("INSERT INTO accounts (id, name, balance) VALUES (?, ?, ?)", (1, "Ecem", initial_balance))
conn.commit()

print_table(cursor)
print("---")

cursor.execute("UPDATE accounts SET balance = ? WHERE id = ?", (updated_balance, 1))
conn.commit()

print_table(cursor)
print("---")

cursor.execute("DELETE FROM accounts WHERE id = ?", (1,))
conn.commit()

print_table(cursor)

conn.close()
