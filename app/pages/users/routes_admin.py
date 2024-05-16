from flask import request, jsonify, Blueprint, session, url_for, redirect, render_template, g
from app.pages_fun import *
from app.db import obtener_conexion

admin = Blueprint('admin',__name__)

@admin.route('/administradores')
def administradores():
    if session:
        # if session['user_type'] == 'cliente' or session['user_type'] == 'empleado':
        #     return 'Tu no deberias de estar aqui My friend'
        if session['user_type'] == 'cliente':
            return redirect(url_for('index.goToIndex'))
        elif session['user_type'] == 'empleado':
            return redirect(url_for("employee.empleados"))
    else: return redirect(url_for('index.goToIndex'))
    conexion = obtener_conexion()
    with conexion.cursor() as cur:
        cur.execute("SELECT id_emp, foto_emp, CONCAT(nom_emp, ' ', ap_pat_emp, ' ', ap_mat_emp) as 'Nombre completo', fec_nac_emp, correo_emp, estado_emp FROM empleados")
        empleados = cur.fetchall()
        cur.execute("SELECT id_cli, foto_cli, CONCAT(nom_cli, ' ', ap_pat_cli, ' ', ap_mat_cli) as 'Nombre completo', fecha_nac_cli, correo_cli, estado_cli FROM clientes")
        clientes = cur.fetchall()
        cur.execute("SELECT * FROM proveedores")
        proveedores = cur.fetchall()
    conexion.close()
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
        clientes = list_clientes,
        proveedores = proveedores
    )

@admin.route("/modify_prov/<int:id>", methods = ['POST'])
def modify_prov(id):
    if session and session['user_type'] == 'administrador':
        try:
            if request.method == 'POST':
                nom_prov = request.form['nom_prov']
                ap_pat_prov = request.form['ap_pat_prov']
                ap_mat_prov = request.form['ap_mat_prov']
                correo_prov = request.form['correo_prov']
                tel_prov = request.form['tel_prov']
                conexion = obtener_conexion()
                with conexion.cursor() as cur:
                    cur.execute("UPDATE proveedores SET nom_prov = %s, ap_pat_prov = %s, ap_mat_prov = %s, correo_prov = %s, tel_prov = %s WHERE id_prov = %s", (nom_prov, ap_pat_prov, ap_mat_prov, correo_prov, tel_prov, id))
                conexion.commit()
                return redirect(url_for('admin.administradores'))
        except Exception as e:
            return jsonify({'modificacion_exitosa': False, 'error': str(e)})


@admin.route("/insert_proveedores", methods = ['POST'])
def insert_proveedores():
    if session and session['user_type'] == 'administrador':
        try:
            if request.method == 'POST':
                nom_prov = request.form['nom_prov']
                ap_pat_prov = request.form['ap_pat_prov']
                ap_mat_prov = request.form['ap_mat_prov']
                correo_prov = request.form['correo_prov']
                tel_prov = request.form['tel_prov']
                conexion = obtener_conexion()
                with conexion.cursor() as cur:
                    cur.execute("INSERT INTO proveedores VALUES (default, %s, %s, %s, %s, %s)", (nom_prov, ap_pat_prov, ap_mat_prov, correo_prov, tel_prov))
                conexion.commit()
                return jsonify({'modificacion_exitosa': True, 'info': "Registro completado con éxito"})
        except Exception as e:
            return jsonify({'modificacion_exitosa': False, 'error': str(e)})
    else: 
        return "No tienes permisos para realizar esta acción"

@admin.route("/upload_img_admin", methods = ['POST'])
def upload_img_admin():
    try:
        if request.method == 'POST':
            conexion = obtener_conexion()
            with conexion.cursor() as cur:
                cur.execute("SELECT foto_admin FROM administradores WHERE id_admin = %s", (session['user_id'], ))
                current_photo = cur.fetchone()
            conexion.close()
            if current_photo[0] != '': os.remove('static/' + current_photo[0])
            file = request.files['photo']
            unique_file = generar_nombre_unico(file.filename)
            url_photo = 'static/uploads/admins/' + unique_file
            file.save(url_photo)
            url_photo = 'uploads/admins/' + unique_file
            conexion = obtener_conexion()
            with conexion.cursor() as cur:
                cur.execute("UPDATE administradores SET foto_admin = %s WHERE id_admin = %s", (url_photo, session['user_id']))
            conexion.commit()
            conexion.close()
            return jsonify({'modificacion_exitosa': True})
    except Exception as e:
        return jsonify({'modificacion_exitosa': False, 'error': str(e)})
    
@admin.route('/dar_de_alta_cli/<int:id>', methods = ['POST'])
def dar_de_alta_cli(id):
    if session and session['user_type'] == 'administrador':
        conexion = obtener_conexion()
        with conexion.cursor() as cur:
            cur.execute("UPDATE clientes SET estado_cli = true WHERE id_cli = %s", (id, ))
        conexion.commit()
        conexion.close()
        return redirect(url_for('admin.administradores'))
    else:
        return "No tienes permisos para realizar esta acción"

