import tkinter as tk
from tkinter import messagebox
import os
import datetime

class SoporteFrame(tk.Frame):
    def __init__(self, parent, volver_callback, usuario):
        super().__init__(parent, bg="#FFFFFF")
        self.volver_callback = volver_callback
        self.usuario = usuario
        self.crear_ui()

    def crear_ui(self):
        header = tk.Frame(self, bg="#096B35", height=60)
        header.pack(fill="x")
        tk.Label(header, text="Soporte", font=("Segoe UI", 16, "bold"),
                 fg="white", bg="#096B35").pack(pady=15)

        tk.Label(self, text="Describa su problema a continuación:",
                 font=("Segoe UI", 12), bg="#FFFFFF").pack(pady=(30, 10))

        self.entrada_texto = tk.Text(self, width=45, height=12, font=("Segoe UI", 11))
        self.entrada_texto.pack(pady=5)

        tk.Button(self, text="Enviar", bg="#7AC35D", fg="white",
                  font=("Segoe UI", 11), width=15, height=1,
                  command=self.enviar_problema).pack(pady=(10, 30))

        tk.Button(self, text="Volver", bg="#7AC35D", fg="white",
                  font=("Segoe UI", 10), width=12,
                  command=self.volver_callback).pack(pady=(0, 20))

    def enviar_problema(self):
        mensaje = self.entrada_texto.get("1.0", tk.END).strip()
        if mensaje:
            fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            nombre = self.usuario.get("nombre", "Desconocido")
            numero_serie = self.usuario.get("numero_serie", "N/A")
            telefono = self.usuario.get("telefono", "Sin número")

            registro = f"{fecha_hora}|{nombre}|{numero_serie}|{telefono}|{mensaje}\n"
            os.makedirs("data", exist_ok=True)
            with open("data/llamadas_servicio.txt", "a", encoding="utf-8") as f:
                f.write(registro)

            messagebox.showinfo("Enviado", "Tu mensaje ha sido enviado al equipo de soporte.")
            self.entrada_texto.delete("1.0", tk.END)
        else:
            messagebox.showwarning("Campo vacío", "Por favor escribe tu problema antes de enviar.")
