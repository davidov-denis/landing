import sqlite3


conn = sqlite3.connect("banana.db")
cur = conn.cursor()
data = cur.execute("""SELECT * FROM orders""").fetchall()

cur.close()
conn.close()
for i in data:
    print(i)