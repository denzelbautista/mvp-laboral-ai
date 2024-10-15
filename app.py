from flask import Flask, request, jsonify , render_template
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from views import views_bp
import requests
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Establece una clave secreta para la gestión de sesiones
app.register_blueprint(views_bp)

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'views.login'

# Estructuras de datos en memoria para reemplazar la base de datos
usuarios = {}
productos = {}
next_user_id = 1
next_product_id = 1

@login_manager.user_loader
def load_user(user_id):
    return usuarios.get(int(user_id))

@app.route('/productos/<int:id>', methods=['GET'])
def get_producto(id):
    producto = productos.get(id)
    if producto:
        return jsonify({'success': True, 'producto': producto}), 200
    return jsonify({'success': False, 'message': 'Producto no encontrado'}), 404

@app.route('/productos/<int:producto_id>', methods=['PATCH'])
def update_stock(producto_id):
    producto = productos.get(producto_id)
    if not producto:
        return jsonify({'success': False, 'message': 'Producto no encontrado'}), 404
    
    cantidad = request.json.get('cantidad', 0)
    if producto['stock'] >= cantidad:
        producto['stock'] -= cantidad
        return jsonify({'success': True, 'message': 'Stock actualizado'}), 200
    return jsonify({'success': False, 'message': 'Stock insuficiente'}), 400

@app.route('/productos/<int:id>', methods=['DELETE'])
def delete_producto(id):
    if id in productos:
        del productos[id]
        return jsonify({'success': True, 'message': 'Producto eliminado correctamente'}), 200
    return jsonify({'success': False, 'message': 'Producto no encontrado'}), 404

@app.route('/usuario/<int:product_id>/producto', methods=['GET'])
def get_usuario_by_product_id(product_id):
    producto = productos.get(product_id)
    if not producto:
        return jsonify({"success": False, "message": "Producto no encontrado"}), 404

    usuario = usuarios.get(producto['vendedor_id'])
    if not usuario:
        return jsonify({"success": False, "message": "Usuario no encontrado"}), 404

    return jsonify({
        "success": True,
        "usuario": {
            "nombre": usuario['nombre'],
            "telefono": usuario['telefono']
        }
    })

@app.route('/register', methods=['POST'])
def register_user():
    global next_user_id
    data = request.json
    if not data or 'nombre' not in data or 'telefono' not in data or 'password' not in data:
        return jsonify({'success': False, 'message': 'Datos incompletos'}), 400
    
    usuario = {
        'id': next_user_id,
        'nombre': data['nombre'],
        'telefono': data['telefono'],
        'password': data['password']  # En una aplicación real, almacena la contraseña hasheada
    }
    usuarios[next_user_id] = usuario
    next_user_id += 1
    return jsonify({'success': True, 'message': 'Usuario registrado'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data or 'nombre' not in data or 'password' not in data:
        return jsonify({'success': False, 'message': 'Datos incompletos'}), 400
    
    for usuario in usuarios.values():
        if usuario['nombre'] == data['nombre'] and usuario['password'] == data['password']:
            login_user(usuario)
            return jsonify({'success': True, 'message': 'Login exitoso'}), 200
    return jsonify({'success': False, 'message': 'Credenciales incorrectas'}), 401

@app.route('/nuevo_empleo')
def create_empleo():
    return render_template('registroproducto.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Captura de datos del formulario
    empresa_id = request.form.get("empresa_id")
    empleo_datos = {
        "nombre_empleo": request.form.get("nombre_empleo"),
        "tipo_contrato": request.form.get("tipo_contrato"),
        "fecha_publicacion": request.form.get("fecha_publicacion"),
        "fecha_final": request.form.get("fecha_final"),
        "modalidad": request.form.get("modalidad"),
        "ubicacion": request.form.get("ubicacion"),
        "salario_min": int(request.form.get("salario_min")),
        "salario_max": int(request.form.get("salario_max")),
        "experiencia": request.form.get("experiencia"),
        "vacantes": int(request.form.get("vacantes")),
        "descripcion": request.form.get("descripcion"),
        "funciones": request.form.get("funciones").split(","),
        "requisitos": request.form.get("requisitos").split(","),
        "beneficios": request.form.get("beneficios").split(","),
        "nivel_estudios": request.form.get("nivel_estudios")
    }

    data = {
        "empresa_id": empresa_id,
        "empleo_datos": empleo_datos
    }

    # Enviar datos a la API externa
    api_url = "https://azy1wlrgli.execute-api.us-east-1.amazonaws.com/prod/empleos/crear"
    headers = {"Content-Type": "application/json"}
    response = requests.post(api_url, json=data, headers=headers)

    # Mostrar la respuesta de la API
    if response.status_code == 200:
        return jsonify({"status": "success", "response_data": response.json()})
    else:
        return jsonify({"status": "error", "message": "Error al enviar los datos", "details": response.text}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)

