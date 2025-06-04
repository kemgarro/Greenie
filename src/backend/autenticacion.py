import os

RUTA_USUARIOS = os.path.join("data", "users.txt")

def registrar_usuario(usuario, contrasena, nombre_completo, rol):
    if not os.path.exists(RUTA_USUARIOS):
        with open(RUTA_USUARIOS, "w") as f:
            pass

    with open(RUTA_USUARIOS, "r") as f:
        for linea in f:
            existente = linea.strip().split(",")[0]
            if usuario == existente:
                return False

    with open(RUTA_USUARIOS, "a") as f:
        f.write(f"{usuario},{contrasena},{nombre_completo},{rol}\n")
    return True



def verificar_credenciales(usuario, contrasena):
    if not os.path.exists(RUTA_USUARIOS):
        return None  # Nadie puede entrar

    with open(RUTA_USUARIOS, "r") as f:
        for linea in f:
            partes = linea.strip().split(",")
            if len(partes) == 4:
                usr, pwd, nombre, rol = partes
                if usuario == usr and contrasena == pwd:
                    return {"usuario": usr, "nombre": nombre, "rol": rol}
    return None
def cargar_usuarios():
    usuarios = []
    try:
        with open("data/users.txt", "r", encoding="utf-8") as file:
            for linea in file:
                partes = linea.strip().split(",")
                if len(partes) == 4:
                    usuario, contrasena, nombre, rol = partes
                    usuarios.append({
                        "usuario": usuario,
                        "contrasena": contrasena,
                        "nombre": nombre,
                        "rol": rol
                    })
    except FileNotFoundError:
        pass
    return usuarios


def eliminar_usuario(numero_serie):
    usuarios = cargar_usuarios()
    nuevos = [u for u in usuarios if u["usuario"] != numero_serie]
    if len(nuevos) == len(usuarios):
        return False  # No se encontró
    try:
        with open("data/users.txt", "w", encoding="utf-8") as file:
            for u in nuevos:
                file.write(f"{u['usuario']},{u['contrasena']},{u['nombre']},{u['rol']}\n")
        return True
    except Exception:
        return False
