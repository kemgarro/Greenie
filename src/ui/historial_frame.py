
import tkinter as tk
from tkinter import ttk
import os

HISTORIAL_FILE = "data/historial.txt"

class HistorialFrame(tk.Frame):
    def __init__(self, master, volver_callback):
        super().__init__(master, bg="#FFFFFF")
        self.volver_callback = volver_callback
        self.crear_interfaz()
        self.cargar_historial()

    def crear_interfaz(self):
        header = tk.Frame(self, bg="#096B35", height=60)
        header.pack(fill="x")
        tk.Label(header, text="Historial del Sistema", font=("Segoe UI", 16, "bold"),
                 fg="white", bg="#096B35").pack(pady=15)

        self.tabla = ttk.Treeview(self, columns=("Fecha", "Evento"), show="headings", height=12)
        self.tabla.heading("Fecha", text="Fecha")
        self.tabla.heading("Evento", text="Evento")
        self.tabla.column("Fecha", width=120, anchor="center")
        self.tabla.column("Evento", width=260, anchor="w")
        self.tabla.pack(padx=10, pady=10, fill="both", expand=True)

        tk.Button(self, text="Volver", bg="#7AC35D", fg="white",
                  font=("Segoe UI", 10), width=12,
                  command=self.volver_callback).pack(pady=10)

    def cargar_historial(self):
        self.tabla.delete(*self.tabla.get_children())
        if not os.path.exists(HISTORIAL_FILE):
            return
        with open(HISTORIAL_FILE, "r", encoding="utf-8") as f:
            for linea in f:
                partes = linea.strip().split(",", 1)
                if len(partes) == 2:
                    self.tabla.insert("", "end", values=partes)
