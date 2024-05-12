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
import os
import uuid
from flask import Flask, jsonify, render_template, request, session, g, redirect, url_for
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

def generar_nombre_unico(nombre_original):
    nombre_unico = uuid.uuid4().hex # Genera un nombre aleatorio
    extension = os.path.splitext(nombre_original)[1] # Obtiene la extensión del archivo
    return f"{nombre_unico}{extension}" # Regresa el nombre aleatorio con la extensión

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
                    SELECT id_emp as id, password_emp as password FROM empleados WHERE correo_emp = %s AND estado_emp = true
                """
                user_type = "empleado"
            else:
                query = """
                    SELECT id_cli as id, password_cli as password FROM clientes WHERE correo_cli = %s AND estado_cli = true
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
                return jsonify({'loggeo_exitoso': False, 'error': "El usuario esta baneado"})
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

@app.route("/modify_name_employee", methods = ['POST'])
def modify_name_employee():
    try:
        if request.method == 'POST':
            name = request.form['name']
            cur = mysql.connection.cursor()
            cur.execute("UPDATE empleados SET nom_emp = %s WHERE id_emp = %s", (name, session['user_id']))
            mysql.connection.commit()
            return jsonify({'modificacion_exitosa': True})
    except Exception as e:
        return jsonify({'modificacion_exitosa': False, 'error': str(e)})

@app.route("/modify_name_admin", methods = ['POST'])
def modify_name_admin():
    try:
        if request.method == 'POST':
            name = request.form['name']
            cur = mysql.connection.cursor()
            cur.execute("UPDATE administradores SET nom_admin = %s WHERE id_admin = %s", (name, session['user_id']))
            mysql.connection.commit()
            return jsonify({'modificacion_exitosa': True})
    except Exception as e:
        return jsonify({'modificacion_exitosa': False, 'error': str(e)})

@app.route("/modify_appat_employee", methods = ['POST'])
def modify_appat_employee():
    try:
        if request.method == 'POST':
            appat = request.form['appat']
            cur = mysql.connection.cursor()
            cur.execute("UPDATE empleados SET ap_pat_emp = %s WHERE id_emp = %s", (appat, session['user_id']))
            mysql.connection.commit()
            return jsonify({'modificacion_exitosa': True})
    except Exception as e:
        return jsonify({'modificacion_exitosa': False, 'error': str(e)})

@app.route("/modify_appat_admin", methods = ['POST'])
def modify_appat_admin():
    try:
        if request.method == 'POST':
            appat = request.form['appat']
            cur = mysql.connection.cursor()
            cur.execute("UPDATE administradores SET ap_pat_admin = %s WHERE id_admin = %s", (appat, session['user_id']))
            mysql.connection.commit()
            return jsonify({'modificacion_exitosa': True})
    except Exception as e:
        return jsonify({'modificacion_exitosa': False, 'error': str(e)})


@app.route("/modify_apmat_employee", methods = ['POST'])
def modify_apmat_employee():
    try:
        if request.method == 'POST':
            apmat = request.form['apmat']
            cur = mysql.connection.cursor()
            cur.execute("UPDATE empleados SET ap_mat_emp = %s WHERE id_emp = %s", (apmat, session['user_id']))
            mysql.connection.commit()
            return jsonify({'modificacion_exitosa': True})
    except Exception as e:
        return jsonify({'modificacion_exitosa': False, 'error': str(e)})

@app.route("/modify_apmat_admin", methods = ['POST'])
def modify_apmat_admin():
    try:
        if request.method == 'POST':
            apmat = request.form['apmat']
            cur = mysql.connection.cursor()
            cur.execute("UPDATE administradores SET ap_mat_admin = %s WHERE id_admin = %s", (apmat, session['user_id']))
            mysql.connection.commit()
            return jsonify({'modificacion_exitosa': True})
    except Exception as e:
        return jsonify({'modificacion_exitosa': False, 'error': str(e)})

@app.route("/modify_correo_employee", methods = ['POST'])
def modify_correo_employee():
    try:
        if request.method == 'POST':
            correo = request.form['correo']
            if is_emp(correo):
                cur = mysql.connection.cursor()
                cur.execute("UPDATE empleados SET correo_emp = %s WHERE id_emp = %s", (correo, session['user_id']))
                mysql.connection.commit()
                return jsonify({'modificacion_exitosa': True})
            else: return jsonify({'modificacion_exitosa': False, 'error': "Correo inválido"})

    except Exception as e:
        return jsonify({'modificacion_exitosa': False, 'error': str(e)})

