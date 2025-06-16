import tkinter as tk
import os
from src.ui.atencion_frame import AtencionFrame

class LlamadasFrame(tk.Frame):
    def __init__(self, parent, volver_callback):
        super().__init__(parent, bg="#FFFFFF")
        self.volver_callback = volver_callback
        self.llamadas = []
        self.crear_ui()

    def crear_ui(self):
        header = tk.Frame(self, bg="#096B35", height=60)
        header.pack(fill="x")
        tk.Label(header, text="Llamadas de Servicio", font=("Segoe UI", 16, "bold"),
                 fg="white", bg="#096B35").pack(pady=15)

        self.lista = tk.Listbox(self, width=60, height=18, font=("Segoe UI", 10))
        self.lista.pack(pady=10)

        botones = tk.Frame(self, bg="#FFFFFF")
        botones.pack()

        tk.Button(botones, text="Actualizar", bg="#7AC35D", fg="white",
                  font=("Segoe UI", 10), command=self.cargar_llamadas).grid(row=0, column=0, padx=10)

        tk.Button(botones, text="Atender llamada", bg="#7AC35D", fg="white",
                  font=("Segoe UI", 10), command=self.abrir_atencion).grid(row=0, column=1, padx=10)

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

    def abrir_atencion(self):
        seleccion = self.lista.curselection()
        if seleccion:
            datos_llamada = self.llamadas[seleccion[0]]
            nueva_ventana = tk.Toplevel(self)
            AtencionFrame(nueva_ventana, datos_llamada)
        else:
            tk.messagebox.showwarning("Atención", "Por favor seleccione una llamada.")
