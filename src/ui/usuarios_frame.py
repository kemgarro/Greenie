import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from src.backend.autenticacion import (
    registrar_usuario, cargar_usuarios, eliminar_usuario
)

class UsuariosFrame(tk.Frame):
    def __init__(self, master, volver_callback):
        # Ajustar tamaño de la ventana
        try:
            master.geometry("1000x650")
            master.minsize(900, 600)
        except Exception:
            pass
        super().__init__(master, bg="#E8E8E8")
        self.volver_callback = volver_callback
        self.crear_interfaz()
        self.cargar_tabla()

    def crear_interfaz(self):
        # --- Header simple como Greenie ---
        header = tk.Frame(self, bg="#7AC35D", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(
            header, 
            text="Gestión de Usuarios",
            font=("Segoe UI", 18, "bold"),
            fg="white", 
            bg="#7AC35D"
        ).pack(expand=True)

        # --- Contenedor principal con scroll ---
        main_canvas = tk.Canvas(self, bg="#E8E8E8", highlightthickness=0)
        main_scrollbar = ttk.Scrollbar(self, orient="vertical", command=main_canvas.yview)
        scrollable_frame = tk.Frame(main_canvas, bg="#E8E8E8")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )
        
        main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=main_scrollbar.set)
        
        main_canvas.pack(side="left", fill="both", expand=True)
        main_scrollbar.pack(side="right", fill="y")

        # --- Formulario sencillo ---
        form_frame = tk.Frame(scrollable_frame, bg="#E8E8E8")
        form_frame.pack(fill="x", padx=20, pady=15)

        self.campos = {}
        
        # Campos en layout simple
        campos_info = [
            ("Nombre", "entry"),
            ("Número de Serie", "entry"),
            ("Contraseña", "password"),
            ("Rol", "combo"),
            ("Fecha de Compra", "date"),
            ("Dirección", "entry"),
            ("Número de Teléfono", "entry")
        ]
        
        # Crear campos en 2 columnas
        for i, (label, tipo) in enumerate(campos_info):
            row = i // 2
            col = i % 2
            
            # Frame para cada campo
            campo_frame = tk.Frame(form_frame, bg="#E8E8E8")
            campo_frame.grid(row=row, column=col, padx=15, pady=8, sticky="ew")
            
            # Label sencillo
            tk.Label(
                campo_frame,
                text=label,
                font=("Segoe UI", 10),
                bg="#E8E8E8",
                anchor="w"
            ).pack(fill="x")

            # Campo de entrada
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

        # Configurar grid
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=1)

        # Botón de registro estilo Greenie
        btn_frame = tk.Frame(form_frame, bg="#E8E8E8")
        btn_frame.grid(row=(len(campos_info) + 1) // 2, column=0, columnspan=2, pady=15)
        
        tk.Button(
            btn_frame,
            text="Registrar Usuario",
            command=self.registrar,
            bg="#7AC35D",
            fg="white",
            font=("Segoe UI", 11),
            padx=20,
            pady=8,
            relief="flat"
        ).pack()

        # --- Tabla de usuarios ---
        tabla_frame = tk.Frame(scrollable_frame, bg="#E8E8E8")
        tabla_frame.pack(fill="both", expand=True, padx=20, pady=15)
        
        # Título de la tabla
        tk.Label(
            tabla_frame,
            text="Usuarios Registrados",
            font=("Segoe UI", 12, "bold"),
            bg="#E8E8E8"
        ).pack(anchor="w", pady=(0, 10))

        # Frame para la tabla con scrollbars
        tabla_container = tk.Frame(tabla_frame, bg="#E8E8E8")
        tabla_container.pack(fill="both", expand=True)

        # Configurar Treeview simple
        style = ttk.Style()
        style.configure(
            "Simple.Treeview",
            background="white",
            foreground="#333333",
            rowheight=25,
            fieldbackground="white"
        )
        style.configure(
            "Simple.Treeview.Heading",
            background="#D3D3D3",
            foreground="#333333",
            font=("Segoe UI", 10, "bold")
        )
        style.map(
            "Simple.Treeview",
            background=[('selected', '#7AC35D')],
            foreground=[('selected', 'white')]
        )

        cols = (
            "Nombre", "N° Serie", "Rol",
            "Fecha Compra", "Dirección", "Teléfono"
        )
        
        self.tabla = ttk.Treeview(
            tabla_container,
            columns=cols,
            show="headings",
            style="Simple.Treeview",
            height=10
        )

        # Scrollbars para la tabla
        v_scroll = ttk.Scrollbar(
            tabla_container,
            orient="vertical",
            command=self.tabla.yview
        )
        self.tabla.configure(yscrollcommand=v_scroll.set)
        
        h_scroll = ttk.Scrollbar(
            tabla_container,
            orient="horizontal",
            command=self.tabla.xview
        )
        self.tabla.configure(xscrollcommand=h_scroll.set)

        # Posicionar tabla y scrollbars
        self.tabla.grid(row=0, column=0, sticky="nsew")
        v_scroll.grid(row=0, column=1, sticky="ns")
        h_scroll.grid(row=1, column=0, sticky="ew")
        
        tabla_container.grid_rowconfigure(0, weight=1)
        tabla_container.grid_columnconfigure(0, weight=1)

        # Configurar encabezados y anchos
        widths = [150, 120, 80, 120, 200, 120]
        for col, w in zip(cols, widths):
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=w, anchor="center", minwidth=70)

        # Botones de acción estilo Greenie
        botones_frame = tk.Frame(tabla_frame, bg="#E8E8E8")
        botones_frame.pack(pady=15)
        
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

        # Botón volver estilo Greenie
        tk.Button(
            scrollable_frame,
            text="Volver",
            bg="#7AC35D",
            fg="white",
            font=("Segoe UI", 11),
            padx=25,
            pady=10,
            relief="flat",
            command=self.volver_callback
        ).pack(pady=20)

        # Bind scroll del mouse
        def _on_mousewheel(event):
            main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        main_canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def registrar(self):
        # Mapeo de campos
        datos = {
            "nombre": self.campos["nombre"].get().strip(),
            "usuario": self.campos["número_de_serie"].get().strip(),
            "contrasena": self.campos["contraseña"].get().strip(),
            "rol": self.campos["rol"].get(),
            "fecha_compra": self.campos["fecha_de_compra"].get().strip(),
            "direccion": self.campos["dirección"].get().strip(),
            "telefono": self.campos["número_de_teléfono"].get().strip()
        }
        
        # Validaciones
        if not datos["nombre"]:
            messagebox.showerror("Error", "El nombre es obligatorio.")
            return
        if not datos["usuario"]:
            messagebox.showerror("Error", "El número de serie es obligatorio.")
            return
        if not datos["contrasena"]:
            messagebox.showerror("Error", "La contraseña es obligatoria.")
            return
        if len(datos["contrasena"]) < 3:
            messagebox.showerror("Error", "La contraseña debe tener al menos 3 caracteres.")
            return

        exito = registrar_usuario(
            datos["usuario"], datos["contrasena"],
            datos["nombre"], datos["rol"],
            datos["fecha_compra"], datos["direccion"], datos["telefono"]
        )
        
        if exito:
            messagebox.showinfo(
                "Éxito", 
                f"Usuario '{datos['usuario']}' registrado correctamente."
            )
            self.cargar_tabla()
            self.limpiar_campos()
        else:
            messagebox.showerror(
                "Error", 
                f"El número de serie '{datos['usuario']}' ya está registrado."
            )

    def limpiar_campos(self):
        """Limpia todos los campos del formulario"""
        for key, campo in self.campos.items():
            try:
                if hasattr(campo, 'delete'):
                    campo.delete(0, tk.END)
                elif hasattr(campo, 'set'):
                    if key == "rol":
                        campo.set("cliente")
                    else:
                        campo.set("")
            except Exception:
                pass

    def cargar_tabla(self):
        """Carga todos los usuarios en la tabla"""
        # Limpiar tabla
        for row in self.tabla.get_children():
            self.tabla.delete(row)
        
        # Cargar usuarios
        usuarios = cargar_usuarios()
        
        if not usuarios:
            return
            
        # Insertar datos con colores alternos
        for i, u in enumerate(usuarios):
            tags = ("even",) if i % 2 == 0 else ("odd",)
            
            self.tabla.insert(
                "",
                "end",
                values=(
                    u["nombre"],
                    u["usuario"],
                    u["rol"],
                    u.get("fecha_compra", ""),
                    u.get("direccion", ""),
                    u.get("telefono", "")
                ),
                tags=tags
            )
        
        # Configurar colores alternos suaves
        self.tabla.tag_configure("even", background="#F9F9F9")
        self.tabla.tag_configure("odd", background="white")

    def eliminar(self):
        """Elimina el usuario seleccionado"""
        sel = self.tabla.selection()
        if not sel:
            messagebox.showerror("Error", "Seleccione un usuario para eliminar.")
            return
            
        # Obtener datos del usuario seleccionado
        item_values = self.tabla.item(sel[0])["values"]
        if not item_values:
            return
            
        usuario_nombre = item_values[0]
        numero_serie = item_values[1]
        
        # Confirmar eliminación
        respuesta = messagebox.askyesno(
            "Confirmar",
            f"¿Eliminar usuario '{usuario_nombre}'?\n"
            f"N° Serie: {numero_serie}"
        )
        
        if respuesta:
            if eliminar_usuario(numero_serie):
                messagebox.showinfo("Eliminado", f"Usuario '{usuario_nombre}' eliminado.")
                self.cargar_tabla()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el usuario.")