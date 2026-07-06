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

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == "alex" and password == "123":
            return redirect(url_for('products'))
        else:
            error_text = "Неверный логин или пароль"
            return render_template('login.html', error=error_text)
        
    return render_template("login.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        age = request.form.get('age')
        gender = request.form.get('gender')
        weight = request.form.get('weight')
        height = request.form.get('height')
        activity = request.form.get('activity')

        if not all([username, password, age, gender, weight, height, activity]):
            return render_template('register.html', error="Пожалуйста, заполните все поля.")

        try:
            age = int(age)
            weight = float(weight)
            height = int(height)
        except ValueError:
            return render_template('register.html', error="Некорректный формат числовых полей.")

        return redirect(url_for('login'))
    return render_template("register.html")

asgi_app = WsgiToAsgi(app)