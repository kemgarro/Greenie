
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os

LLAMADAS_FILE = "data/llamadas.txt"
SEGUIMIENTO_FILE = "data/seguimiento.txt"

class LlamadasFrame(tk.Frame):
    def __init__(self, master, volver_callback):
        super().__init__(master, bg="#FFFFFF")
        self.volver_callback = volver_callback
        self.crear_interfaz()
        self.cargar_llamadas()

    def crear_interfaz(self):
        header = tk.Frame(self, bg="#096B35", height=60)
        header.pack(fill="x")
        tk.Label(header, text="Llamadas de Soporte", font=("Segoe UI", 16, "bold"),
                 fg="white", bg="#096B35").pack(pady=15)

        self.tabla = ttk.Treeview(self, columns=("Fecha", "Serie", "Motivo"), show="headings", height=8)
        for col in self.tabla["columns"]:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=120, anchor="center")
        self.tabla.pack(pady=10)

        ttk.Button(self, text="Atender Llamada", command=self.atender_llamada).pack(pady=10)

        tk.Button(self, text="Volver", bg="#7AC35D", fg="white",
                  font=("Segoe UI", 10), width=12,
                  command=self.volver_callback).pack(pady=10)

    def cargar_llamadas(self):
        self.tabla.delete(*self.tabla.get_children())
        if not os.path.exists(LLAMADAS_FILE):
            return
        with open(LLAMADAS_FILE, "r", encoding="utf-8") as file:
            for linea in file:
                partes = linea.strip().split(",")
                if len(partes) == 3:
                    self.tabla.insert("", "end", values=partes)

    def atender_llamada(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Seleccione una llamada para atender.")
            return

        datos = self.tabla.item(seleccion[0])["values"]
        fecha, serie, motivo = datos
        comentario = tk.simpledialog.askstring("Seguimiento", f"Comentario para la llamada de {serie}:")
        if not comentario:
            return

        fecha_seg = datetime.now().strftime("%Y-%m-%d %H:%M")
        with open(SEGUIMIENTO_FILE, "a", encoding="utf-8") as f:
            f.write(f"{fecha_seg},{serie},{motivo},{comentario}\n")

        self.tabla.delete(seleccion[0])

        llamadas_restantes = []
        with open(LLAMADAS_FILE, "r", encoding="utf-8") as f:
            for linea in f:
                if not linea.startswith(fecha):
                    llamadas_restantes.append(linea)
        with open(LLAMADAS_FILE, "w", encoding="utf-8") as f:
            f.writelines(llamadas_restantes)

        messagebox.showinfo("Llamada atendida", f"Seguimiento guardado para {serie}.")
