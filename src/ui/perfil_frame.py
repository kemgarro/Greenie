
import tkinter as tk

class PerfilFrame(tk.Frame):
    def __init__(self, master, volver_callback):
        super().__init__(master, bg="#FFFFFF")
        self.volver_callback = volver_callback
        self.crear_interfaz()

    def crear_interfaz(self):
        header = tk.Frame(self, bg="#096B35", height=60)
        header.pack(fill="x")
        tk.Label(header, text="Mi Perfil", font=("Segoe UI", 16, "bold"),
                 fg="white", bg="#096B35").pack(pady=15)

        tk.Label(self, text="Nombre del Cliente: Ejemplo S.A.", bg="#FFFFFF", font=("Segoe UI", 12)).pack(pady=5)
        tk.Label(self, text="Número de Serie: 1234567890", bg="#FFFFFF", font=("Segoe UI", 12)).pack(pady=5)

        tk.Button(self, text="Volver", bg="#7AC35D", fg="white",
                  font=("Segoe UI", 10), width=12,
                  command=self.volver_callback).pack(pady=20)
