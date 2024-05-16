from flask import Flask
from app.index import index
from app.users.routes_admin import admin
from app.users.routes_user import user
from app.users.routes_employe import employee
from app.users.routes_general import general
from app.pages.routes_pages import pagesR


def create_app():
    app = Flask(__name__)
    app.secret_key = 'jinofvx' # La clave es aleatoria, solo es para que funcione la sesión

    app.register_blueprint(index)
    app.register_blueprint(user)
    app.register_blueprint(admin)
    app.register_blueprint(employee)
    app.register_blueprint(pagesR)
    app.register_blueprint(general)


    return app

