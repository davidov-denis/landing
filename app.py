from flask import Flask, redirect, render_template, request, session
import sqlite3


app = Flask(__name__, static_folder="static")
app.config['SECRET_KEY'] = 'my-secret-key'


def to_db(name, email, phone, city, street, house, coords, howmany, color, price):
    conn = sqlite3.connect("banana.db")
    cur = conn.cursor()
    cur.execute("""INSERT INTO orders VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?)""",
                (name, email, phone, city, street, house, coords, howmany, color, price, False))
    conn.commit()
    conn.close()


def from_db_is_complete_true():
    conn = sqlite3.connect("banana.db")
    cur = conn.cursor()
    is_complete_true = cur.execute("""SELECT * FROM orders WHERE iscomplet=true ORDER BY id DESC;""").fetchall()
    conn.close()
    return is_complete_true


def from_db_is_complete_false():
    conn = sqlite3.connect("banana.db")
    cur = conn.cursor()
    is_complete_false = cur.execute("""SELECT * FROM orders WHERE iscomplet=false ORDER BY id DESC;""").fetchall()
    conn.close()
    return is_complete_false


def from_db_all():
    conn = sqlite3.connect("banana.db")
    cur = conn.cursor()
    all_table = cur.execute("""SELECT * FROM orders ORDER BY id DESC;""").fetchall()
    conn.close()
    return all_table


def update_db(id):
    conn = sqlite3.connect("banana.db")
    cur = conn.cursor()
    sql = "UPDATE orders SET iscomplet=true WHERE id={}".format(int(id))
    cur.execute(sql)
    conn.commit()
    conn.close()


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route("/kypi-banan/", methods=["POST", "GET"])
def kypi_banan():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        city = request.form.get("city")
        street = request.form.get("street")
        house = request.form.get("house")
        coords = request.form.get("coords")
        promo = request.form.get("promo")
        howmany = request.form.get("howmany")
        color = request.form.get("color")
        price = int(howmany) * 6 * 10 ** 7
        print(price)
        to_db(name, email, phone, city, street, house, coords, howmany, color, price)
        return render_template("kypi_banan.html", isOk=True)
    return render_template("kypi_banan.html", isOk=False)


@app.route("/admin/orders/update/", methods=["get", "post"])
def update_order():
    if request.method == "POST":
        id = request.form.get("id")
        print(id)
        update_db(id)
    return redirect("/admin/orders/")


@app.route("/admin/orders/")
def order():
    if "isAuth" in session:
        if session.get("isAuth") == True:
            all_table = from_db_all()
            return render_template("orders.html", orders=all_table)
        else:
            return redirect("/admin/")
    else:
        return redirect("/admin/")


@app.route("/admin/")
def admin():
    if "isAuth" in session:
        if session.get("isAuth") == True:
            return render_template("isAuth.html")
        else:
            return render_template("login.html")
    else:
        session["isAuth"] = False
        return render_template("login.html")


@app.route("/check/", methods=["get", "post"])
def check():
    if request.method == "POST":
        password = request.form.get("password")
        if password == "150105":
            session["isAuth"] = True
    return redirect("/admin/")

@app.route("/price-counter/", methods=["GET", "POST"])
def price_counter():
    printable = False
    if request.method == "POST":
        howmany = request.form.get("howmany")
        price = int(howmany) * 6 * 10 ** 7
        howmany = int(howmany) * 1000
        return render_template("price_counter.html", howmany=howmany, price=price, printable=True)
    return render_template("price_counter.html", printable=printable)


@app.route("/contact/")
def contact():
    return render_template("contact.html")

# UPDATE orders SET iscomplet=true WHERE id=5; ОБНОВЛЕНИЕ БАЗЫ ДАННЫХ
# SELECT * FROM orders;


if __name__ == '__main__':
    app.run(debug=True)
