import sqlite3

def init_db(db_path: str = "weather.db"):
    """
    Create the SQLite database and the weather_history table if it does not exist.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS weather_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT NOT NULL,
        temperature_celsius REAL NOT NULL,
        humidity INTEGER NOT NULL,
        condition TEXT NOT NULL,
        timestamp TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized at weather.db")