# views.py
from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from flask_login import UserMixin, current_user, login_required, login_user, logout_user
import requests
import json
# Crea un Blueprint llamado 'views'
views_bp = Blueprint("views", __name__)

usuarios = {}

class TempUser(UserMixin):
    def __init__(self, id):
        self.id = id

@views_bp.route("/")
def index():
    return render_template("index.html")


@views_bp.route("/empleos_listar")
def shop():
    response = requests.post('https://azy1wlrgli.execute-api.us-east-1.amazonaws.com/prod/empleos/listartodos', json={})
    
    if response.status_code == 200:
        
        body = response.json().get('body')
        if body:
            empleos = json.loads(body)  
            
        else:
            empleos = []
    else:
        empleos = []
        print("Error en la API:", response.status_code)

    return render_template("shop.html", empleos=empleos)

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


@views_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Obtener los datos del formulario
        correo = request.form.get("correo")
        contrasena = request.form.get("contrasena")

        # Imprime los valores para depuración
        print(f"Correo: {correo}, Contraseña: {contrasena}")

        # Verifica si ambos campos fueron completados
        if correo and contrasena:
            # Redirige a la página de dashboard si se ingresaron ambos campos
            return redirect(url_for("views.dashboard"))
        else:
            return jsonify({"success": False, "message": "Debe ingresar correo y contraseña"}), 400

    return render_template("login.html")


@views_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.index"))


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
