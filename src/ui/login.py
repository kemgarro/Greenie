import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
from src.ui.registro import RegistroUI
from src.backend.autenticacion import verificar_credenciales
from src.ui.panel_admin import PanelAdmin
from src.ui.panel_cliente import PanelCliente
from src.hardware.serial_manager import SerialManager

serial_manager = SerialManager()

class LoginUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Greenie - Inicio de sesión")
        self.root.geometry("400x500")
        self.root.configure(bg="#F7F7F7")
        self.root.resizable(False, False)

        self.configurar_estilos()
        self.crear_widgets()

    def configurar_estilos(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TEntry",
                        foreground="black",
                        fieldbackground="white",
                        padding=10)

        style.configure("TButton",
                        foreground="white",
                        background="#7AC35D",
                        font=("Segoe UI", 10, "bold"),
                        padding=10)
        style.map("TButton", background=[('active', '#7AC35D')])

    def crear_widgets(self):
        contenedor = tk.Frame(self.root, bg="#F7F7F7")
        contenedor.pack(expand=True, pady=30)

        # Texto "Bienvenido a"
        tk.Label(contenedor,
                text="Bienvenido a",
                font=("Segoe UI", 14),
                fg="#555",
                bg="#F7F7F7").pack(pady=(0, 5))

        # Logo de Greenie
        ruta_logo = os.path.join("assets", "logos", "logo.png")
        if os.path.exists(ruta_logo):
            imagen = Image.open(ruta_logo).resize((140, 120))
            self.logo = ImageTk.PhotoImage(imagen)
            tk.Label(contenedor, image=self.logo, bg="#F7F7F7").pack(pady=(0, 25))

        # Entradas
        tk.Label(contenedor, text="Usuario:", bg="#F7F7F7").pack(anchor="w", padx=40)
        self.usuario = ttk.Entry(contenedor, width=30)
        self.usuario.pack(pady=(0, 10))

        tk.Label(contenedor, text="Contraseña:", bg="#F7F7F7").pack(anchor="w", padx=40)
        self.contrasena = ttk.Entry(contenedor, width=30, show="*")
        self.contrasena.pack(pady=(0, 20))

        ttk.Separator(contenedor, orient='horizontal').pack(fill='x', padx=40, pady=10)

        ttk.Button(contenedor, text="INICIAR SESIÓN", command=self.iniciar_sesion).pack(pady=10, ipadx=20)

        # Enlace de registro
        enlace = tk.Frame(contenedor, bg="#F7F7F7")
        enlace.pack(pady=(10, 0))

    def iniciar_sesion(self):
        user = self.usuario.get().strip()
        pwd = self.contrasena.get().strip()

        datos = verificar_credenciales(user, pwd)

        if datos:
            messagebox.showinfo("Éxito", f"¡Bienvenido, {datos['nombre']}!")
            self.root.destroy()
            if datos["rol"] == "admin":
                PanelAdmin()
            else:
                PanelCliente(user, serial_manager)
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")

    def abrir_registro(self):
        RegistroUI(self.root)

    def mostrar(self):
        self.root.mainloop()

# Para pruebas locales
if __name__ == "__main__":
    app = LoginUI()
    app.mostrar()
