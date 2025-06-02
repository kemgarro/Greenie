import tkinter as tk
from tkinter import ttk, messagebox
from src.backend.autenticacion import registrar_usuario


class RegistroUI:
    def __init__(self, master):
        self.top = tk.Toplevel(master)
        self.top.title("Registro - Greenie")
        self.top.geometry("400x400")
        self.top.configure(bg="#096B35")
        self.top.resizable(False, False)
        self.top.grab_set()  # Bloquea ventana principal

        self.configurar_estilos()
        self.crear_widgets()

    def configurar_estilos(self):
        style = ttk.Style(self.top)
        style.theme_use("clam")

        style.configure("TEntry",
                        foreground="white",
                        fieldbackground="#054B25",
                        background="#054B25",
                        padding=10)

        style.configure("TButton",
                        foreground="white",
                        background="#7AC35D",
                        font=("Segoe UI", 10, "bold"),
                        padding=10)

    def crear_widgets(self):
        contenedor = tk.Frame(self.top, bg="#096B35")
        contenedor.pack(expand=True, pady=20)

        campos = [
            ("Nombre completo", "nombre"),
            ("Usuario", "usuario"),
            ("Contraseña", "contrasena", True),
            ("Confirmar contraseña", "confirmar", True)
        ]

        self.entradas = {}

        for label_texto, clave, *es_clave in campos:
            tk.Label(contenedor, text=label_texto, fg="white", bg="#096B35").pack(pady=(10, 0))
            entrada = ttk.Entry(contenedor, width=30, show="*" if es_clave else "")
            entrada.pack()
            self.entradas[clave] = entrada

        ttk.Button(contenedor, text="Registrarse", command=self.registrar_usuario).pack(pady=20)

    def registrar_usuario(self):
        nombre = self.entradas["nombre"].get().strip()
        usuario = self.entradas["usuario"].get().strip()
        pwd = self.entradas["contrasena"].get()
        conf = self.entradas["confirmar"].get()

        if not all([nombre, usuario, pwd, conf]):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if pwd != conf:
            messagebox.showerror("Error", "Las contraseñas no coinciden.")
            return

        exito = registrar_usuario(usuario, pwd, nombre)

        if exito:
            messagebox.showinfo("Éxito", f"Usuario '{usuario}' registrado correctamente.")
            self.top.destroy()
        else:
            messagebox.showerror("Error", "El nombre de usuario ya está en uso.")

