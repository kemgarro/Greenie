import tkinter as tk
from tkinter import ttk, messagebox
from src.backend.autenticacion import registrar_usuario


class RegistroUI:
    def __init__(self, master):
        self.top = tk.Toplevel(master)
        self.top.title("Registro - Greenie")
        self.top.geometry("400x600")
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
                # Selector de rol
        tk.Label(contenedor, text="Rol", fg="white", bg="#096B35").pack(pady=(10, 0))

        self.rol_var = tk.StringVar(value="cliente")

        roles = [("Cliente", "cliente"), ("Administrador", "admin")]
        for texto, valor in roles:
            tk.Radiobutton(
                contenedor,
                text=texto,
                variable=self.rol_var,
                value=valor,
                fg="white",
                bg="#096B35",
                activebackground="#096B35",
                selectcolor="#054B25",
                command=self.actualizar_rol
            ).pack(anchor="w", padx=80)


        self.codigo_frame = tk.Frame(contenedor, bg="#096B35")

        tk.Label(self.codigo_frame, text="Código de acceso", fg="white", bg="#096B35").pack()
        self.codigo_entry = ttk.Entry(self.codigo_frame, width=30)
        self.codigo_entry.pack()



        self.entradas = {}

        for label_texto, clave, *es_clave in campos:
            tk.Label(contenedor, text=label_texto, fg="white", bg="#096B35").pack(pady=(10, 0))
            entrada = ttk.Entry(contenedor, width=30, show="*" if es_clave else "")
            entrada.pack()
            self.entradas[clave] = entrada

        ttk.Button(contenedor, text="Registrarse", command=self.registrar_usuario).pack(pady=20)

    def actualizar_rol(self):
        if self.rol_var.get() == "admin":
            self.codigo_frame.pack(pady=(5, 0))
        else:
            self.codigo_frame.pack_forget()


    def registrar_usuario(self):
        nombre = self.entradas["nombre"].get().strip()
        usuario = self.entradas["usuario"].get().strip()
        pwd = self.entradas["contrasena"].get()
        conf = self.entradas["confirmar"].get()
        rol = self.rol_var.get()

        if not all([nombre, usuario, pwd, conf]):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if pwd != conf:
            messagebox.showerror("Error", "Las contraseñas no coinciden.")
            return

        if rol == "admin":
            codigo = self.codigo_entry.get().strip()
            if codigo != "GREENIE-2025":
                messagebox.showerror("Acceso denegado", "Código de acceso incorrecto para administrador.")
                return

        from src.backend.autenticacion import registrar_usuario as guardar_usuario
        exito = guardar_usuario(usuario, pwd, nombre, rol)

        if exito:
            messagebox.showinfo("Éxito", f"Usuario '{usuario}' registrado correctamente.")
            self.top.destroy()
        else:
            messagebox.showerror("Error", "El nombre de usuario ya está en uso.")
