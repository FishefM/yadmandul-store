from flask import Blueprint, render_template, redirect, url_for, g, session

pagesR = Blueprint('pagesR',__name__)

@pagesR.route('/contacto')
def contacto():
    return render_template('contacto.html')

@pagesR.route('/login')
def inicio_sesion():
    if g.user:
        return redirect(url_for('index.goToIndex'))
    return render_template('inicioSesionClientes.html')

@pagesR.route("/logout")
def logout():
    session.pop('user_id', None)
    session.pop('user_type', None)
    g.user = None
    return redirect(url_for('pagesR.inicio_sesion'))

