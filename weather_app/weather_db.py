import sqlite3
from datetime import datetime
from typing import Optional, List, Dict

def get_connection(db_path: str = "weather.db") -> sqlite3.Connection:
    """
    Return a sqlite3 connection with Row factory so we can convert rows to dicts easily.
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def insert_weather(city: str, temperature_celsius: float, humidity: int, condition: str, db_path: str = "weather.db") -> int:
    """
    Insert a weather record into weather_history.
    Returns the new record id.
    """
    conn = get_connection(db_path)
    cur = conn.cursor()
    timestamp = datetime.utcnow().isoformat()
    cur.execute("""
        INSERT INTO weather_history (city, temperature_celsius, humidity, condition, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (city, temperature_celsius, humidity, condition, timestamp))
    conn.commit()
    rowid = cur.lastrowid
    conn.close()
    return rowid

def get_latest_weather(city: str, db_path: str = "weather.db") -> Optional[Dict]:
    """
    Return the latest weather record for the given city or None if not found.
    """
    conn = get_connection(db_path)
    cur = conn.cursor()
    cur.execute("""
        SELECT id, city, temperature_celsius, humidity, condition, timestamp
        FROM weather_history
        WHERE city = ?
        ORDER BY timestamp DESC
        LIMIT 1
    """, (city,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None

def get_weather_history(city: str, limit: int = 100, db_path: str = "weather.db") -> List[Dict]:
    """
    Return a list of weather records for the given city ordered by newest first.
    """
    conn = get_connection(db_path)
    cur = conn.cursor()
    cur.execute("""
        SELECT id, city, temperature_celsius, humidity, condition, timestamp
        FROM weather_history
        WHERE city = ?
        ORDER BY timestamp DESC
        LIMIT ?
    """, (city, limit))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def update_weather(record_id: int, temperature_celsius: Optional[float] = None, humidity: Optional[int] = None, condition: Optional[str] = None, db_path: str = "weather.db") -> bool:
    """
    Update provided fields for a weather record by id.
    Returns True if a row was updated, False otherwise.
    """
    fields = []
    params = []
    if temperature_celsius is not None:
        fields.append("temperature_celsius = ?")
        params.append(temperature_celsius)
    if humidity is not None:
        fields.append("humidity = ?")
        params.append(humidity)
    if condition is not None:
        fields.append("condition = ?")
        params.append(condition)

    if not fields:
        # nothing to update
        return False

    params.append(record_id)
    sql = f"UPDATE weather_history SET {', '.join(fields)} WHERE id = ?"

    conn = get_connection(db_path)
    cur = conn.cursor()
    cur.execute(sql, tuple(params))
    conn.commit()
    updated = cur.rowcount > 0
    conn.close()
    return updated

def delete_weather(record_id: int, db_path: str = "weather.db") -> bool:
    """
    Delete a weather record by id. Returns True if a row was deleted.
    """
    conn = get_connection(db_path)
    cur = conn.cursor()
    cur.execute("DELETE FROM weather_history WHERE id = ?", (record_id,))
    conn.commit()
    deleted = cur.rowcount > 0
    conn.close()
    return deleted
