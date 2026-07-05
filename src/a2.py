from flask import Flask, render_template, session, request
from asgiref.wsgi import WsgiToAsgi
import secrets


app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

@app.route("/", methods=["GET","POST"])
def index():
    clicks = session.get('clicks', 0)
    if request.method == "POST":
        clicks += 1
    session['clicks'] = clicks
    return render_template("click.html", value=clicks)

asgi_app = WsgiToAsgi(app)