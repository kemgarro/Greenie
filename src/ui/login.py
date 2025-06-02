import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from src.ui.registro import RegistroUI
from src.backend.autenticacion import verificar_credenciales

class LoginUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Greenie - Inicio de sesión")
        self.root.geometry("400x600")
        self.root.configure(bg="#096B35")
        self.root.resizable(False, False)

        self.configurar_estilos()
        self.crear_widgets()

    def configurar_estilos(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TEntry",
                        foreground="white",
                        fieldbackground="#054B25",
                        background="#054B25",
                        padding=10,
                        borderwidth=0)
        
        style.configure("TButton",
                        foreground="white",
                        background="#7AC35D",
                        font=("Segoe UI", 10, "bold"),
                        padding=10)
        
        style.map("TButton",
                  background=[('active', '#65a24c')])

    def crear_widgets(self):
        contenedor = tk.Frame(self.root, bg="#096B35")
        contenedor.pack(expand=True)

        # Logo
        ruta_logo = os.path.join("assets", "logos", "logo.png")
        if os.path.exists(ruta_logo):
            imagen = Image.open(ruta_logo).resize((70, 70))
            self.logo = ImageTk.PhotoImage(imagen)
            tk.Label(contenedor, image=self.logo, bg="#096B35").pack(pady=(20, 10))

        # Título Greenie
        tk.Label(contenedor,
                 text="Greenie",
                 font=("Segoe UI", 24, "bold"),
                 fg="white",
                 bg="#096B35").pack()

        # Subtítulo
        tk.Label(contenedor,
                 text="Bienvenido a Greenie",
                 font=("Segoe UI", 12),
                 fg="white",
                 bg="#096B35").pack(pady=(10, 30))

        # Campos de entrada
        self.usuario = ttk.Entry(contenedor, width=30)
        self.usuario.insert(0, "Usuario")
        self.usuario.pack(pady=10)

        self.contrasena = ttk.Entry(contenedor, width=30, show="*")
        self.contrasena.insert(0, "Contraseña")
        self.contrasena.pack(pady=10)

        # Botón de iniciar sesión
        ttk.Button(contenedor,
                   text="INICIAR SESIÓN",
                   command=self.iniciar_sesion,
                   style="TButton").pack(pady=20)

        # Enlace para registro
        abajo = tk.Frame(contenedor, bg="#096B35")
        abajo.pack(pady=(30, 10))

        
        tk.Button(abajo,
                  text="Registrarse",
                  font=("Segoe UI", 9, "underline"),
                  fg="#7AC35D",
                  bg="#096B35",
                  borderwidth=0,
                  cursor="hand2",
                  command=self.abrir_registro).pack(side="left")

    def iniciar_sesion(self):
        user = self.usuario.get().strip()
        pwd = self.contrasena.get().strip()

        if verificar_credenciales(user, pwd):
            messagebox.showinfo("Éxito", f"¡Bienvenido, {user}!")
            self.root.destroy()
            # Aquí podrías redirigir al panel correcto
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")

    def abrir_registro(self):
        messagebox.showinfo("Registro", "Aquí se abriría la ventana de registro")

    def mostrar(self):
        self.root.mainloop()


    def abrir_registro(self):
        RegistroUI(self.root)


# Para pruebas
if __name__ == "__main__":
    app = LoginUI()
    app.mostrar()
