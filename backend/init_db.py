
import sqlite3

conn = sqlite3.connect("users.db")
cur = conn.cursor()
cur.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
''')
conn.commit()
conn.close()
print("Database initialized.")
