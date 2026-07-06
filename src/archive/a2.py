from flask import Flask, render_template, session, request
from asgiref.wsgi import WsgiToAsgi
import secrets


app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

@app.route("/", methods=["GET","POST"])
def index():
    clicks = session.get('clicks', 0)
    adding = session.get('adding', 1)
    if request.method == "POST":
        btt = request.form.get('action')
        if btt == "click":
            clicks += adding
        if btt == "upgrade":
            adding += 1
    session['clicks'] = clicks
    session['adding'] = adding
    return render_template("click.html", value=clicks, adding=adding)

asgi_app = WsgiToAsgi(app)