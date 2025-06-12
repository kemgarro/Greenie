import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import sqlite3
from datetime import datetime

class ProductosFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg='#f0f0f0')
        
        # Variables para los campos
        self.var_numero_serie = tk.StringVar()
        self.var_id_producto = tk.StringVar()
        self.var_nombre = tk.StringVar()
        self.var_descripcion = tk.StringVar()
        self.var_cantidad = tk.StringVar()
        self.var_precio = tk.StringVar()
        
        # Variable para controlar el modo edición
        self.editando = False
        self.producto_seleccionado = None
        
        self.setup_ui()
        self.cargar_productos()
        self.cargar_usuarios_combobox()
    
    def setup_ui(self):
        # Frame principal con scroll
        main_frame = tk.Frame(self, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        title_label = tk.Label(
            main_frame,
            text="GESTIÓN DE PRODUCTOS",
            font=('Arial', 24, 'bold'),
            bg='#f0f0f0',
            fg='#2e7d32'
        )
        title_label.pack(pady=(0, 30))
        
        # Frame para formulario y botones
        form_frame = tk.Frame(main_frame, bg='#f0f0f0')
        form_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Frame izquierdo para el formulario
        left_frame = tk.Frame(form_frame, bg='#f0f0f0')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Frame del formulario
        self.form_frame = tk.LabelFrame(
            left_frame,
            text="Datos del Producto",
            font=('Arial', 12, 'bold'),
            bg='#ffffff',
            fg='#2e7d32',
            padx=20,
            pady=15
        )
        self.form_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Campo: Número de serie de usuario (ComboBox)
        tk.Label(
            self.form_frame,
            text="Usuario (Número de Serie):",
            font=('Arial', 10, 'bold'),
            bg='#ffffff',
            fg='#333333'
        ).grid(row=0, column=0, sticky='w', pady=(0, 5))
        
        self.combo_usuarios = ttk.Combobox(
            self.form_frame,
            textvariable=self.var_numero_serie,
            font=('Arial', 10),
            state='readonly',
            width=30
        )
        self.combo_usuarios.grid(row=0, column=1, sticky='ew', pady=(0, 10))
        
        # Campo: ID del producto
        tk.Label(
            self.form_frame,
            text="ID del Producto:",
            font=('Arial', 10, 'bold'),
            bg='#ffffff',
            fg='#333333'
        ).grid(row=1, column=0, sticky='w', pady=(0, 5))
        
        tk.Entry(
            self.form_frame,
            textvariable=self.var_id_producto,
            font=('Arial', 10),
            width=30
        ).grid(row=1, column=1, sticky='ew', pady=(0, 10))
        
        # Campo: Nombre del producto
        tk.Label(
            self.form_frame,
            text="Nombre del Producto:",
            font=('Arial', 10, 'bold'),
            bg='#ffffff',
            fg='#333333'
        ).grid(row=2, column=0, sticky='w', pady=(0, 5))
        
        tk.Entry(
            self.form_frame,
            textvariable=self.var_nombre,
            font=('Arial', 10),
            width=30
        ).grid(row=2, column=1, sticky='ew', pady=(0, 10))
        
        # Campo: Descripción
        tk.Label(
            self.form_frame,
            text="Descripción:",
            font=('Arial', 10, 'bold'),
            bg='#ffffff',
            fg='#333333'
        ).grid(row=3, column=0, sticky='w', pady=(0, 5))
        
        self.text_descripcion = tk.Text(
            self.form_frame,
            font=('Arial', 10),
            width=30,
            height=3
        )
        self.text_descripcion.grid(row=3, column=1, sticky='ew', pady=(0, 10))
        
        # Campo: Fecha de fabricación
        tk.Label(
            self.form_frame,
            text="Fecha de Fabricación:",
            font=('Arial', 10, 'bold'),
            bg='#ffffff',
            fg='#333333'
        ).grid(row=4, column=0, sticky='w', pady=(0, 5))
        
        self.date_fabricacion = DateEntry(
            self.form_frame,
            font=('Arial', 10),
            width=28,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern='dd/mm/yyyy'
        )
        self.date_fabricacion.grid(row=4, column=1, sticky='ew', pady=(0, 10))
        
        # Campo: Cantidad en stock
        tk.Label(
            self.form_frame,
            text="Cantidad en Stock:",
            font=('Arial', 10, 'bold'),
            bg='#ffffff',
            fg='#333333'
        ).grid(row=5, column=0, sticky='w', pady=(0, 5))
        
        tk.Entry(
            self.form_frame,
            textvariable=self.var_cantidad,
            font=('Arial', 10),
            width=30
        ).grid(row=5, column=1, sticky='ew', pady=(0, 10))
        
        # Campo: Precio unitario
        tk.Label(
            self.form_frame,
            text="Precio Unitario ($):",
            font=('Arial', 10, 'bold'),
            bg='#ffffff',
            fg='#333333'
        ).grid(row=6, column=0, sticky='w', pady=(0, 5))
        
        tk.Entry(
            self.form_frame,
            textvariable=self.var_precio,
            font=('Arial', 10),
            width=30
        ).grid(row=6, column=1, sticky='ew', pady=(0, 10))
        
        # Configurar expansión de columnas
        self.form_frame.columnconfigure(1, weight=1)
        
        # Frame derecho para botones
        right_frame = tk.Frame(form_frame, bg='#f0f0f0')
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        
        # Frame para botones de acción
        buttons_frame = tk.Frame(right_frame, bg='#f0f0f0')
        buttons_frame.pack(pady=20)
        
        # Botón Registrar/Actualizar
        self.btn_action = tk.Button(
            buttons_frame,
            text="REGISTRAR PRODUCTO",
            font=('Arial', 11, 'bold'),
            bg='#4caf50',
            fg='white',
            padx=20,
            pady=10,
            cursor='hand2',
            command=self.registrar_producto
        )
        self.btn_action.pack(pady=(0, 10))
        
        # Botón Cancelar/Limpiar
        self.btn_cancel = tk.Button(
            buttons_frame,
            text="LIMPIAR",
            font=('Arial', 11, 'bold'),
            bg='#ff9800',
            fg='white',
            padx=20,
            pady=10,
            cursor='hand2',
            command=self.limpiar_formulario
        )
        self.btn_cancel.pack(pady=(0, 10))
        
        # Botón Editar
        tk.Button(
            buttons_frame,
            text="EDITAR SELECCIONADO",
            font=('Arial', 11, 'bold'),
            bg='#2196f3',
            fg='white',
            padx=20,
            pady=10,
            cursor='hand2',
            command=self.editar_producto
        ).pack(pady=(0, 10))
        
        # Botón Eliminar
        tk.Button(
            buttons_frame,
            text="ELIMINAR SELECCIONADO",
            font=('Arial', 11, 'bold'),
            bg='#f44336',
            fg='white',
            padx=20,
            pady=10,
            cursor='hand2',
            command=self.eliminar_producto
        ).pack(pady=(0, 10))
        
        # Botón Volver
        tk.Button(
            buttons_frame,
            text="VOLVER AL MENÚ",
            font=('Arial', 11, 'bold'),
            bg='#607d8b',
            fg='white',
            padx=20,
            pady=10,
            cursor='hand2',
            command=self.volver_menu
        ).pack(pady=(20, 0))
        
        # Frame para la tabla
        table_frame = tk.LabelFrame(
            main_frame,
            text="Lista de Productos",
            font=('Arial', 12, 'bold'),
            bg='#ffffff',
            fg='#2e7d32',
            padx=10,
            pady=10
        )
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview para mostrar productos
        self.tree = ttk.Treeview(
            table_frame,
            columns=('num_serie', 'id_producto', 'nombre', 'descripcion', 'fecha_fab', 'cantidad', 'precio'),
            show='headings',
            height=12
        )
        
        # Configurar columnas
        self.tree.heading('num_serie', text='Núm. Serie Usuario')
        self.tree.heading('id_producto', text='ID Producto')
        self.tree.heading('nombre', text='Nombre')
        self.tree.heading('descripcion', text='Descripción')
        self.tree.heading('fecha_fab', text='Fecha Fab.')
        self.tree.heading('cantidad', text='Stock')
        self.tree.heading('precio', text='Precio ($)')
        
        # Configurar ancho de columnas
        self.tree.column('num_serie', width=120, minwidth=100)
        self.tree.column('id_producto', width=100, minwidth=80)
        self.tree.column('nombre', width=150, minwidth=120)
        self.tree.column('descripcion', width=200, minwidth=150)
        self.tree.column('fecha_fab', width=100, minwidth=80)
        self.tree.column('cantidad', width=80, minwidth=60)
        self.tree.column('precio', width=100, minwidth=80)
        
        # Scrollbars para la tabla
        v_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Ubicar tabla y scrollbars
        self.tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        # Configurar expansión del grid
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Bind para selección de producto
        self.tree.bind('<<TreeviewSelect>>', self.on_producto_select)
    
    def init_database(self):
        """Inicializa la base de datos y crea las tablas necesarias"""
        conn = sqlite3.connect('greenie.db')
        cursor = conn.cursor()
        
        # Crear tabla de productos si no existe
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_serie_usuario TEXT NOT NULL,
                id_producto TEXT NOT NULL UNIQUE,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                fecha_fabricacion DATE NOT NULL,
                cantidad_stock INTEGER NOT NULL,
                precio_unitario REAL NOT NULL,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (numero_serie_usuario) REFERENCES usuarios (numero_serie)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def cargar_usuarios_combobox(self):
        """Carga los usuarios disponibles en el combobox"""
        try:
            conn = sqlite3.connect('greenie.db')
            cursor = conn.cursor()
            
            cursor.execute('SELECT numero_serie, nombre FROM usuarios ORDER BY nombre')
            usuarios = cursor.fetchall()
            
            # Formatear datos para el combobox
            valores_combo = [f"{num_serie} - {nombre}" for num_serie, nombre in usuarios]
            self.combo_usuarios['values'] = valores_combo
            
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al cargar usuarios: {e}")
    
    def registrar_producto(self):
        """Registra un nuevo producto o actualiza uno existente"""
        if not self.validar_campos():
            return
        
        try:
            self.init_database()
            conn = sqlite3.connect('greenie.db')
            cursor = conn.cursor()
            
            # Extraer solo el número de serie del combo
            numero_serie = self.var_numero_serie.get().split(' - ')[0]
            
            # Obtener descripción del Text widget
            descripcion = self.text_descripcion.get('1.0', tk.END).strip()
            
            # Formatear fecha
            fecha_fab = self.date_fabricacion.get_date().strftime('%Y-%m-%d')
            
            if self.editando:
                # Actualizar producto existente
                cursor.execute('''
                    UPDATE productos SET
                        numero_serie_usuario = ?,
                        id_producto = ?,
                        nombre = ?,
                        descripcion = ?,
                        fecha_fabricacion = ?,
                        cantidad_stock = ?,
                        precio_unitario = ?
                    WHERE id = ?
                ''', (
                    numero_serie,
                    self.var_id_producto.get(),
                    self.var_nombre.get(),
                    descripcion,
                    fecha_fab,
                    int(self.var_cantidad.get()),
                    float(self.var_precio.get()),
                    self.producto_seleccionado
                ))
                messagebox.showinfo("Éxito", "Producto actualizado correctamente")
            else:
                # Registrar nuevo producto
                cursor.execute('''
                    INSERT INTO productos (
                        numero_serie_usuario, id_producto, nombre, descripcion,
                        fecha_fabricacion, cantidad_stock, precio_unitario
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    numero_serie,
                    self.var_id_producto.get(),
                    self.var_nombre.get(),
                    descripcion,
                    fecha_fab,
                    int(self.var_cantidad.get()),
                    float(self.var_precio.get())
                ))
                messagebox.showinfo("Éxito", "Producto registrado correctamente")
            
            conn.commit()
            conn.close()
            
            self.limpiar_formulario()
            self.cargar_productos()
            
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                messagebox.showerror("Error", "Ya existe un producto con ese ID")
            else:
                messagebox.showerror("Error", f"Error de integridad: {e}")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error de base de datos: {e}")
        except ValueError as e:
            messagebox.showerror("Error", "Verifique que la cantidad sea un número entero y el precio un número válido")
    
    def validar_campos(self):
        """Valida que todos los campos requeridos estén completos"""
        if not self.var_numero_serie.get():
            messagebox.showerror("Error", "Seleccione un usuario")
            return False
        
        if not self.var_id_producto.get().strip():
            messagebox.showerror("Error", "Ingrese el ID del producto")
            return False
        
        if not self.var_nombre.get().strip():
            messagebox.showerror("Error", "Ingrese el nombre del producto")
            return False
        
        try:
            cantidad = int(self.var_cantidad.get())
            if cantidad < 0:
                messagebox.showerror("Error", "La cantidad no puede ser negativa")
                return False
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número entero")
            return False
        
        try:
            precio = float(self.var_precio.get())
            if precio < 0:
                messagebox.showerror("Error", "El precio no puede ser negativo")
                return False
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser un número válido")
            return False
        
        return True
    
    def cargar_productos(self):
        """Carga todos los productos en la tabla"""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            self.init_database()
            conn = sqlite3.connect('greenie.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT p.id, p.numero_serie_usuario, p.id_producto, p.nombre,
                       p.descripcion, p.fecha_fabricacion, p.cantidad_stock, p.precio_unitario
                FROM productos p
                ORDER BY p.fecha_registro DESC
            ''')
            
            productos = cursor.fetchall()
            
            for producto in productos:
                # Formatear precio
                precio_formateado = f"${producto[7]:.2f}"
                
                # Truncar descripción si es muy larga
                descripcion = producto[4][:50] + "..." if len(producto[4]) > 50 else producto[4]
                
                self.tree.insert('', tk.END, values=(
                    producto[1],  # numero_serie_usuario
                    producto[2],  # id_producto
                    producto[3],  # nombre
                    descripcion,  # descripcion (truncada)
                    producto[5],  # fecha_fabricacion
                    producto[6],  # cantidad_stock
                    precio_formateado  # precio_unitario
                ), tags=(producto[0],))  # Guardar ID en tags
            
            conn.close()
            
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al cargar productos: {e}")
    
    def on_producto_select(self, event):
        """Maneja la selección de un producto en la tabla"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            self.producto_seleccionado = item['tags'][0] if item['tags'] else None
    
    def editar_producto(self):
        """Carga los datos del producto seleccionado para edición"""
        if not self.producto_seleccionado:
            messagebox.showwarning("Advertencia", "Seleccione un producto para editar")
            return
        
        try:
            conn = sqlite3.connect('greenie.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT numero_serie_usuario, id_producto, nombre, descripcion,
                       fecha_fabricacion, cantidad_stock, precio_unitario
                FROM productos WHERE id = ?
            ''', (self.producto_seleccionado,))
            
            producto = cursor.fetchone()
            
            if producto:
                # Cargar datos en el formulario
                # Buscar el valor correcto para el combobox
                for value in self.combo_usuarios['values']:
                    if value.startswith(producto[0]):
                        self.var_numero_serie.set(value)
                        break
                
                self.var_id_producto.set(producto[1])
                self.var_nombre.set(producto[2])
                
                # Limpiar y cargar descripción
                self.text_descripcion.delete('1.0', tk.END)
                self.text_descripcion.insert('1.0', producto[3] if producto[3] else '')
                
                # Cargar fecha
                fecha_obj = datetime.strptime(producto[4], '%Y-%m-%d').date()
                self.date_fabricacion.set_date(fecha_obj)
                
                self.var_cantidad.set(str(producto[5]))
                self.var_precio.set(str(producto[6]))
                
                # Cambiar a modo edición
                self.editando = True
                self.btn_action.config(text="ACTUALIZAR PRODUCTO", bg='#ff9800')
                self.btn_cancel.config(text="CANCELAR")
            
            conn.close()
            
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al cargar datos del producto: {e}")
    
    def eliminar_producto(self):
        """Elimina el producto seleccionado"""
        if not self.producto_seleccionado:
            messagebox.showwarning("Advertencia", "Seleccione un producto para eliminar")
            return
        
        # Confirmar eliminación
        respuesta = messagebox.askyesno(
            "Confirmar Eliminación",
            "¿Está seguro de que desea eliminar este producto?\nEsta acción no se puede deshacer."
        )
        
        if respuesta:
            try:
                conn = sqlite3.connect('greenie.db')
                cursor = conn.cursor()
                
                cursor.execute('DELETE FROM productos WHERE id = ?', (self.producto_seleccionado,))
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Éxito", "Producto eliminado correctamente")
                self.cargar_productos()
                self.producto_seleccionado = None
                
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Error al eliminar producto: {e}")
    
    def limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        self.var_numero_serie.set('')
        self.var_id_producto.set('')
        self.var_nombre.set('')
        self.text_descripcion.delete('1.0', tk.END)
        self.date_fabricacion.set_date(datetime.now().date())
        self.var_cantidad.set('')
        self.var_precio.set('')
        
        # Resetear modo edición
        self.editando = False
        self.producto_seleccionado = None
        self.btn_action.config(text="REGISTRAR PRODUCTO", bg='#4caf50')
        self.btn_cancel.config(text="LIMPIAR")
    
    def volver_menu(self):
        """Vuelve al menú principal de administrador"""
        if hasattr(self.controller, 'show_frame'):
            self.controller.show_frame('AdminFrame')
        else:
            # Alternativa si el controlador tiene un método diferente
            self.controller.mostrar_admin()