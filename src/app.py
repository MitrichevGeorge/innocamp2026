from flask import Flask, render_template, session, request, redirect, url_for
from asgiref.wsgi import WsgiToAsgi
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

@app.route("/")
def index():
    return redirect("/products")

@app.route("/products", methods=["GET", "POST"])
def products():
    products: list = session.get('products', [])
    if request.method == "POST":
        product_name = request.form.get('product')
        quantity = request.form.get('quantity')
        action = request.form.get('action')
        if action == "add":
            if product_name and quantity:
                quantity = int(quantity)
                products.append({"product_name":product_name, "quantity": quantity})
    session['products'] = products
    return render_template("products.html", tab=1, products=products)

@app.route("/schedule")
def schedule():
    return render_template("diet.html", tab=2)

@app.route("/shop")
def shop():
    return render_template("recom.html", tab=3)

@app.route("/settings")
def settings():
    return render_template("settings.html", tab=4)

asgi_app = WsgiToAsgi(app)