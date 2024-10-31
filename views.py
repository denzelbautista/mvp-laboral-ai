# views.py
import json
from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from flask_login import UserMixin, current_user, login_required, login_user, logout_user
import requests

# Crea un Blueprint llamado 'views'
views_bp = Blueprint("views", __name__)

usuarios = {}

class TempUser(UserMixin):
    def __init__(self, id):
        self.id = id

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


@views_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        correo = request.form.get("correo")
        contrasena = request.form.get("contrasena")

        lambda_payload = {
            'correo': correo,
            'contrasena': contrasena
        }

        try:
            lambda_response = requests.post(
                'https://cuneyfem18.execute-api.us-east-1.amazonaws.com/prod/auth/login',
                json=lambda_payload
            )

            print("Lambda response:", lambda_response.text)  # Debug: Muestra la respuesta completa

            if lambda_response.status_code == 200:
                try:
                    lambda_result = lambda_response.json()
                    body = json.loads(lambda_result.get('body', '{}'))

                    if body.get('success'):
                        user_id = body.get('user_id')
                        user = TempUser(id=user_id)
                        login_user(user)
                        return redirect(url_for("views.dashboard"))
                    else:
                        return jsonify({"success": False, "message": "Credenciales incorrectas"}), 401
                except json.JSONDecodeError:
                    return jsonify({"success": False, "message": "Error en formato JSON de Lambda"}), 500
            else:
                return jsonify({"success": False, "message": "Error en la respuesta de Lambda"}), lambda_response.status_code

        except Exception as e:
            return jsonify({"success": False, "message": "Error al iniciar sesión", "error": str(e)}), 500

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
