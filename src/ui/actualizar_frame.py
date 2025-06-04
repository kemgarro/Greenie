
import tkinter as tk

class ActualizarFrame(tk.Frame):
    def __init__(self, master, volver_callback):
        super().__init__(master, bg="#FFFFFF")
        self.volver_callback = volver_callback
        self.crear_interfaz()

    def crear_interfaz(self):
        header = tk.Frame(self, bg="#096B35", height=60)
        header.pack(fill="x")
        tk.Label(header, text="Actualizar Lecturas", font=("Segoe UI", 16, "bold"),
                 fg="white", bg="#096B35").pack(pady=15)

        tk.Button(self, text="Refrescar Sensores", font=("Segoe UI", 12),
                  bg="#7AC35D", fg="white", width=22, height=2).pack(pady=40)

        tk.Button(self, text="Volver", bg="#7AC35D", fg="white",
                  font=("Segoe UI", 10), width=12,
                  command=self.volver_callback).pack(pady=10)
