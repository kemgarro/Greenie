
import tkinter as tk
from tkinter import ttk
import os

SEGUIMIENTO_FILE = "data/seguimiento.txt"

class SeguimientoFrame(tk.Frame):
    def __init__(self, master, volver_callback):
        super().__init__(master, bg="#FFFFFF")
        self.volver_callback = volver_callback
        self.crear_interfaz()
        self.cargar_datos()

    def crear_interfaz(self):
        header = tk.Frame(self, bg="#096B35", height=60)
        header.pack(fill="x")
        tk.Label(header, text="Seguimiento de Llamadas", font=("Segoe UI", 16, "bold"),
                 fg="white", bg="#096B35").pack(pady=15)

        self.tabla = ttk.Treeview(self, columns=("Fecha", "Serie", "Motivo", "Comentario"), show="headings", height=10)
        for col in self.tabla["columns"]:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, anchor="center", width=100)
        self.tabla.pack(padx=10, pady=10, fill="both", expand=True)

        tk.Button(self, text="Volver", bg="#7AC35D", fg="white",
                  font=("Segoe UI", 10), width=12,
                  command=self.volver_callback).pack(pady=10)

    def cargar_datos(self):
        self.tabla.delete(*self.tabla.get_children())
        if not os.path.exists(SEGUIMIENTO_FILE):
            return
        with open(SEGUIMIENTO_FILE, "r", encoding="utf-8") as f:
            for linea in f:
                partes = linea.strip().split(",")
                if len(partes) == 4:
                    self.tabla.insert("", "end", values=partes)
