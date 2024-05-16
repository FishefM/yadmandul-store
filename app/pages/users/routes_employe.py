from flask import request, jsonify, Blueprint, session, url_for, redirect, render_template, g
from app.pages_fun import *
from app.db import obtener_conexion

employee = Blueprint('employee',__name__)

@employee.route('/empleados')
def empleados():
    if session:
        # if session['user_type'] == 'cliente' or session['user_type'] == 'administrador':
        #     return 'Tu no deberias de estar aqui My friend'
        if session['user_type'] == 'cliente':
            return redirect(url_for('index.goToIndex'))
        elif session['user_type'] == 'administrador':
            return redirect(url_for('admin.administradores'))
    else: return redirect(url_for('index.goToIndex'))
    conexion = obtener_conexion()
    with conexion.cursor() as cur:
        cur.execute("SELECT id_prod, id_prov, foto_prod, nom_prod, tipo_prod, precio_prod, cantidad_prod, estado_prod FROM productos")
        productos = cur.fetchall()
        cur.execute("SELECT id_prov, CONCAT(nom_prov, ' ', ap_pat_prov, ' ', ap_mat_prov) FROM proveedores")
        proveedores = cur.fetchall()
    conexion.close()

    list_productos = [list(producto) for producto in productos]
    for producto in list_productos:
        if producto[2] == '': producto[2] = "assets/img/product.png"
    
    return render_template(
        'cuentaEmpleados.html', 
        user = g.user, 
        productos = list_productos,
        proveedores = proveedores,
        tipos_prod = ['dulces', 'bebidas', 'jarcieria', 'cinstantanea']
    )

@employee.route("/modify_prod/<int:id>", methods = ['POST'])
def modify_prod(id):
    if session and session['user_type'] == 'empleado':
        try:
            if request.method == 'POST':
                id_prov = request.form['id_prov']
                conexion = obtener_conexion()
                with conexion.cursor() as cur:
                    cur.execute("SELECT foto_prod FROM productos WHERE id_prod = %s", (id, ))
                    current_photo = cur.fetchone()
                conexion.close()
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
                conexion = obtener_conexion()
                with conexion.cursor() as cur:
                    cur.execute("UPDATE productos SET id_prov = %s, foto_prod = %s, nom_prod = %s, tipo_prod = %s, precio_prod = %s, cantidad_prod = %s WHERE id_prod = %s", (id_prov, url_photo, nom_prod, tipo_prod, precio_prod, cantidad_prod, id))
                conexion.commit()
                return redirect(url_for('employee.empleados'))
        except Exception as e:
            return jsonify({'modificacion_exitosa': False, 'error': str(e)})

@employee.route("/insert_products", methods = ['POST'])
def insert_products():
    if session and session['user_type'] == 'empleado':
        try:
            if request.method == 'POST':
                nom_prod = request.form['nom_prod']
                tipo_prod = request.form['tipo_prod']
                precio_prod = request.form['precio_prod']
                cantidad_prod = request.form['cantidad_prod']
                id_prov = request.form['id_prov']
                file = request.files['foto_prod']
                unique_file = generar_nombre_unico(file.filename)
                url_photo = 'static/uploads/img_products/' + unique_file
                file.save(url_photo)
                url_photo = 'uploads/img_products/' + unique_file
                conexion = obtener_conexion()
                with conexion.cursor() as cur:
                    cur.execute("INSERT INTO productos VALUES (default, %s, %s, %s, %s, true, %s, %s)", (nom_prod, tipo_prod, precio_prod, cantidad_prod, url_photo, id_prov))
                conexion.commit()
                return jsonify({'modificacion_exitosa': True, 'info': "Registro completado con éxito"})
        except Exception as e:
            return jsonify({'modificacion_exitosa': False, 'error': str(e)})
    else:
        return "No tienes permisos para realizar esta acción"

@employee.route('/dar_de_alta_prod/<int:id>', methods = ['POST'])
def dar_de_alta_prod(id):
    if session and session['user_type'] == 'empleado':
        conexion = obtener_conexion()
        with conexion.cursor() as cur:
            cur.execute("UPDATE productos SET estado_prod = true WHERE id_prod = %s", (id, ))
        conexion.commit()
        conexion.close()
        return redirect(url_for('empleados'))
    else:
        return "No tienes permisos para realizar esta acción"

@employee.route('/dar_de_baja_prod/<int:id>', methods = ['POST'])
def dar_de_baja_prod(id):
    if session and session['user_type'] == 'empleado':
        conexion = obtener_conexion()
        with conexion.cursor() as cur:
            cur.execute("UPDATE productos SET estado_prod = false WHERE id_prod = %s", (id, ))
        conexion.commit()
        conexion.close()
        return redirect(url_for('empleados'))
    else:
        return "No tienes permisos para realizar esta acción"

