from flask import request, jsonify, Blueprint, session, url_for, redirect, render_template, g
from app.pages_fun import *
from app.db import obtener_conexion

general = Blueprint('general', __name__)

@general.route('/startsession', methods=['POST'])
def startsession():
    try:
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            query = ""
            user_type = ""
            if is_admin(email):
                query = """
                    SELECT id_admin as id, password_admin as password FROM administradores WHERE correo_admin = %s
                """
                user_type = "administrador"
            elif is_emp(email):
                query = """
                    SELECT id_emp as id, password_emp as password FROM empleados WHERE correo_emp = %s AND estado_emp = true
                """
                user_type = "empleado"
            else:
                query = """
                    SELECT id_cli as id, password_cli as password FROM clientes WHERE correo_cli = %s AND estado_cli = true
                """
                user_type = "cliente"
            conexion = obtener_conexion()
            cur = conexion.cursor()
            cur.execute(query, (email,))
            user = cur.fetchall()
            conexion.close()
            if user:
                if check_password(user[0][1], password):
                    session['user_id'] = user[0][0]
                    session['user_type'] = user_type
                    return jsonify({'loggeo_exitoso': True, 'user': user_type})
                else:
                    return jsonify({'loggeo_exitoso': False})
            else:
                return jsonify({'loggeo_exitoso': False, 'error': "El usuario esta baneado"})
    except Exception as e:
        return jsonify({'loggeo_exitoso': False, 'error': str(e)})
