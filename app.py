from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_login import LoginManager, login_user, logout_user, login_required
import requests
from functools import wraps
from views import views_bp
import json
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'  
app.register_blueprint(views_bp)
SECRET_KEY = 'xdxd'

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

@app.route('/api/register', methods=['POST'])
def register_user():
    data = request.json
    # Validación de los campos recibidos
    required_fields = ['nombre', 'razon_social', 'RUC', 'correo', 'numero_contacto', 'contrasena']
    if not all(field in data for field in required_fields):
        return jsonify({'success': False, 'message': 'Datos incompletos'}), 400

    # Preparar datos para enviar a la API Lambda
    lambda_payload = {
        'correo_admin': data['correo'],
        'contrasena_admin': data['contrasena'],
        'ruc': data['RUC'],
        'razon_social': data['razon_social'],
        'empresa_datos': {
            'nombre': data['nombre'],
            'telefono': int(data['numero_contacto'])
        }
    }

    try:
        # Hacer la solicitud a la API Lambda
        lambda_response = requests.post(
            'https://cuneyfem18.execute-api.us-east-1.amazonaws.com/prod/auth/register', 
            json=lambda_payload
        )

        # Convertir la respuesta a JSON
        lambda_result = lambda_response.json()
        
        # Verificar el código de estado de la respuesta de Lambda
        if lambda_response.status_code == 200:
            # Descomponer el cuerpo
            body = json.loads(lambda_result['body'])  # Convertir el body de string a dict
            
            # Verificar el éxito de la creación
            if body.get('success'):
                
                token = body.get('token', None)
                return jsonify({'success': True, 'message': 'Usuario registrado', 'token': token}), 201
            else:
                return jsonify({'success': False, 'message': body.get('message', 'Error en registro')}), 400
        else:
            return jsonify({'success': False, 'message': 'Error en la respuesta de Lambda'}), lambda_response.status_code

    except Exception as e:
        return jsonify({'success': False, 'message': 'Error al registrar usuario', 'error': str(e)}), 500
    
@app.route('/api/login', methods=[ 'POST'])
def login_user_api():
    if request.method == 'POST':
        data = request.form  
        required_fields = ['correo', 'contrasena']
        if not all(field in data for field in required_fields):
            return jsonify({'success': False, 'message': 'Datos incompletos'}), 400

        
        lambda_payload = {
            'correo_admin': data['correo'],
            'contrasena_proporcionada': data['contrasena']
        }

        try:
            
            lambda_response = requests.post(
                'https://cuneyfem18.execute-api.us-east-1.amazonaws.com/prod/auth/login',
                json=lambda_payload
            )

            if lambda_response.status_code == 200:
                lambda_result = lambda_response.json()
                body = json.loads(lambda_result['body'])

                
                if body.get('success'):
                    token = body.get('token', None)
                    if not token:
                        return jsonify({'success': False, 'message': 'Token no encontrado en la respuesta'}), 500

                    
                    session['token'] = token
                    
                    return redirect(url_for('views.dashboard'))

                else:
                    
                    return render_template('login.html', error_message=body.get('message', 'Credenciales incorrectas'))
            else:
                return render_template('login.html', error_message='Error en la respuesta de Lambda')

        except requests.exceptions.RequestException as e:
            return render_template('login.html', error_message=f'Error en la solicitud a Lambda: {str(e)}')
    else:
        
        return render_template('login.html')


@app.route('/api/logout', methods=['POST'])
@login_required
def logout_user_api():
    logout_user()
    return jsonify({'success': True, 'message': 'Sesión cerrada exitosamente'}), 200

@app.route('/nuevo_empleo')
def create_empleo():
    return render_template('registroproducto.html')




@app.route('/submit', methods=['POST'])
def submit():
    
    token = session.get('token')

    if not token:
        return jsonify({'message': '¡Falta el token!'}), 403

    
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

    api_url = "https://azy1wlrgli.execute-api.us-east-1.amazonaws.com/prod/empleos/crear"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

   
    data = {
        "empleo_datos": empleo_datos
    }

    response = requests.post(api_url, json=data, headers=headers)

    if response.status_code == 200:
        return redirect(url_for('views.shop')) 
    else:
        
        return jsonify({'success': False, 'message': 'Error al registrar el empleo', 'details': response.json()}), 500


        

if __name__ == '__main__':
    app.run(debug=True)
