import tkinter as tk
import os

class SeguimientoFrame(tk.Frame):
    def __init__(self, parent, volver_callback):
        super().__init__(parent, bg="#FFFFFF")
        self.volver_callback = volver_callback
        self.llamadas = []
        self.crear_ui()

    def crear_ui(self):
        # Encabezado
        header = tk.Frame(self, bg="#096B35", height=60)
        header.pack(fill="x")
        tk.Label(header, text="Seguimiento de Llamadas", font=("Segoe UI", 16, "bold"),
                 fg="white", bg="#096B35").pack(pady=15)

        # Lista de llamadas
        self.lista = tk.Listbox(self, width=60, height=20, font=("Segoe UI", 10))
        self.lista.pack(pady=10)

        # Botones
        botones = tk.Frame(self, bg="#FFFFFF")
        botones.pack()

        tk.Button(botones, text="Actualizar", bg="#7AC35D", fg="white",
                  font=("Segoe UI", 10), command=self.cargar_llamadas).grid(row=0, column=0, padx=10)

        tk.Button(botones, text="Ver seguimiento", bg="#7AC35D", fg="white",
                  font=("Segoe UI", 10), command=self.ver_seguimiento).grid(row=0, column=1, padx=10)

        tk.Button(self, text="Volver", bg="#7AC35D", fg="white",
                  font=("Segoe UI", 10), command=self.volver_callback).pack(pady=10)

        self.cargar_llamadas()

    def cargar_llamadas(self):
        self.lista.delete(0, tk.END)
        self.llamadas.clear()
        ruta = "data/llamadas_servicio.txt"

        if os.path.exists(ruta):
            with open(ruta, "r", encoding="utf-8") as f:
                for linea in f:
                    partes = linea.strip().split("|")
                    if len(partes) == 5:
                        self.llamadas.append(partes)
                        fecha, nombre, serie, telefono, mensaje = partes
                        resumen = f"[{fecha}] {nombre} - Serie: {serie}"
                        self.lista.insert(tk.END, resumen)
        else:
            self.lista.insert(tk.END, "No hay llamadas registradas aún.")

    def ver_seguimiento(self):
        seleccion = self.lista.curselection()
        if not seleccion:
            tk.messagebox.showwarning("Aviso", "Por favor seleccione una llamada.")
            return

        datos = self.llamadas[seleccion[0]]
        self.abrir_ventana_seguimiento(datos)

    def abrir_ventana_seguimiento(self, datos_llamada):
        fecha, nombre, serie, telefono, mensaje = datos_llamada
        ventana = tk.Toplevel(self)
        ventana.title("Detalle de seguimiento")
        ventana.geometry("500x500")
        ventana.configure(bg="#FFFFFF")

        # Título
        tk.Label(ventana, text="Seguimiento de llamada", font=("Segoe UI", 14, "bold"),
                 bg="#096B35", fg="white", height=2).pack(fill="x")

        # Info básica
        info = (
            f"📅 Fecha: {fecha}\n"
            f"👤 Nombre: {nombre}\n"
            f"🔢 Serie: {serie}\n"
            f"📞 Teléfono: {telefono}\n\n"
            f"📝 Mensaje:\n{mensaje}\n"
        )

        tk.Label(ventana, text=info, justify="left", bg="#FFFFFF", font=("Segoe UI", 10),
                 anchor="w").pack(padx=20, pady=10, fill="x")

        # Área de acciones
        area_acciones = tk.Text(ventana, width=60, height=15, font=("Segoe UI", 10))
        area_acciones.pack(pady=10)
        area_acciones.config(state="normal")
        area_acciones.insert(tk.END, "📋 Acciones registradas:\n")

        ruta_seguimiento = os.path.join("data", "seguimiento", f"{serie}.txt")
        if os.path.exists(ruta_seguimiento):
            with open(ruta_seguimiento, "r", encoding="utf-8") as f:
                for linea in f:
                    partes = linea.strip().split("|")
                    if len(partes) == 3:
                        acc_fecha, acc_serie, acc_texto = partes
                        area_acciones.insert(tk.END, f"   ➤ [{acc_fecha}] {acc_texto}\n")
        else:
            area_acciones.insert(tk.END, "   ⚠ No hay acciones registradas para esta llamada.\n")

        area_acciones.config(state="disabled")

        tk.Button(ventana, text="Cerrar", font=("Segoe UI", 10),
                  bg="#DDDDDD", width=15, command=ventana.destroy).pack(pady=10)