@employee.route("/upload_img_employee", methods = ['POST'])
def upload_img_employee():
    try:
        if request.method == 'POST':
            conexion = obtener_conexion()
            with conexion.cursor() as cur:
                cur.execute("SELECT foto_emp FROM empleados WHERE id_emp = %s", (session['user_id'], ))
                current_photo = cur.fetchone()
            conexion.close()
            if current_photo[0] != '': os.remove('static/' + current_photo[0])
            file = request.files['photo']
            unique_file = generar_nombre_unico(file.filename)
            url_photo = 'static/uploads/empleados/' + unique_file
            file.save(url_photo)
            url_photo = 'uploads/empleados/' + unique_file
            conexion = obtener_conexion()
            with conexion.cursor() as cur:
                cur.execute("UPDATE empleados SET foto_emp = %s WHERE id_emp = %s", (url_photo, session['user_id']))
            conexion.commit()
            conexion.close()
            return jsonify({'modificacion_exitosa': True})
    except Exception as e:
        return jsonify({'modificacion_exitosa': False, 'error': str(e)})

@employee.route("/modify_password_employee", methods = ['POST'])
def modify_password_employee():
    try:
        if request.method == 'POST':
            password = encrypt_password(request.form['password'])
            conexion = obtener_conexion()
            with conexion.cursor() as cur:
                cur.execute("UPDATE empleados SET password_emp = %s WHERE id_emp = %s", (password, session['user_id']))
            conexion.commit()
            conexion.close()
            return jsonify({'modificacion_exitosa': True})
    except Exception as e:
        return jsonify({'modificacion_exitosa': False, 'error': str(e)})

@employee.route("/modify_correo_employee", methods = ['POST'])
def modify_correo_employee():
    try:
        if request.method == 'POST':
            correo = request.form['correo']
            if is_emp(correo):
                conexion = obtener_conexion()
                with conexion.cursor() as cur:
                    cur.execute("UPDATE empleados SET correo_emp = %s WHERE id_emp = %s", (correo, session['user_id']))
                conexion.commit()
                conexion.close()
                return jsonify({'modificacion_exitosa': True})
            else: return jsonify({'modificacion_exitosa': False, 'error': "Correo inválido"})

    except Exception as e:
        return jsonify({'modificacion_exitosa': False, 'error': str(e)})

@employee.route("/modify_fechanac_employee", methods = ['POST'])
def modify_fechanac_employee():
    try:
        if request.method == 'POST':
            fechanac = request.form['fechanac']
            conexion = obtener_conexion()
            with conexion.cursor() as cur:
                cur.execute("UPDATE empleados SET fec_nac_emp = %s WHERE id_emp = %s", (fechanac, session['user_id']))
                conexion.commit()
                conexion.close()
            return jsonify({'modificacion_exitosa': True})
    except Exception as e:
        return jsonify({'modificacion_exitosa': False, 'error': str(e)})

@employee.route("/modify_apmat_employee", methods = ['POST'])
def modify_apmat_employee():
    try:
        if request.method == 'POST':
            apmat = request.form['apmat']
            conexion = obtener_conexion()
            with conexion.cursor() as cur:
                cur.execute("UPDATE empleados SET ap_mat_emp = %s WHERE id_emp = %s", (apmat, session['user_id']))
            conexion.commit()
            conexion.close()
            return jsonify({'modificacion_exitosa': True})
    except Exception as e:
        return jsonify({'modificacion_exitosa': False, 'error': str(e)})
    
@employee.route("/modify_appat_employee", methods = ['POST'])
def modify_appat_employee():
    try:
        if request.method == 'POST':
            appat = request.form['appat']
            conexion = obtener_conexion()
            with conexion.cursor() as cur:
                cur.execute("UPDATE empleados SET ap_pat_emp = %s WHERE id_emp = %s", (appat, session['user_id']))
            conexion.commit()
            conexion.close()
            return jsonify({'modificacion_exitosa': True})
    except Exception as e:
        return jsonify({'modificacion_exitosa': False, 'error': str(e)})



@employee.route("/modify_name_employee", methods = ['POST'])
def modify_name_employee():
    try:
        if request.method == 'POST':
            name = request.form['name']
            conexion = obtener_conexion()
            with conexion.cursor() as cur:
                cur.execute("UPDATE empleados SET nom_emp = %s WHERE id_emp = %s", (name, session['user_id']))
            conexion.commit()
            conexion.close()
            return jsonify({'modificacion_exitosa': True})
    except Exception as e:
        return jsonify({'modificacion_exitosa': False, 'error': str(e)})



