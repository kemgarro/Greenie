import tkinter as tk
from tkinter import messagebox, simpledialog

class PerfilFrame(tk.Frame):
    def __init__(self, master, volver_callback, numero_serie):
        super().__init__(master, bg="#FFFFFF")
        self.volver_callback = volver_callback
        self.numero_serie = numero_serie
        self.usuario = self.cargar_usuario_por_serie(numero_serie)
        self.crear_interfaz()

    def cargar_usuario_por_serie(self, serie):
        try:
            with open("data/users.txt", "r", encoding="utf-8") as f:
                for linea in f:
                    datos = linea.strip().split(",")
                    if len(datos) == 7 and datos[0] == serie:
                        return {
                            "nombre": datos[2],
                            "numero_serie": datos[0],
                            "telefono": datos[6],
                            "direccion": datos[5],
                            "fecha_compra": datos[4],
                            "password": datos[1]
                        }
        except FileNotFoundError:
            pass
        return None


    def crear_interfaz(self):
        header = tk.Frame(self, bg="#096B35", height=60)
        header.pack(fill="x")
        tk.Label(header, text="Mi Perfil", font=("Segoe UI", 16, "bold"),
                 fg="white", bg="#096B35").pack(pady=15)

        if not self.usuario:
            tk.Label(self, text="Usuario no encontrado.", bg="#FFFFFF", font=("Segoe UI", 12)).pack(pady=10)
            return

        # Mostrar datos del usuario
        for clave, valor in self.usuario.items():
            if clave != "password":
                tk.Label(self, text=f"{clave.capitalize()}: {valor}", bg="#FFFFFF", font=("Segoe UI", 12)).pack(pady=3)

        # Cambiar contraseña
        tk.Button(self, text="Cambiar Contraseña", bg="#7AC35D", fg="white",
                  font=("Segoe UI", 10), width=20, command=self.cambiar_password).pack(pady=15)

        # Botón Volver
        tk.Button(self, text="Volver", bg="#7AC35D", fg="white",
                  font=("Segoe UI", 10), width=12, command=self.volver_callback).pack(pady=10)

    def cambiar_password(self):
        actual = simpledialog.askstring("Contraseña actual", "Ingrese su contraseña actual:", show="*")
        nueva = simpledialog.askstring("Nueva contraseña", "Ingrese su nueva contraseña:", show="*")
        confirmar = simpledialog.askstring("Confirmar nueva", "Confirme su nueva contraseña:", show="*")

        if not (actual and nueva and confirmar):
            messagebox.showwarning("Campos vacíos", "Debe completar todos los campos.")
            return

        if nueva != confirmar:
            messagebox.showerror("Error", "Las contraseñas no coinciden.")
            return

        if actual != self.usuario["password"]:
            messagebox.showerror("Error", "Contraseña actual incorrecta.")
            return

        # ✅ Actualizar en archivo y en memoria
        if self.actualizar_password_en_archivo(nueva):
            self.usuario["password"] = nueva
            messagebox.showinfo("Éxito", "Contraseña cambiada correctamente.")
        else:
            messagebox.showerror("Error", "No se pudo actualizar la contraseña.")


    def actualizar_usuario_en_archivo(self):
        with open("data/users.txt", "r", encoding="utf-8") as f:
            lineas = f.readlines()

        with open("data/users.txt", "w", encoding="utf-8") as f:
            for linea in lineas:
                datos = linea.strip().split("|")
                if len(datos) >= 6 and datos[1] == self.usuario["serie"]:
                    nueva_linea = "|".join([
                        self.usuario["nombre"],
                        self.usuario["serie"],
                        self.usuario["telefono"],
                        self.usuario["direccion"],
                        self.usuario["fecha_compra"],
                        self.usuario["password"]
                    ])
                    f.write(nueva_linea + "\n")
                else:
                    f.write(linea)

    def actualizar_password_en_archivo(self, nueva_password):
        try:
            with open("data/users.txt", "r", encoding="utf-8") as f:
                lineas = f.readlines()

            with open("data/users.txt", "w", encoding="utf-8") as f:
                for linea in lineas:
                    partes = linea.strip().split(",")
                    if len(partes) == 7 and partes[0] == self.usuario["numero_serie"]:
                        partes[1] = nueva_password  # Actualizamos la contraseña
                        nueva_linea = ",".join(partes)
                        f.write(nueva_linea + "\n")
                    else:
                        f.write(linea)
            return True
        except Exception as e:
            print(f"[Error] No se pudo actualizar la contraseña: {e}")
            return False
