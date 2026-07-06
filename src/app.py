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

recipes_data = [
            ("Овсяная каша", "завтрак", "Овсянка на молоке с маслом"),
            ("Яичница с помидорами", "завтрак", "Яичница с томатами и зеленью"),
            ("Омлет с сыром", "завтрак", "Омлет с твёрдым сыром"),
            ("Каша гречневая с молоком", "завтрак", "Гречка с молоком и маслом"),
            ("Творог с ягодами", "завтрак", "Творог с клубникой или малиной"),
            ("Бутерброд с маслом", "завтрак", "Хлеб с маслом и чай"),
            ("Рисовая каша на молоке", "завтрак", "Рис с молоком и сахаром"),
            ("Запеканка творожная", "завтрак", "Творожная запеканка с изюмом"),
            ("Гречка с курицей", "обед", "Гречневая каша с куриной грудкой"),
            ("Рис с овощами", "обед", "Рис с морковью и луком, заправленный маслом"),
            ("Картофельное пюре с котлетой", "обед", "Пюре с куриной котлетой"),
            ("Паста с соусом болоньезе", "обед", "Макароны с мясным соусом из говядины"),
            ("Рис с рыбой", "обед", "Рис с лососем и зеленью"),
            ("Гречка с грибами", "обед", "Гречка с шампиньонами и луком"),
            ("Плов с курицей", "обед", "Рис с курицей и морковью"),
            ("Картошка тушеная с мясом", "обед", "Картофель с говядиной и луком"),
            ("Картофельное пюре с котлетой", "ужин", "Пюре с куриной котлетой"),
            ("Запеченная рыба с овощами", "ужин", "Лосось с брокколи и морковью"),
            ("Гречка с печенью", "ужин", "Гречка с говяжьей печенью"),
            ("Овощное рагу", "ужин", "Кабачок, баклажан, перец, томаты"),
            ("Творожная запеканка", "ужин", "Творожная запеканка с фруктами"),
            ("Куриное филе с рисом", "ужин", "Куриная грудка с рисом и соевым соусом"),
            ("Салат с тунцом", "ужин", "Салат с тунцом, яйцом, огурцом и зеленью"),
            ("Омлет с овощами", "ужин", "Омлет с помидорами, луком и перцем"),
            ("Овощной суп", "суп", "Лёгкий суп с картофелем, морковью, луком и капустой"),
            ("Борщ", "суп", "Борщ со свеклой, капустой, картофелем и томатами"),
            ("Куриный суп", "суп", "Суп с курицей, картофелем и вермишелью"),
            ("Суп-пюре из тыквы", "суп", "Крем-суп из тыквы со сливками"),
            ("Грибной суп", "суп", "Суп с шампиньонами, картофелем и зеленью"),
            ("Солянка", "суп", "Солянка с мясными продуктами (говядина, колбаса)"),
            ("Суп с фасолью", "суп", "Суп с красной фасолью и копченостями"),
        ]
@app.route("/schedule", methods=['GET', 'POST'])
def schedule():
    answer = ""
    if request.method == 'POST':
        recipe_name = request.form.get('recipe_name')
        chosen_plan = request.form.get('plan_type')
        
        answer = (f"Добавляем '{recipe_name}' в план на {chosen_plan}")
    return render_template("diet.html", tab=2, recipes_data=recipes_data, answer=answer)

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