@app.route("/modify_correo_admin", methods = ['POST'])
def modify_correo_admin():
    try:
        if request.method == 'POST':
            correo = request.form['correo']
            if is_admin(correo):
                cur = mysql.connection.cursor()
                cur.execute("UPDATE administradores SET correo_admin = %s WHERE id_admin = %s", (correo, session['user_id']))
                mysql.connection.commit()
                return jsonify({'modificacion_exitosa': True})
            else: return jsonify({'modificacion_exitosa': False, 'error': "Correo inválido"})
    except Exception as e:
        return jsonify({'modificacion_exitosa': False, 'error': str(e)})

@app.route("/modify_password_employee", methods = ['POST'])
def modify_password_employee():
    try:
        if request.method == 'POST':
            password = encrypt_password(request.form['password'])
            cur = mysql.connection.cursor()
            cur.execute("UPDATE empleados SET password_emp = %s WHERE id_emp = %s", (password, session['user_id']))
            mysql.connection.commit()
            return jsonify({'modificacion_exitosa': True})
    except Exception as e:
        return jsonify({'modificacion_exitosa': False, 'error': str(e)})

@app.route("/modify_password_admin", methods = ['POST'])
def modify_password_admin():
    try:
        if request.method == 'POST':
            password = encrypt_password(request.form['password'])
            cur = mysql.connection.cursor()
            cur.execute("UPDATE administradores SET password_admin = %s WHERE id_admin = %s", (password, session['user_id']))
            mysql.connection.commit()
            return jsonify({'modificacion_exitosa': True})
    except Exception as e:
        return jsonify({'modificacion_exitosa': False, 'error': str(e)})

@app.route("/upload_img_employee", methods = ['POST'])
def upload_img_employee():
    try:
        if request.method == 'POST':
            cur = mysql.connection.cursor()
            cur.execute("SELECT foto_emp FROM empleados WHERE id_emp = %s", (session['user_id'], ))
            current_photo = cur.fetchone()
            if current_photo[0] != '': os.remove('static/' + current_photo[0])
            file = request.files['photo']
            unique_file = generar_nombre_unico(file.filename)
            url_photo = 'static/uploads/empleados/' + unique_file
            file.save(url_photo)
            url_photo = 'uploads/empleados/' + unique_file
            cur.execute("UPDATE empleados SET foto_emp = %s WHERE id_emp = %s", (url_photo, session['user_id']))
            mysql.connection.commit()
            return jsonify({'modificacion_exitosa': True})
    except Exception as e:
        return jsonify({'modificacion_exitosa': False, 'error': str(e)})

@app.route("/logout")
def logout():
    session.pop('user_id', None)
    session.pop('user_type', None)
    g.user = None

    return redirect(url_for('inicio_sesion'))

@app.before_request
def load_user():
    if 'user_id' in session:
        if session['user_type'] == 'cliente':
            cur = mysql.connection.cursor()
            cur.execute('SELECT nom_cli, ap_pat_cli, ap_mat_cli, fecha_nac_cli, correo_cli, password_cli, foto_cli FROM clientes WHERE id_cli = %s', (session['user_id'], ))
            user_data = cur.fetchone()
        elif session['user_type'] == 'empleado':
            cur = mysql.connection.cursor()
            cur.execute('SELECT nom_emp, ap_pat_emp, ap_mat_emp, fec_nac_emp, correo_emp, password_emp, foto_emp FROM empleados WHERE id_emp = %s', (session['user_id'], ))
            user_data = cur.fetchone()
        elif session['user_type'] == 'administrador':
            cur = mysql.connection.cursor()
            cur.execute('SELECT nom_admin, ap_pat_admin, ap_mat_admin, fec_nac_admin, correo_admin, password_admin, foto_admin FROM administradores WHERE id_admin = %s', (session['user_id'], ))
            user_data = cur.fetchone()

        if user_data is not None:
            nom, ap_pat, ap_mat, fecha_nac, correo, password, foto = user_data
            if(session['user_type'] == 'cliente' and len(nom) > 6): nom = nom[0:6]
            if(foto == ''): foto = 'assets/img/user.png'
            user = {
                "name": nom,
                "ap_pat": ap_pat,
                "ap_mat": ap_mat,
                "fecha_nac": fecha_nac,
                "correo": correo,
                "password": password, 
                "photo": foto
            }
            g.user = user
        else:
            user = {
                "name": "",
                "ap_pat": "",
                "ap_mat": "",
                "fecha_nac": "",
                "correo": "",
                "password": "", 
                "photo": ""
            }
            g.user = user
        
    else:
        g.user = None

