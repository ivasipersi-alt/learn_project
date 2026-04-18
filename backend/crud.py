from backend.database import get_connection

def get_all_courses():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM courses ORDER BY id").fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_course_by_id(course_id: int):
    conn = get_connection()
    row = conn.execute("SELECT * FROM courses WHERE id = ?", (course_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

def create_course(course_data: dict):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO courses (title, description, price, duration_months, instructor) VALUES (?, ?, ?, ?, ?)",
        (course_data["title"], course_data.get("description", ""), course_data["price"], course_data["duration_months"], course_data["instructor"])
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return get_course_by_id(new_id)

def update_course(course_id: int, course_data: dict):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE courses SET title=?, description=?, price=?, duration_months=?, instructor=? WHERE id=?",
        (course_data["title"], course_data.get("description", ""), course_data["price"], course_data["duration_months"], course_data["instructor"], course_id)
    )
    conn.commit()
    res = cursor.rowcount
    conn.close()
    return get_course_by_id(course_id) if res > 0 else None

def patch_course(course_id: int, course_data: dict):
    existing = get_course_by_id(course_id)
    if not existing: return None
    updated = {k: course_data.get(k, existing[k]) for k in ["title", "description", "price", "duration_months", "instructor"]}
    return update_course(course_id, updated)

def delete_course(course_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM courses WHERE id = ?", (course_id,))
    conn.commit()
    res = cursor.rowcount
    conn.close()
    return res > 0