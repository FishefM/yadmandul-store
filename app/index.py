from app.db import obtener_conexion
from flask import render_template, Blueprint,g



index = Blueprint('index',__name__, url_prefix= "/")

@index.route("/")
def goToIndex():
    conexion = obtener_conexion()
    with conexion.cursor() as cur:
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
    conexion.close()
    return render_template(
        "index.html", 
        bebidas = bebidas, 
        dulces = dulces, 
        jarcieria = jarcieria,
        comidas = comidas,
        user = g.user
    )