@app.route('/dar_de_baja_emp/<int:id>', methods = ['POST'])
def dar_de_baja_emp(id):
    if session and session['user_type'] == 'administrador':
        cur = mysql.connection.cursor()
        cur.execute("UPDATE empleados SET estado_emp = false WHERE id_emp = %s", (id, ))
        mysql.connection.commit()
        return redirect(url_for('administradores'))
    else:
        return "No tienes permisos para realizar esta acción"

@app.route('/dar_de_alta_emp/<int:id>', methods = ['POST'])
def dar_de_alta_emp(id):
    if session and session['user_type'] == 'administrador':
        cur = mysql.connection.cursor()
        cur.execute("UPDATE empleados SET estado_emp = true WHERE id_emp = %s", (id, ))
        mysql.connection.commit()
        return redirect(url_for('administradores'))
    else:
        return "No tienes permisos para realizar esta acción"

@app.route('/dar_de_baja_cli/<int:id>', methods = ['POST'])
def dar_de_baja_cli(id):
    if session and session['user_type'] == 'administrador':
        cur = mysql.connection.cursor()
        cur.execute("UPDATE clientes SET estado_cli = false WHERE id_cli = %s", (id, ))
        mysql.connection.commit()
        return redirect(url_for('administradores'))
    else:
        return "No tienes permisos para realizar esta acción"

@app.route('/dar_de_baja_prod/<int:id>', methods = ['POST'])
def dar_de_baja_prod(id):
    if session and session['user_type'] == 'empleado':
        cur = mysql.connection.cursor()
        cur.execute("UPDATE productos SET estado_prod = false WHERE id_prod = %s", (id, ))
        mysql.connection.commit()
        return redirect(url_for('empleados'))
    else:
        return "No tienes permisos para realizar esta acción"

@app.route('/dar_de_alta_cli/<int:id>', methods = ['POST'])
def dar_de_alta_cli(id):
    if session and session['user_type'] == 'administrador':
        cur = mysql.connection.cursor()
        cur.execute("UPDATE clientes SET estado_cli = true WHERE id_cli = %s", (id, ))
        mysql.connection.commit()
        return redirect(url_for('administradores'))
    else:
        return "No tienes permisos para realizar esta acción"

@app.route('/dar_de_alta_prod/<int:id>', methods = ['POST'])
def dar_de_alta_prod(id):
    if session and session['user_type'] == 'empleado':
        cur = mysql.connection.cursor()
        cur.execute("UPDATE productos SET estado_prod = true WHERE id_prod = %s", (id, ))
        mysql.connection.commit()
        return redirect(url_for('empleados'))
    else:
        return "No tienes permisos para realizar esta acción"

@app.route("/upload_img_admin", methods = ['POST'])
def upload_img_admin():
    try:
        if request.method == 'POST':
            cur = mysql.connection.cursor()
            cur.execute("SELECT foto_admin FROM administradores WHERE id_admin = %s", (session['user_id'], ))
            current_photo = cur.fetchone()
            if current_photo[0] != '': os.remove('static/' + current_photo[0])
            file = request.files['photo']
            unique_file = generar_nombre_unico(file.filename)
            url_photo = 'static/uploads/admins/' + unique_file
            file.save(url_photo)
            url_photo = 'uploads/admins/' + unique_file
            cur.execute("UPDATE administradores SET foto_admin = %s WHERE id_admin = %s", (url_photo, session['user_id']))
            mysql.connection.commit()
            return jsonify({'modificacion_exitosa': True})
    except Exception as e:
        return jsonify({'modificacion_exitosa': False, 'error': str(e)})

@app.route("/modify_prod/<int:id>", methods = ['POST'])
def modify_prod(id):
    if session and session['user_type'] == 'empleado':
        try:
            if request.method == 'POST':
                id_prov = request.form['id_prov']
                cur = mysql.connection.cursor()
                cur.execute("SELECT foto_prod FROM productos WHERE id_prod = %s", (id, ))
                current_photo = cur.fetchone()
                file = request.files['foto_prod']
                if file.filename != '':
                    if current_photo[0] != '': os.remove('static/' + current_photo[0])
                    unique_file = generar_nombre_unico(file.filename)
                    url_photo = 'static/uploads/img_products/' + unique_file
                    file.save(url_photo)
                    url_photo = 'uploads/img_products/' + unique_file
                else: url_photo = current_photo[0]
                nom_prod = request.form['nom_prod']
                tipo_prod = request.form['tipo_prod']
                precio_prod = request.form['precio_prod']
                cantidad_prod = request.form['cantidad_prod']
                cur.execute("UPDATE productos SET id_prov = %s, foto_prod = %s, nom_prod = %s, tipo_prod = %s, precio_prod = %s, cantidad_prod = %s WHERE id_prod = %s", (id_prov, url_photo, nom_prod, tipo_prod, precio_prod, cantidad_prod, id))
                mysql.connection.commit()
                return jsonify({'modificacion_exitosa': True})
        except Exception as e:
            return jsonify({'modificacion_exitosa': False, 'error': str(e)})
        
