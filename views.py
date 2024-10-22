# views.py
from flask import Blueprint, render_template, request
from flask_login import current_user, login_required, login_user, logout_user

# Crea un Blueprint llamado 'views'
views_bp = Blueprint("views", __name__)


@views_bp.route("/")
def index():
    return render_template("index.html")


@views_bp.route("/shop")
def shop():
    return render_template("shop.html")


@views_bp.route("/contact")
def contact():
    return render_template("contact.html")


@views_bp.route("/comprar")
def sell():
    return render_template("comprar.html")


@views_bp.route("/carrito")
def carrito():
    return render_template("carrito.html")


@views_bp.route("/register")
def register():
    return render_template("register.html")


@views_bp.route("/login")
def login():
    return render_template("login.html")


@views_bp.route("/detallesproducto")
def detallesproducto():
    product_id = request.args.get("id")
    return render_template("detallesproducto.html", product_id=product_id)


@views_bp.route("/editarproducto")
def editarproducto():
    product_id = request.args.get("id")
    return render_template("editarproducto.html", product_id=product_id)


@views_bp.route("/registroproducto")
def registroproducto():
    return render_template("registroproducto.html")


@views_bp.route("/misproductos")
def misproductos():
    return render_template("misproductos.html")


@views_bp.route("/profile")
def profile():
    return render_template("profile.html")


@views_bp.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")
