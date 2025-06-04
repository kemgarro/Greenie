
import tkinter as tk
from tkinter import ttk, messagebox
from src.backend.autenticacion import registrar_usuario, cargar_usuarios, eliminar_usuario

class UsuariosFrame(tk.Frame):
    def __init__(self, master, volver_callback):
        super().__init__(master, bg="#FFFFFF")
        self.volver_callback = volver_callback
        self.crear_interfaz()
        self.cargar_tabla()

    def crear_interfaz(self):
        header = tk.Frame(self, bg="#096B35", height=60)
        header.pack(fill="x")
        tk.Label(header, text="Gestión de Usuarios", font=("Segoe UI", 16, "bold"),
                 fg="white", bg="#096B35").pack(pady=15)

        contenedor = tk.Frame(self, bg="#FFFFFF")
        contenedor.pack(pady=10)

        self.campos = {}
        for campo in ["Nombre", "Número de Serie", "Contraseña", "Rol"]:
            tk.Label(contenedor, text=campo, bg="#FFFFFF", anchor="w").pack(fill="x", padx=40)
            entrada = ttk.Entry(contenedor, width=30, show="*" if "Contraseña" in campo else "")
            entrada.pack(pady=5)
            self.campos[campo.lower()] = entrada

        self.campos["rol"].destroy()
        self.campos["rol"] = ttk.Combobox(contenedor, values=["cliente", "admin"], state="readonly")
        self.campos["rol"].pack(pady=5)
        self.campos["rol"].set("cliente")

        ttk.Button(contenedor, text="Registrar Usuario", command=self.registrar).pack(pady=10)

        self.tabla = ttk.Treeview(self, columns=("Nombre", "Serie", "Rol"), show="headings", height=6)
        for col in self.tabla["columns"]:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=120, anchor="center")
        self.tabla.pack(pady=10)

        ttk.Button(self, text="Eliminar Usuario Seleccionado", command=self.eliminar).pack(pady=5)

        tk.Button(self, text="Volver", bg="#7AC35D", fg="white",
                  font=("Segoe UI", 10), width=12,
                  command=self.volver_callback).pack(pady=10)

    def registrar(self):
        nombre = self.campos["nombre"].get().strip()
        usuario = self.campos["número de serie"].get().strip()
        contrasena = self.campos["contraseña"].get()
        rol = self.campos["rol"].get()

        if not all([nombre, usuario, contrasena, rol]):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if registrar_usuario(usuario, contrasena, nombre, rol):
            messagebox.showinfo("Éxito", f"Usuario '{usuario}' registrado.")
            self.cargar_tabla()
            for campo in self.campos.values():
                campo.delete(0, tk.END)
            self.campos["rol"].set("cliente")
        else:
            messagebox.showerror("Error", "El número de serie ya está registrado.")

    def cargar_tabla(self):
        for row in self.tabla.get_children():
            self.tabla.delete(row)
        usuarios = cargar_usuarios()
        for user in usuarios:
            self.tabla.insert("", "end", values=(user["nombre"], user["usuario"], user["rol"]))

    def eliminar(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showerror("Error", "Seleccione un usuario para eliminar.")
            return
        datos = self.tabla.item(seleccion[0])["values"]
        numero_serie = datos[1]
        if eliminar_usuario(numero_serie):
            messagebox.showinfo("Eliminado", f"Usuario '{numero_serie}' eliminado.")
            self.cargar_tabla()
        else:
            messagebox.showerror("Error", "No se pudo eliminar el usuario.")
