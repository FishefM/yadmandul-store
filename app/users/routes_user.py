
from flask import request, jsonify, Blueprint, session, url_for, redirect, render_template, g
from app.pages_fun import *
from app.db import obtener_conexion

user = Blueprint('user',__name__)

@user.route('/cuenta')
def cuenta():
    if session:
        # if session['user_type'] == 'cliente' or session['user_type'] == 'empleado':
        #     return 'Tu no deberias de estar aqui My friend'
        if session['user_type'] == 'administrador':
            return redirect(url_for('admin.administradores'))
        elif session['user_type'] == 'empleado':
            return redirect(url_for("employee.empleados"))
    else: return redirect(url_for('pagesR.inicio_sesion'))
    return render_template(
        "cuenta.html",
        user = g.user
    )

@user.route('/add_usr', methods = ['POST'])
def add_usr():
    try:
        if request.method == 'POST':
            nombre = request.form['nombre']
            ap_pat = request.form['ap_pat']
            ap_mat = request.form['ap_mat']
            fec_nac = request.form['fec_nac']
            correo = request.form['correo']
            password = encrypt_password(request.form['password'])                       
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
            conexion = obtener_conexion()
            with conexion.cursor() as cur:
                cur.execute(query, (nombre, ap_pat, ap_mat, fec_nac, correo, password, ''))
            conexion.commit()
            conexion.close()
            return jsonify({'registro_exitoso': True})
    except Exception as e:
        return jsonify({'registro_exitoso': False, 'error': str(e)})
    
@user.route("/upload_img_client", methods = ['POST'])
def upload_img_client():
    try:
        if request.method == 'POST':
            conexion = obtener_conexion()
            with conexion.cursor() as cur:
                cur.execute("SELECT foto_cli FROM clientes WHERE id_cli = %s", (session['user_id'], ))
                current_photo = cur.fetchone()
            conexion.close()
            if current_photo[0] != '': os.remove('app/static/' + current_photo[0])
            file = request.files['photo']
            unique_file = generar_nombre_unico(file.filename)
            url_photo = 'app/static/uploads/clientes/' + unique_file
            file.save(url_photo)
            url_photo = 'uploads/clientes/' + unique_file
            conexion = obtener_conexion()
            with conexion.cursor() as cur:
                cur.execute("UPDATE clientes SET foto_cli = %s WHERE id_cli = %s", (url_photo, session['user_id']))
            conexion.commit()
            conexion.close()
            return jsonify({'modificacion_exitosa': True})
    except Exception as e:
        return jsonify({'modificacion_exitosa': False, 'error': str(e)})

@user.route("/modify_password_cli", methods = ['POST'])
def modify_password_cli():
    try:
        if  request.method == 'POST':
            password = encrypt_password(request.form['password'])
            conexion = obtener_conexion()
            with conexion.cursor() as cur:
                cur.execute("UPDATE clientes SET password_cli = %s WHERE id_cli = %s", (password, session['user_id']))
            conexion.commit()
            conexion.close()
            return jsonify({'modificacion_exitosa': True})
    except Exception as e:
        return jsonify({'modificacion_exitosa': False, 'error': str(e)})

@user.route("/modify_correo_cli", methods = ['POST'])
def modify_correo_cli():
    try:
        if request.method == 'POST':
            correo = request.form['correo']
            if not is_admin(correo) and not is_emp(correo):
                conexion = obtener_conexion()
                with conexion.cursor() as cur:
                    cur.execute("UPDATE clientes SET correo_cli = %s WHERE id_cli = %s", (correo, session['user_id']))
                conexion.commit()
                conexion.close()
                return jsonify({'modificacion_exitosa': True})
            else: return jsonify({'modificacion_exitosa': False, 'error': "Correo inválido"})
    except Exception as e:
        return jsonify({'modificacion_exitosa': False, 'error': str(e)})

@user.route("/modify_fechanac_cli", methods = ['POST'])
def modify_fechanac_cli():
    try:
        if request.method == 'POST':
            fechanac = request.form['fechanac']
            conexion = obtener_conexion()
            with conexion.cursor() as cur:
                cur.execute("UPDATE clientes SET fecha_nac_cli = %s WHERE id_cli = %s", (fechanac, session['user_id']))
            conexion.commit()
            conexion.close()
            return jsonify({'modificacion_exitosa': True})
    except Exception as e:
        return jsonify({'modificacion_exitosa': False, 'error': str(e)})


@user.route("/modify_apmat_cli", methods = ['POST'])
def modify_apmat_cli():
    try:
        if request.method == 'POST':
            apmat = request.form['apmat']
            conexion = obtener_conexion()
            with conexion.cursor() as cur:
                cur.execute("UPDATE clientes SET ap_mat_cli = %s WHERE id_cli = %s", (apmat, session['user_id']))
            conexion.commit()
            conexion.close()
            return jsonify({'modificacion_exitosa': True})
    except Exception as e:
        return jsonify({'modificacion_exitosa': False, 'error': str(e)})

@user.route("/modify_appat_cli", methods = ['POST'])
def modify_appat_cli():
    try:
        if request.method == 'POST':
            appat = request.form['appat']
            conexion = obtener_conexion()
            with conexion.cursor() as cur:
                cur.execute("UPDATE clientes SET ap_pat_cli = %s WHERE id_cli = %s", (appat, session['user_id']))
            conexion.commit()
            conexion.close()
            return jsonify({'modificacion_exitosa': True})
    except Exception as e:
        return jsonify({'modificacion_exitosa': False, 'error': str(e)})

@user.route("/modify_name_cli", methods = ['POST'])
def modify_name_cli():
    try:
        if request.method == 'POST':
            name = request.form['name']
            conexion = obtener_conexion()
            with conexion.cursor() as cur:
                cur.execute("UPDATE clientes SET nom_cli = %s WHERE id_cli = %s", (name, session['user_id']))
            conexion.commit()
            conexion.close()
            return jsonify({'modificacion_exitosa': True})
    except Exception as e:
        return jsonify({'modificacion_exitosa': False, 'error': str(e)})


