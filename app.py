# main.py
from flask import Flask, request, jsonify, abort, redirect, url_for
import sys
#from database import init_app, db
#from config.local import config
#from flask import Flask, send_file, render_template, init_app
import requests
import json
# flask-login
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
# end flask-login
#from models import Usuario, Comentario, Producto, Compra, Suscriptor
from views import views_bp
#from users_controller import users_bp

app = Flask(__name__)
#init_app(app)

#app.config['SECRET_KEY'] = config['SECRET_KEY']

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(user_id)

# Para la web

app.register_blueprint(views_bp)

# Para la API

@app.route('/productos/<id>', methods=['GET'])
def get_producto(id):
    try:
        producto = Producto.query.get(id)
        if producto:
            producto_data = {
                'id': producto.id,
                'nombre': producto.nombre,
                'descripcion': producto.descripcion,
                'precio': producto.precio,
                'categoria': producto.categoria,
                'stock': producto.stock,
                'imagen_producto': producto.imagen_producto
            }
            return jsonify({'success': True, 'producto': producto_data}), 200
        else:
            return jsonify({'success': False, 'message': 'Producto no encontrado'}), 404
    except Exception as e:
        print(sys.exc_info())
        return jsonify({'success': False, 'message': 'Error obteniendo producto'}), 500

@app.route('/productos/<producto_id>', methods=['PATCH'])
def update_stock(producto_id):
    producto = Producto.query.get_or_404(producto_id)
    cantidad = request.json.get('cantidad')
    
    if producto.stock >= cantidad:
        producto.stock -= cantidad
        db.session.commit()
        return jsonify({'success': True, 'message': 'Stock actualizado'}), 200
    else:
        return jsonify({'success': False, 'message': 'Stock insuficiente'}), 400

@app.route('/productos/<id>', methods=['DELETE'])
def delete_producto(id):
    try:
        producto = Producto.query.get(id)
        if producto:
            db.session.delete(producto)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Producto eliminado correctamente'}), 200
        else:
            return jsonify({'success': False, 'message': 'Producto no encontrado'}), 404
    except Exception as e:
        db.session.rollback()
        print(sys.exc_info())
        return jsonify({'success': False, 'message': 'Error eliminando producto'}), 500

@app.route('/usuario/<product_id>/producto', methods=['GET'])
def get_usuario_by_product_id(product_id):
    try:
        producto = Producto.query.get(product_id)
        if not producto:
            return jsonify({"success": False, "message": "Producto no encontrado"}), 404

        usuario = Usuario.query.get(producto.vendedor_id)
        if not usuario:
            return jsonify({"success": False, "message": "Usuario no encontrado"}), 404

        return jsonify({
            "success": True,
            "usuario": {
                "nombre": usuario.nombre,
                "telefono": usuario.telefono
            }
        })

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

