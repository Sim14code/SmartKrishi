import sqlite3

# This is the name of the database file that will be created
DB_NAME = "db.sqlite3"

# This sets up the logs table (if it doesn’t exist already)
def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                crop TEXT,
                land_size REAL,
                goal REAL,
                city TEXT,
                language TEXT,
                response TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

# This saves a single interaction into the logs table
def save_log(data):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO logs (crop, land_size, goal, city, language, response)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            data.get("crop"),
            data.get("land_size"),
            data.get("goal"),
            data.get("city"),
            data.get("language"),
            data.get("response")
        ))
        conn.commit()
