from backend.database import get_connection


def _format_course(row):
    if not row: return None
    course = dict(row)
    price = course.get('price', 0.0)
    discount = course.get('discount_percent', 0)
    course['final_price'] = round(price * (1 - discount / 100), 2)
    return course


def get_all_courses(filter_type: str = None):
    conn = get_connection()
    if filter_type == 'free':
        query = "SELECT * FROM courses WHERE price = 0 OR discount_percent = 100"
    elif filter_type == 'paid':
        query = "SELECT * FROM courses WHERE price > 0 AND discount_percent < 100"
    else:
        query = "SELECT * FROM courses"

    rows = conn.execute(query).fetchall()
    conn.close()
    return [_format_course(row) for row in rows]


def get_course_by_id(course_id: int):
    conn = get_connection()
    row = conn.execute("SELECT * FROM courses WHERE id = ?", (course_id,)).fetchone()
    conn.close()
    return _format_course(row)


def create_course(data: dict):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO courses (title, description, price, discount_percent, duration_months, instructor) VALUES (?, ?, ?, ?, ?, ?)",
        (data["title"], data["description"], data["price"], data.get("discount_percent", 0), data["duration_months"],
         data["instructor"])
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id


def update_course(course_id: int, data: dict):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE courses SET title=?, description=?, price=?, discount_percent=?, duration_months=?, instructor=? WHERE id=?",
        (data["title"], data["description"], data["price"], data.get("discount_percent", 0), data["duration_months"],
         data["instructor"], course_id)
    )
    conn.commit()
    res = cursor.rowcount
    conn.close()
    return get_course_by_id(course_id) if res > 0 else None


def patch_course(course_id: int, data: dict):
    existing = get_course_by_id(course_id)
    if not existing: return None
    updated = {k: data.get(k, existing[k]) for k in
               ["title", "description", "price", "discount_percent", "duration_months", "instructor"]}
    return update_course(course_id, updated)


def delete_course(course_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM courses WHERE id=?", (course_id,))
    conn.commit()
    conn.close()
