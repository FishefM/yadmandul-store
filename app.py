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
from flask import Flask, jsonify, render_template, request
from flask_mysqldb import MySQL
import re

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

@app.route("/add_usr", methods = ['POST'])
def add_usr():
    try:
        if request.method == 'POST':
            nombre = request.form['nombre']
            ap_pat = request.form['ap_pat']
            ap_mat = request.form['ap_mat']
            fec_nac = request.form['fec_nac']
            correo = request.form['correo']
            password = request.form['password']
            cur = mysql.connection.cursor()
            query = ""
            if is_admin(correo): 
                query = """
                    INSERT INTO administradores VALUES (default, %s, %s, %s, %s, %s, %s)
                """
            elif is_emp(correo):
                query = """
                    INSERT INTO empleados VALUES (default, %s, %s, %s, %s, %s, %s, true)
                """
            else:
                query = """
                    INSERT INTO clientes VALUES (default, %s, %s, %s, %s, %s, %s, true)
                """
            
            cur.execute(query, (nombre, ap_pat, ap_mat, fec_nac, correo, password))
            mysql.connection.commit()
            return jsonify({'registro_exitoso': True})
    except Exception as e:
        return jsonify({'registro_exitoso': False, 'error': str(e)})

#Paginas
@app.route("/")
def index():
    cur = mysql.connection.cursor()

    #Consulta para bebidas
    cur.execute('SELECT nom_prod, precio_prod, foto_prod FROM productos WHERE cantidad_prod > 0 AND estado_prod=true AND tipo_prod="bebidas"')
    bebidas = cur.fetchall()

    #Consulta para dulces
    cur.execute('SELECT nom_prod, precio_prod, foto_prod FROM productos WHERE cantidad_prod > 0 AND estado_prod=true AND tipo_prod="dulces"')
    dulces = cur.fetchall()
    #print(data)
    return render_template("index.html", bebidas = bebidas, dulces = dulces)

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

if __name__ == '__main__':
    app.run(debug=True) # Inicia el servidor web en modo debug