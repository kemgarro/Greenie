import os

RUTA_USUARIOS = os.path.join("data", "users.txt")

def registrar_usuario(usuario, contrasena, nombre_completo):
    if not os.path.exists(RUTA_USUARIOS):
        with open(RUTA_USUARIOS, "w") as f:
            pass

    with open(RUTA_USUARIOS, "r") as f:
        for linea in f:
            existente = linea.strip().split(",")[0]
            if usuario == existente:
                return False

    with open(RUTA_USUARIOS, "a") as f:
        f.write(f"{usuario},{contrasena},{nombre_completo}\n")
    return True

def verificar_credenciales(usuario, contrasena):
    if not os.path.exists(RUTA_USUARIOS):
        return False

    with open(RUTA_USUARIOS, "r") as f:
        for linea in f:
            datos = linea.strip().split(",")
            if len(datos) >= 2:
                if usuario == datos[0] and contrasena == datos[1]:
                    return True
    return False
