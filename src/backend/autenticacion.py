import os

# Ruta al archivo de usuarios (se crea si no existe)
RUTA_USUARIOS = os.path.join("data", "users.txt")


def registrar_usuario(usuario,
                       contrasena,
                       nombre_completo,
                       rol,
                       fecha_compra,
                       direccion,
                       telefono):
    """
    Registra un nuevo usuario con los campos adicionales:
    fecha_compra, direccion y telefono.
    Devuelve False si el usuario ya existe, True en caso contrario.
    """
    # Asegurar existencia del archivo
    os.makedirs(os.path.dirname(RUTA_USUARIOS), exist_ok=True)
    if not os.path.exists(RUTA_USUARIOS):
        with open(RUTA_USUARIOS, "w", encoding="utf-8"):
            pass

    # Verificar duplicado
    with open(RUTA_USUARIOS, "r", encoding="utf-8") as f:
        for linea in f:
            existente = linea.strip().split(",")[0]
            if usuario == existente:
                return False

    # Escribir nueva línea con todos los campos
    with open(RUTA_USUARIOS, "a", encoding="utf-8") as f:
        f.write(
            f"{usuario},{contrasena},{nombre_completo},{rol},"
            f"{fecha_compra},{direccion},{telefono}\n"
        )
    return True


def verificar_credenciales(usuario, contrasena):
    """
    Verifica usuario y contraseña. Devuelve un diccionario con los datos completos si coincide.
    """
    if not os.path.exists(RUTA_USUARIOS):
        return None

    with open(RUTA_USUARIOS, "r", encoding="utf-8") as f:
        for linea in f:
            partes = linea.strip().split(",")
            if len(partes) == 7:
                numero_serie, pwd, nombre, rol, fecha_compra, direccion, telefono = partes
                if usuario == numero_serie and contrasena == pwd:
                    return {
                        "numero_serie": numero_serie,
                        "password": pwd,
                        "nombre": nombre,
                        "rol": rol,
                        "fecha_compra": fecha_compra,
                        "direccion": direccion,
                        "telefono": telefono
                    }
    return None



def cargar_usuarios():
    """
    Devuelve lista de diccionarios con todos los usuarios,
    incluyendo fecha_compra, direccion y telefono.
    """
    usuarios = []
    try:
        with open(RUTA_USUARIOS, "r", encoding="utf-8") as file:
            for linea in file:
                partes = linea.strip().split(",")
                # Esperamos exactamente 7 campos
                if len(partes) == 7:
                    usuario, contrasena, nombre, rol, fecha_compra, direccion, telefono = partes
                    usuarios.append({
                        "usuario": usuario,
                        "contrasena": contrasena,
                        "nombre": nombre,
                        "rol": rol,
                        "fecha_compra": fecha_compra,
                        "direccion": direccion,
                        "telefono": telefono
                    })
    except FileNotFoundError:
        pass
    return usuarios


def eliminar_usuario(numero_serie):
    """
    Elimina el usuario con el número de serie indicado.
    Devuelve True si se eliminó algún registro, False si no se encontró.
    """
    usuarios = cargar_usuarios()
    nuevos = [u for u in usuarios if u["usuario"] != numero_serie]
    if len(nuevos) == len(usuarios):
        return False

    try:
        with open(RUTA_USUARIOS, "w", encoding="utf-8") as file:
            for u in nuevos:
                file.write(
                    f"{u['usuario']},{u['contrasena']},{u['nombre']},{u['rol']},"
                    f"{u['fecha_compra']},{u['direccion']},{u['telefono']}\n"
                )
        return True
    except Exception:
        return False
