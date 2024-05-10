"""
@file app.py
@brief Archivo principal del servidor web
@details Este archivo se encarga de conectar la base de datos MySQL con la aplicacion web
@date 2024-03-12
@version 1.0.0
@author1 Jesus Antonio Lopez Bandala
@author2 Kitzya Minerva Luna Guadarrama
@author3 Yucef Ubayd Hernandez Garcia
@author4 Angel Yael Monroy Muñoz
@colaborator Hector Ramses Navarrete Gomez
"""
from flask import Flask, jsonify, render_template, request, session
from flask_mysqldb import MySQL
import re
import bcrypt

app = Flask(__name__)
app.secret_key = 'jinofvx' # La clave es aleatoria, solo es para que funcione la sesión
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "yadmandul_store"
mysql = MySQL(app)

#Metodos para las paginas
def is_emp(email):
    pattern = r"[a-zA-Z0-9\.]+@yad.mx"
    return re.search(pattern, email)

def is_admin(email):
    pattern = r"[a-zA-Z0-9\.]+@yad.admin.mx"
    return re.search(pattern, email)

def encrypt_password(password):
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password.decode('utf-8')

def check_password(hashed_password, user_password):
    user_password_bytes = user_password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')

    return bcrypt.checkpw(user_password_bytes, hashed_password_bytes)

@app.route('/startsession', methods=['POST'])
def startsession():
    try:
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            cur = mysql.connection.cursor()
            query = ""
            user_type = ""
            if is_admin(email):
                query = """
                    SELECT id_admin as id, password_admin as password FROM administradores WHERE correo_admin = %s
                """
                user_type = "administrador"
            elif is_emp(email):
                query = """
                    SELECT id_emp as id, password_emp as password FROM empleados WHERE correo_emp = %s
                """
                user_type = "empleado"
            else:
                query = """
                    SELECT id_cli as id, password_cli as password FROM clientes WHERE correo_cli = %s
                """
                user_type = "cliente"

            cur.execute(query, (email,))
            user = cur.fetchall()
            if user:
                if check_password(user[0][1], password):
                    session['user_id'] = user[0][0]
                    session['user_type'] = user_type
                    return jsonify({'loggeo_exitoso': True, 'user': user_type})
                else:
                    return jsonify({'loggeo_exitoso': False})
            else:
                return jsonify({'loggeo_exitoso': False})
    except Exception as e:
        return jsonify({'loggeo_exitoso': False, 'error': str(e)})
@app.route("/add_usr", methods = ['POST'])
def add_usr():
    try:
        if request.method == 'POST':
            nombre = request.form['nombre']
            ap_pat = request.form['ap_pat']
            ap_mat = request.form['ap_mat']
            fec_nac = request.form['fec_nac']
            correo = request.form['correo']
            password = encrypt_password(request.form['password'])
            cur = mysql.connection.cursor()
            query = ""
            if is_admin(correo): 
                query = """
                    INSERT INTO administradores VALUES (default, %s, %s, %s, %s, %s, %s, %s)
                """
            elif is_emp(correo):
                query = """
                    INSERT INTO empleados VALUES (default, %s, %s, %s, %s, %s, %s, true, %s)
                """
            else:
                query = """
                    INSERT INTO clientes VALUES (default, %s, %s, %s, %s, %s, %s, true, %s)
                """
            
            cur.execute(query, (nombre, ap_pat, ap_mat, fec_nac, correo, password, ''))
            mysql.connection.commit()
            return jsonify({'registro_exitoso': True})
    except Exception as e:
        return jsonify({'registro_exitoso': False, 'error': str(e)})

#Paginas
@app.route("/")
def index():
    if session:
        if session['user_type'] == 'administrador' or session['user_type'] == 'empleado':
            return 'Tu no deberias de estar aqui My friend'
    cur = mysql.connection.cursor()

    #Consulta para los usuarios
    cur.execute('SELECT nom_cli, foto_cli FROM clientes WHERE id_cli = %s', (session['user_id'], ))
    user_data = cur.fetchone()
    if user_data is not None:
        nom_cli, foto_cli = user_data
        if(len(nom_cli) > 6): nom_cli = nom_cli[0:6]
        if(foto_cli == ''): foto_cli = 'assets/img/user.png'
        user = {"name": nom_cli, "photo": foto_cli}
    else:
        user = {"name": "", "photo": ""}

    #Consulta para bebidas
    cur.execute('SELECT nom_prod, precio_prod, foto_prod FROM productos WHERE cantidad_prod > 0 AND estado_prod=true AND tipo_prod="bebidas"')
    bebidas = cur.fetchall()

    #Consulta para dulces
    cur.execute('SELECT nom_prod, precio_prod, foto_prod FROM productos WHERE cantidad_prod > 0 AND estado_prod=true AND tipo_prod="dulces"')
    dulces = cur.fetchall()
    #print(data)
    return render_template(
        "index.html", 
        bebidas = bebidas, 
        dulces = dulces, 
        user = user
    )

@app.errorhandler(404)
def page_not_found(e):
    # Si el usuario intenta acceder a una página que no existe, regresa un error 404
    return render_template('404.html'), 404

@app.route('/login')
def inicio_sesion():
    return render_template('inicioSesionClientes.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/empleados')
def empleados():
    if session:
        if session['user_type'] == 'cliente' or session['user_type'] == 'administrador':
            return 'Tu no deberias de estar aqui My friend'
    return render_template('cuentaEmpleados.html')

@app.route('/administradores')
def administradores():
    if session:
        if session['user_type'] == 'cliente' or session['user_type'] == 'empleado':
            return 'Tu no deberias de estar aqui My friend'
    return render_template("cuentaAdmins.html")

if __name__ == '__main__':
    app.run(debug=True) # Inicia el servidor web en modo debug