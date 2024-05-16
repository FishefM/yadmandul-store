from flask import g, session, render_template
from app.db import obtener_conexion
from app.__init__ import create_app
from flask_mysqldb import MySQL

app = create_app()

@app.before_request
def load_user():
    if 'user_id' in session:
        if session['user_type'] == 'cliente':
            conexion = obtener_conexion()
            with conexion.cursor() as cur:                
                cur.execute('SELECT nom_cli, ap_pat_cli, ap_mat_cli, fecha_nac_cli, correo_cli, password_cli, foto_cli FROM clientes WHERE id_cli = %s', (session['user_id'], ))
                user_data = cur.fetchone()
        elif session['user_type'] == 'empleado':
            conexion = obtener_conexion()
            with conexion.cursor() as cur:
                cur.execute('SELECT nom_emp, ap_pat_emp, ap_mat_emp, fec_nac_emp, correo_emp, password_emp, foto_emp FROM empleados WHERE id_emp = %s', (session['user_id'], ))
                user_data = cur.fetchone()
        elif session['user_type'] == 'administrador':
            conexion = obtener_conexion()
            with conexion.cursor() as cur:
                cur.execute('SELECT nom_admin, ap_pat_admin, ap_mat_admin, fec_nac_admin, correo_admin, password_admin, foto_admin FROM administradores WHERE id_admin = %s', (session['user_id'], ))
                user_data = cur.fetchone()
        conexion.close()

        if user_data is not None:
            nom, ap_pat, ap_mat, fecha_nac, correo, password, foto = user_data
            #if(session['user_type'] == 'cliente' and len(nom) > 6): nom = nom[0:6]
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

@app.errorhandler(404)
def page_not_found(e):
    # Si el usuario intenta acceder a una página que no existe, regresa un error 404
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug = True)