@admin.route('/dar_de_baja_cli/<int:id>', methods = ['POST'])
def dar_de_baja_cli(id):
    if session and session['user_type'] == 'administrador':
        conexion = obtener_conexion()
        with conexion.cursor() as cur:
            cur.execute("UPDATE clientes SET estado_cli = false WHERE id_cli = %s", (id, ))
        conexion.commit()
        conexion.close()
        return redirect(url_for('admin.administradores'))
    else:
        return "No tienes permisos para realizar esta acción"


@admin.route('/dar_de_baja_emp/<int:id>', methods = ['POST'])
def dar_de_baja_emp(id):
    if session and session['user_type'] == 'administrador':
        conexion = obtener_conexion()
        with conexion.cursor() as cur:
            cur.execute("UPDATE empleados SET estado_emp = false WHERE id_emp = %s", (id, ))
        conexion.commit()
        conexion.close()
        return redirect(url_for('admin.administradores'))
    else:
        return "No tienes permisos para realizar esta acción"

@admin.route('/dar_de_alta_emp/<int:id>', methods = ['POST'])
def dar_de_alta_emp(id):
    if session and session['user_type'] == 'administrador':
        conexion = obtener_conexion()
        with conexion.cursor() as cur:
            cur.execute("UPDATE empleados SET estado_emp = true WHERE id_emp = %s", (id, ))
        conexion.commit()
        conexion.close()
        return redirect(url_for('admin.administradores'))
    else:
        return "No tienes permisos para realizar esta acción"
    
@admin.route("/modify_password_admin", methods = ['POST'])
def modify_password_admin():
    try:
        if request.method == 'POST':
            password = encrypt_password(request.form['password'])
            conexion = obtener_conexion()
            with conexion.cursor() as cur:
                cur.execute("UPDATE administradores SET password_admin = %s WHERE id_admin = %s", (password, session['user_id']))
            conexion.commit()
            conexion.close()
            return jsonify({'modificacion_exitosa': True})
    except Exception as e:
        return jsonify({'modificacion_exitosa': False, 'error': str(e)})

@admin.route("/modify_correo_admin", methods = ['POST'])
def modify_correo_admin():
    try:
        if request.method == 'POST':
            correo = request.form['correo']
            if is_admin(correo):
                conexion = obtener_conexion()
                with conexion.cursor() as cur:
                    cur.execute("UPDATE administradores SET correo_admin = %s WHERE id_admin = %s", (correo, session['user_id']))
                conexion.commit()
                conexion.close()
                return jsonify({'modificacion_exitosa': True})
            else: return jsonify({'modificacion_exitosa': False, 'error': "Correo inválido"})
    except Exception as e:
        return jsonify({'modificacion_exitosa': False, 'error': str(e)})

@admin.route("/modify_fechanac_admin", methods = ['POST'])
def modify_fechanac_admin():
    try:
        if request.method == 'POST':
            fechanac = request.form['fechanac']
            conexion = obtener_conexion()
            with conexion.cursor() as cur:
                cur.execute("UPDATE administradores SET fec_nac_admin = %s WHERE id_admin = %s", (fechanac, session['user_id']))
            conexion.commit()
            conexion.close()
            return jsonify({'modificacion_exitosa': True})
    except Exception as e:
        return jsonify({'modificacion_exitosa': False, 'error': str(e)})


@admin.route("/modify_apmat_admin", methods = ['POST'])
def modify_apmat_admin():
    try:
        if request.method == 'POST':
            apmat = request.form['apmat']
            conexion = obtener_conexion()
            with conexion.cursor() as cur:
                cur.execute("UPDATE administradores SET ap_mat_admin = %s WHERE id_admin = %s", (apmat, session['user_id']))
            conexion.commit()
            conexion.close()
            return jsonify({'modificacion_exitosa': True})
    except Exception as e:
        return jsonify({'modificacion_exitosa': False, 'error': str(e)})


@admin.route("/modify_appat_admin", methods = ['POST'])
def modify_appat_admin():
    try:
        if request.method == 'POST':
            appat = request.form['appat']
            conexion = obtener_conexion()
            with conexion.cursor() as cur:
                cur.execute("UPDATE administradores SET ap_pat_admin = %s WHERE id_admin = %s", (appat, session['user_id']))
            conexion.commit()
            conexion.close()
            return jsonify({'modificacion_exitosa': True})
    except Exception as e:
        return jsonify({'modificacion_exitosa': False, 'error': str(e)})


@admin.route("/modify_name_admin", methods = ['POST'])
def modify_name_admin():
    try:
        if request.method == 'POST':
            name = request.form['name']
            conexion = obtener_conexion()
            with conexion.cursor() as cur:
                cur.execute("UPDATE administradores SET nom_admin = %s WHERE id_admin = %s", (name, session['user_id']))
            conexion.commit()
            conexion.close()
            return jsonify({'modificacion_exitosa': True})
    except Exception as e:
        return jsonify({'modificacion_exitosa': False, 'error': str(e)})
