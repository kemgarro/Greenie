import os

# Ruta al archivo de usuarios
RUTA_USUARIOS = os.path.join("data", "users.txt")


def registrar_usuario(usuario,
                       contrasena,
                       nombre_completo,
                       rol,
                       fecha_compra,
                       direccion,
                       telefono):
    """
    Registra un nuevo usuario. 
    Si es admin, se usa el nombre como usuario. 
    Si es cliente, se usa el número de serie como usuario.
    """
    os.makedirs(os.path.dirname(RUTA_USUARIOS), exist_ok=True)
    if not os.path.exists(RUTA_USUARIOS):
        with open(RUTA_USUARIOS, "w", encoding="utf-8"):
            pass

    # Elegir qué campo se registra como "usuario"
    if rol == "admin":
        usuario = nombre_completo.strip()
    else:
        usuario = str(usuario).strip()

    # Verificar duplicado
    with open(RUTA_USUARIOS, "r", encoding="utf-8") as f:
        for linea in f:
            existente = linea.strip().split(",")[0].strip()
            if usuario == existente:
                return False

    # Registrar al usuario
    with open(RUTA_USUARIOS, "a", encoding="utf-8") as f:
        f.write(
            f"{usuario},{contrasena},{nombre_completo},{rol},"
            f"{fecha_compra},{direccion},{telefono}\n"
        )
    return True


def verificar_credenciales(usuario, contrasena):
    """
    Verifica usuario y contraseña. Retorna los datos si coincide.
    """
    if not os.path.exists(RUTA_USUARIOS):
        return None

    usuario = str(usuario).strip()
    contrasena = str(contrasena).strip()

    with open(RUTA_USUARIOS, "r", encoding="utf-8") as f:
        for linea in f:
            partes = linea.strip().split(",")
            if len(partes) == 7:
                numero_serie, pwd, nombre, rol, fecha_compra, direccion, telefono = [p.strip() for p in partes]
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
    Carga todos los usuarios registrados como una lista de diccionarios.
    """
    usuarios = []
    try:
        with open(RUTA_USUARIOS, "r", encoding="utf-8") as file:
            for linea in file:
                partes = linea.strip().split(",")
                if len(partes) == 7:
                    usuario, contrasena, nombre, rol, fecha_compra, direccion, telefono = [p.strip() for p in partes]
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
    Elimina un usuario por su identificador registrado. Devuelve True si fue eliminado.
    """
    numero_serie = str(numero_serie).strip()
    usuarios = cargar_usuarios()

    nuevos = []
    eliminado = False
    for u in usuarios:
        if u["usuario"].strip() != numero_serie:
            nuevos.append(u)
        else:
            eliminado = True
            print(f"[INFO] Usuario eliminado: {u['usuario']}")

    if not eliminado:
        print(f"[WARN] Usuario '{numero_serie}' no encontrado.")
        return False

    try:
        with open(RUTA_USUARIOS, "w", encoding="utf-8") as file:
            for u in nuevos:
                file.write(
                    f"{u['usuario']},{u['contrasena']},{u['nombre']},{u['rol']}," +
                    f"{u['fecha_compra']},{u['direccion']},{u['telefono']}\n"
                )
        print(f"[SUCCESS] Usuario '{numero_serie}' eliminado correctamente.")
        return True
    except Exception as e:
        print(f"[ERROR] No se pudo escribir el archivo: {e}")
        return False
