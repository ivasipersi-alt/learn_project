import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "school.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
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
            price REAL NOT NULL CHECK(price >= 0),
            duration_months INTEGER NOT NULL CHECK(duration_months > 0),
            instructor TEXT NOT NULL
        )
    """)
    conn.commit()

    total = cursor.execute("SELECT COUNT(*) as total FROM courses").fetchone()["total"]
    if total == 0:
        demo_courses = [
            ("Bарка пельмешек", "Вода, соль, наслаждение", 150000.0, 1, "Мистер Пельмень")
        ]
        cursor.executemany(
            "INSERT INTO courses (title, description, price, duration_months, instructor) VALUES (?, ?, ?, ?, ?)",
            demo_courses
        )
        conn.commit()
    conn.close()