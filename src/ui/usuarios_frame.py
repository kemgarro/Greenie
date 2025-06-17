import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from src.backend.autenticacion import (
    registrar_usuario, cargar_usuarios, eliminar_usuario
)

class UsuariosFrame(tk.Frame):
    def __init__(self, master, volver_callback):
        try:
            master.geometry("1000x650")
            master.minsize(900, 600)
        except Exception:
            pass
        super().__init__(master, bg="#F7F7F7")
        self.volver_callback = volver_callback
        self.crear_interfaz()
        self.cargar_tabla()

    def crear_interfaz(self):
        header = tk.Frame(self, bg="#096B35", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(
            header,
            text="Gestión de Usuarios",
            font=("Segoe UI", 18, "bold"),
            fg="white",
            bg="#096B35"
        ).pack(expand=True)

        form_frame = tk.Frame(self, bg="#F7F7F7")
        form_frame.pack(padx=20, pady=10, fill="x")

        self.campos = {}
        campos_info = [
            ("Rol", "combo"),
            ("Nombre", "entry"),
            ("Número de Serie", "entry"),
            ("Contraseña", "password"),
            ("Fecha de Compra", "date"),
            ("Dirección", "entry"),
            ("Número de Teléfono", "entry")
        ]

        for i, (label, tipo) in enumerate(campos_info):
            row = i // 2
            col = i % 2

            campo_frame = tk.Frame(form_frame, bg="#F7F7F7")
            campo_frame.grid(row=row, column=col, padx=10, pady=5, sticky="ew")

            tk.Label(
                campo_frame,
                text=label,
                font=("Segoe UI", 10),
                bg="#F7F7F7",
                anchor="w"
            ).pack(fill="x")

            if tipo == "password":
                entrada = ttk.Entry(campo_frame, width=25, show="*")
            elif tipo == "combo":
                entrada = ttk.Combobox(
                    campo_frame,
                    values=["cliente", "admin"],
                    state="readonly",
                    width=23
                )
                entrada.set("cliente")
                entrada.bind("<<ComboboxSelected>>", self.cambio_rol)
            elif tipo == "date":
                entrada = DateEntry(
                    campo_frame,
                    date_pattern='yyyy-MM-dd',
                    width=23,
                    background='#7AC35D',
                    foreground='white',
                    borderwidth=2
                )
            else:
                entrada = ttk.Entry(campo_frame, width=25)

            entrada.pack(fill="x", pady=(2, 0))
            self.campos[label.lower().replace(" ", "_")] = entrada

        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=1)

        tk.Button(
            form_frame,
            text="Registrar Usuario",
            command=self.registrar,
            bg="#7AC35D",
            fg="white",
            font=("Segoe UI", 11),
            padx=20,
            pady=8,
            relief="flat"
        ).grid(row=4, column=0, columnspan=2, pady=10)

        tabla_frame = tk.Frame(self, bg="#F7F7F7")
        tabla_frame.pack(fill="both", expand=False, padx=20, pady=(10, 0))

        tk.Label(
            tabla_frame,
            text="Usuarios Registrados",
            font=("Segoe UI", 12, "bold"),
            bg="#F7F7F7"
        ).pack(anchor="w", pady=(0, 5))

        columnas = ("Nombre", "N° Serie", "Rol", "Fecha Compra", "Dirección", "Teléfono")
        self.tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings", height=8)

        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=140, anchor="center")

        vsb = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=vsb.set)
        self.tabla.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        botones_frame = tk.Frame(self, bg="#F7F7F7")
        botones_frame.pack(pady=10)

        tk.Button(
            botones_frame,
            text="Eliminar Seleccionado",
            command=self.eliminar,
            bg="#D9534F",
            fg="white",
            font=("Segoe UI", 10),
            padx=15,
            pady=8,
            relief="flat"
        ).pack(side="left", padx=5)

        tk.Button(
            botones_frame,
            text="Actualizar",
            command=self.cargar_tabla,
            bg="#7AC35D",
            fg="white",
            font=("Segoe UI", 10),
            padx=15,
            pady=8,
            relief="flat"
        ).pack(side="left", padx=5)

        tk.Button(
            botones_frame,
            text="Volver",
            command=self.volver_callback,
            bg="#096B35",
            fg="white",
            font=("Segoe UI", 10),
            padx=15,
            pady=8,
            relief="flat"
        ).pack(side="left", padx=5)

    def cambio_rol(self, event):
        rol = self.campos["rol"].get()
        campos_bloquear = [
            "número_de_serie",
            "fecha_de_compra",
            "dirección",
            "número_de_teléfono"
        ]
        for campo in campos_bloquear:
            widget = self.campos[campo]
            estado = "disabled" if rol == "admin" else "normal"
            if isinstance(widget, ttk.Entry):
                widget.config(state=estado)
            elif isinstance(widget, DateEntry):
                widget.config(state=estado)

    def registrar(self):
        datos = {
            "nombre": self.campos["nombre"].get().strip(),
            "usuario": self.campos["número_de_serie"].get().strip(),
            "contrasena": self.campos["contraseña"].get().strip(),
            "rol": self.campos["rol"].get(),
            "fecha_compra": self.campos["fecha_de_compra"].get().strip(),
            "direccion": self.campos["dirección"].get().strip(),
            "telefono": self.campos["número_de_teléfono"].get().strip()
        }

        if not datos["nombre"]:
            messagebox.showerror("Error", "El nombre es obligatorio.")
            return
        if datos["rol"] == "cliente" and not datos["usuario"]:
            messagebox.showerror("Error", "El número de serie es obligatorio para clientes.")
            return
        if not datos["contrasena"]:
            messagebox.showerror("Error", "La contraseña es obligatoria.")
            return
        if len(datos["contrasena"]) < 3:
            messagebox.showerror("Error", "La contraseña debe tener al menos 3 caracteres.")
            return

        # En caso de admin, usar nombre como identificador de usuario
        if datos["rol"] == "admin":
            datos["usuario"] = datos["nombre"]

        exito = registrar_usuario(
            datos["usuario"], datos["contrasena"],
            datos["nombre"], datos["rol"],
            datos["fecha_compra"], datos["direccion"], datos["telefono"]
        )

        if exito:
            messagebox.showinfo("Éxito", f"Usuario '{datos['usuario']}' registrado correctamente.")
            self.cargar_tabla()
            self.limpiar_campos()
        else:
            messagebox.showerror("Error", f"El usuario '{datos['usuario']}' ya está registrado.")

    def limpiar_campos(self):
        for key, campo in self.campos.items():
            try:
                if hasattr(campo, 'delete'):
                    campo.config(state="normal")
                    campo.delete(0, tk.END)
                elif hasattr(campo, 'set'):
                    if key == "rol":
                        campo.set("cliente")
                    else:
                        campo.set("")
            except Exception:
                pass
        self.cambio_rol(None)

    def cargar_tabla(self):
        for row in self.tabla.get_children():
            self.tabla.delete(row)

        usuarios = cargar_usuarios()
        for i, u in enumerate(usuarios):
            tags = ("even",) if i % 2 == 0 else ("odd",)

            if u["rol"] == "admin":
                values = (
                    u["nombre"], "", u["rol"], "", u.get("direccion", ""), ""
                )
            else:
                values = (
                    u["nombre"],
                    u["usuario"],
                    u["rol"],
                    u.get("fecha_compra", ""),
                    u.get("direccion", ""),
                    u.get("telefono", "")
                )

            self.tabla.insert("", "end", values=values, tags=tags)

        self.tabla.tag_configure("even", background="#F9F9F9")
        self.tabla.tag_configure("odd", background="white")

    def eliminar(self):
        sel = self.tabla.selection()
        if not sel:
            messagebox.showerror("Error", "Seleccione un usuario para eliminar.")
            return

        item_values = self.tabla.item(sel[0])["values"]
        if not item_values:
            return

        usuario_nombre = item_values[0]
        numero_serie = str(item_values[1])

        respuesta = messagebox.askyesno(
            "Confirmar",
            f"¿Eliminar usuario '{usuario_nombre}'?\nN° Serie: {numero_serie or '(no aplica)'}"
        )

        if respuesta:
            if eliminar_usuario(numero_serie if numero_serie else usuario_nombre):
                messagebox.showinfo("Eliminado", f"Usuario '{usuario_nombre}' eliminado.")
                self.cargar_tabla()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el usuario.")