#Paginas
@app.route("/")
def index():
    if session:
        # if session['user_type'] == 'administrador' or session['user_type'] == 'empleado':
        #     return 'Tu no deberias de estar aqui My friend'
        if session['user_type'] == 'administrador':
            return redirect(url_for('administradores'))
        elif session['user_type'] == 'empleado':
            return redirect(url_for('empleados'))
    cur = mysql.connection.cursor()

    #Consulta para bebidas
    cur.execute('SELECT nom_prod, precio_prod, foto_prod FROM productos WHERE cantidad_prod > 0 AND estado_prod=true AND tipo_prod="bebidas"')
    bebidas = cur.fetchall()

    #Consulta para dulces
    cur.execute('SELECT nom_prod, precio_prod, foto_prod FROM productos WHERE cantidad_prod > 0 AND estado_prod=true AND tipo_prod="dulces"')
    dulces = cur.fetchall()
    
    #Consulta para jarcieria
    cur.execute('SELECT nom_prod, precio_prod, foto_prod FROM productos WHERE cantidad_prod > 0 AND estado_prod=true AND tipo_prod="jarcieria"')
    jarcieria = cur.fetchall()

    #Consulta para comidas
    cur.execute('SELECT nom_prod, precio_prod, foto_prod FROM productos WHERE cantidad_prod > 0 AND estado_prod=true AND tipo_prod="cinstantanea"')
    comidas = cur.fetchall()

    return render_template(
        "index.html", 
        bebidas = bebidas, 
        dulces = dulces, 
        jarcieria = jarcieria,
        comidas = comidas,
        user = g.user
    )

@app.errorhandler(404)
def page_not_found(e):
    # Si el usuario intenta acceder a una página que no existe, regresa un error 404
    return render_template('404.html'), 404

@app.route('/login')
def inicio_sesion():
    if g.user:
        return redirect(url_for('index'))
    return render_template('inicioSesionClientes.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/empleados')
def empleados():
    if session:
        # if session['user_type'] == 'cliente' or session['user_type'] == 'administrador':
        #     return 'Tu no deberias de estar aqui My friend'
        if session['user_type'] == 'cliente':
            return redirect(url_for('index'))
        elif session['user_type'] == 'administrador':
            return redirect(url_for('administradores'))
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT id_prod, id_prov, foto_prod, nom_prod, tipo_prod, precio_prod, cantidad_prod, estado_prod FROM productos")
    productos = cur.fetchall()
    list_productos = [list(producto) for producto in productos]
    for producto in list_productos:
        if producto[2] == '': producto[2] = "assets/img/product.png"
    return render_template(
        'cuentaEmpleados.html', 
        user = g.user, 
        productos = list_productos,
        tipos_prod = ['dulces', 'bebidas', 'jarcieria', 'cinstantanea']
    )

@app.route('/administradores')
def administradores():
    if session:
        # if session['user_type'] == 'cliente' or session['user_type'] == 'empleado':
        #     return 'Tu no deberias de estar aqui My friend'
        if session['user_type'] == 'cliente':
            return redirect(url_for('index'))
        elif session['user_type'] == 'empleado':
            return redirect(url_for("empleados"))
    cur = mysql.connection.cursor()
    cur.execute("SELECT id_emp, foto_emp, CONCAT(nom_emp, ' ', ap_pat_emp, ' ', ap_mat_emp) as 'Nombre completo', fec_nac_emp, correo_emp, estado_emp FROM empleados")
    empleados = cur.fetchall()
    cur.execute("SELECT id_cli, foto_cli, CONCAT(nom_cli, ' ', ap_pat_cli, ' ', ap_mat_cli) as 'Nombre completo', fecha_nac_cli, correo_cli, estado_cli FROM clientes")
    clientes = cur.fetchall()
    list_empleados = [list(empleado) for empleado in empleados]
    list_clientes = [list(cliente) for cliente in clientes]
    for empleado in list_empleados:
        if empleado[1] == '': empleado[1] = "assets/img/user.png"
    for cliente in list_clientes:
        if cliente[1] == '': cliente[1] = "assets/img/user.png"
    return render_template(
        "cuentaAdmins.html", 
        user = g.user, 
        empleados = list_empleados,
        clientes = list_clientes
    )

if __name__ == '__main__':
    app.run(debug=True) # Inicia el servidor web en modo debug