import sqlite3
from pathlib import Path

DB_NAME = "school.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            discount_percent INTEGER DEFAULT 0,
            duration_months INTEGER NOT NULL,
            instructor TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()