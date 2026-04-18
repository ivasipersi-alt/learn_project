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

    # Заполнение демо-данными
    total = cursor.execute("SELECT COUNT(*) as total FROM courses").fetchone()["total"]
    if total == 0:
        demo_courses = [
            ("Backend на Python", "Изучение FastAPI, Flask и SQL", 15000.0, 4, "Анна Смирнова"),
            ("Frontend Basics", "Основы HTML, CSS и JS", 10000.0, 2, "Иван Иванов"),
            ("DevOps для новичков", "Git, Docker, CI/CD", 18500.0, 3, "Алексей Петров")
        ]
        cursor.executemany(
            "INSERT INTO courses (title, description, price, duration_months, instructor) VALUES (?, ?, ?, ?, ?)",
            demo_courses
        )
        conn.commit()
    conn.close()