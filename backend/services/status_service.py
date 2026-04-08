def get_status_data():
    return {
        "status": "ok",
        "message": "Backend работает",
        "service": "backend-service",
        "items_count": 3
    }
def get_items_data():
    return [
        {"id": 1, "name": "Человек белый", "description": "что-то", "price": "1010"},
        {"id": 2, "name": "Человек черный", "description": "что-то", "price": "1010"},
        {"id": 3, "name": "Человек узкоглазый", "description": "что-то", "price": "1010"}
    ]
