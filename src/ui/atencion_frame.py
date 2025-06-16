import tkinter as tk
from tkinter import messagebox
import os
import datetime

class AtencionFrame:
    def __init__(self, root, datos_llamada):
        self.root = root
        self.root.title("Atención de Llamada")
        self.root.geometry("400x500")
        self.root.configure(bg="#FFFFFF")
        self.datos = datos_llamada
        self.serie = datos_llamada[2]
        self.crear_ui()

    def crear_ui(self):
        tk.Label(self.root, text="Atención de Llamada", font=("Segoe UI", 16, "bold"),
                 bg="#096B35", fg="white", height=2).pack(fill="x")

        info = (
            f"📅 Fecha: {self.datos[0]}\n"
            f"👤 Nombre: {self.datos[1]}\n"
            f"🔢 Serie: {self.datos[2]}\n"
            f"📞 Teléfono: {self.datos[3]}\n\n"
            f"📝 Mensaje:\n{self.datos[4]}"
        )

        tk.Label(self.root, text=info, justify="left", font=("Segoe UI", 10),
                 bg="#FFFFFF", anchor="w").pack(padx=20, pady=20, fill="x")

        acciones = [
            "Se contactó al cliente",
            "Se mandó dispositivo a taller",
            "Se envió dispositivo reparado a cliente",
            "Se dio instrucciones a cliente para solucionara el problema",
            "Se solucionó problema"
        ]

        for accion in acciones:
            tk.Button(self.root, text=accion,
                      font=("Segoe UI", 10), bg="#7AC35D", fg="white",
                      width=40, command=lambda a=accion: self.registrar_accion(a)).pack(pady=5)

        tk.Button(self.root, text="Cerrar", font=("Segoe UI", 10),
                  bg="#DDDDDD", width=20, command=self.root.destroy).pack(pady=20)

    def registrar_accion(self, accion):
        fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linea = f"{fecha_hora}|{self.serie}|{accion}\n"
        os.makedirs("data/seguimiento", exist_ok=True)
        archivo = os.path.join("data/seguimiento", f"{self.serie}.txt")
        with open(archivo, "a", encoding="utf-8") as f:
            f.write(linea)
        messagebox.showinfo("Registrado", f"Acción registrada:\n{accion}")
