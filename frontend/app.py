from flask import Flask, render_template, request, redirect, flash, url_for, session
import requests
import os

app = Flask(__name__)
app.secret_key = "popi"
API_URL = "http://127.0.0.1:8000"


@app.route("/")
def index():
    filter_type = request.args.get('filter')
    cart_count = len(session.get('cart', []))

    try:
        params = {"filter_type": filter_type} if filter_type else {}
        r = requests.get(f"{API_URL}/courses", params=params, timeout=5)
        courses = r.json() if r.ok else []
    except Exception as e:
        flash(f"Ошибка подключения к API: {e}", "error")
        courses = []

    return render_template("index.html", courses=courses, current_filter=filter_type, cart_count=cart_count)


@app.route("/create", methods=["GET", "POST"])
def create():
    cart_count = len(session.get('cart', []))
    if request.method == "POST":
        is_free = request.form.get("is_free") == "on"

        if is_free:
            price = 0.0
            discount_percent = 0
        else:
            raw_price = request.form.get("price")
            price = float(raw_price) if raw_price else 0.0
            discount_percent = int(request.form.get("discount_percent") or 0)

        data = {
            "title": request.form.get("title"),
            "description": request.form.get("description"),
            "price": price,
            "discount_percent": discount_percent,  # Вот этого у тебя не было на скрине!
            "duration_months": int(request.form.get("duration_months")),
            "instructor": request.form.get("instructor")
        }

        r = requests.post(f"{API_URL}/courses", json=data)
        if r.status_code == 201:
            flash("Новый курс успешно добавлен!", "success")
            return redirect(url_for('index'))
        else:
            flash(f"Ошибка API ({r.status_code}): курс не добавлен.", "error")

    return render_template("form.html", cart_count=cart_count)


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    cart_count = len(session.get('cart', []))
    if request.method == "POST":
        is_free = request.form.get("is_free") == "on"

        if is_free:
            price = 0.0
            discount_percent = 0
        else:
            raw_price = request.form.get("price")
            price = float(raw_price) if raw_price else 0.0
            discount_percent = int(request.form.get("discount_percent") or 0)

        data = {
            "title": request.form.get("title"),
            "description": request.form.get("description"),
            "price": float(request.form.get("price")),
            "discount_percent": int(request.form.get("discount_percent") or 0),
            "duration_months": int(request.form.get("duration_months")),
            "instructor": request.form.get("instructor")
        }

        r = requests.put(f"{API_URL}/courses/{id}", json=data)
        if r.ok:
            flash("Курс обновлен!", "success")
            return redirect(url_for('index'))
        else:
            flash(f"Ошибка API ({r.status_code}): данные не обновлены.", "error")

    r = requests.get(f"{API_URL}/courses/{id}")
    if r.ok:
        return render_template("edit.html", course=r.json(), cart_count=cart_count)

    flash("Курс не найден", "error")
    return redirect(url_for('index'))


@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    requests.delete(f"{API_URL}/courses/{id}")
    flash("Курс удалён.", "success")
    return redirect(url_for('index'))


@app.route("/cart")
def view_cart():
    cart_count = len(session.get('cart', []))
    cart_ids = session.get('cart', [])
    courses = []
    total_sum = 0

    for cid in cart_ids:
        r = requests.get(f"{API_URL}/courses/{cid}")
        if r.ok:
            course = r.json()
            courses.append(course)
            total_sum += course.get('final_price', course.get('price', 0))
        else:
            flash(f"Ошибка загрузки курса №{cid}. Бэкенд ответил: {r.status_code}", "error")

    return render_template("cart.html", cart_items=courses, total_sum=total_sum, cart_count=cart_count)


@app.route("/cart/add/<int:id>", methods=["POST"])
def add_to_cart(id):
    cart = list(session.get('cart', []))
    if id not in cart:
        cart.append(id)
        session['cart'] = cart
        session.modified = True
        flash("Курс добавлен в корзину!", "success")
    else:
        flash("Этот курс уже есть в корзине.", "info")
    return redirect(url_for('index'))


@app.route("/cart/remove/<int:id>", methods=["POST"])
def remove_from_cart(id):
    cart = list(session.get('cart', []))
    if id in cart:
        cart.remove(id)
        session['cart'] = cart
        session.modified = True
        flash("Курс удален из корзины.", "success")
    return redirect(url_for('view_cart'))


if __name__ == "__main__":
    app.run(port=5000, debug=True)
