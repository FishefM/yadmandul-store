import os
import bcrypt
import uuid
import re

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