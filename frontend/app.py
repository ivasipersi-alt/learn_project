from flask import Flask, render_template, request, redirect, flash, url_for, session
import requests
import os

app = Flask(__name__)
# Секретный ключ нужен для работы сессий (корзины) и flash-сообщений
app.secret_key = "super-secret-school-key"
API_URL = "http://127.0.0.1:8000"


@app.route("/")
def index():
    try:
        r = requests.get(f"{API_URL}/courses", timeout=5)
        courses = r.json() if r.ok else []
    except Exception as e:
        flash(f"Ошибка подключения к API: {e}", "error")
        courses = []

    # Считаем количество товаров в корзине для отображения в меню
    cart_count = len(session.get('cart', []))
    return render_template("index.html", courses=courses, cart_count=cart_count)


@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        data = {
            "title": request.form.get("title"),
            "description": request.form.get("description"),
            "price": float(request.form.get("price")),
            "duration_months": int(request.form.get("duration_months")),
            "instructor": request.form.get("instructor")
        }
        if requests.post(f"{API_URL}/courses", json=data).status_code == 201:
            flash("Новый курс успешно добавлен!", "success")
            return redirect(url_for('index'))
    return render_template("form.html")


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    if request.method == "POST":
        data = {
            "title": request.form.get("title"),
            "description": request.form.get("description"),
            "price": float(request.form.get("price")),
            "duration_months": int(request.form.get("duration_months")),
            "instructor": request.form.get("instructor")
        }
        if requests.put(f"{API_URL}/courses/{id}", json=data).ok:
            flash("Курс обновлен!", "success")
            return redirect(url_for('index'))

    # Получаем данные курса и передаем их в шаблон edit.html
    r = requests.get(f"{API_URL}/courses/{id}")
    if r.ok:
        return render_template("edit.html", course=r.json())

    flash("Курс не найден", "error")
    return redirect(url_for('index'))


@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    requests.delete(f"{API_URL}/courses/{id}")
    # Если курс удалили, убираем его и из корзины
    if 'cart' in session and id in session['cart']:
        session['cart'].remove(id)
        session.modified = True
    flash("Курс удалён.", "success")
    return redirect(url_for('index'))


# --- ЛОГИКА КОРЗИНЫ ---

@app.route("/cart")
def view_cart():
    cart_ids = session.get('cart', [])
    cart_items = []
    total_sum = 0

    # Запрашиваем информацию по каждому курсу в корзине
    for course_id in cart_ids:
        r = requests.get(f"{API_URL}/courses/{course_id}")
        if r.ok:
            course = r.json()
            cart_items.append(course)
            total_sum += course.get('price', 0)

    return render_template("cart.html", cart_items=cart_items, total_sum=total_sum)


@app.route("/cart/add/<int:id>", methods=["POST"])
def add_to_cart(id):
    if 'cart' not in session:
        session['cart'] = []

    if id not in session['cart']:
        session['cart'].append(id)
        session.modified = True
        flash("Курс добавлен в корзину!", "success")
    else:
        flash("Этот курс уже есть в корзине.", "info")

    return redirect(url_for('index'))


@app.route("/cart/remove/<int:id>", methods=["POST"])
def remove_from_cart(id):
    if 'cart' in session and id in session['cart']:
        session['cart'].remove(id)
        session.modified = True
        flash("Курс удален из корзины.", "success")
    return redirect(url_for('view_cart'))


if __name__ == "__main__":
    app.run(port=5000, debug=True)