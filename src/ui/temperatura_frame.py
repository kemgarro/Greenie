
import tkinter as tk
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

class TemperaturaFrame(tk.Frame):
    def __init__(self, parent, volver_callback, serial_manager):
        super().__init__(parent, bg="#FFFFFF")
        self.volver_callback = volver_callback
        self.serial_manager = serial_manager
        self.archivo = os.path.join("data", "temperatura_log.txt")
        self.crear_ui()
        self.mostrar_temperatura_actual()
        self.mostrar_graficos()

    def crear_ui(self):
        header = tk.Frame(self, bg="#096B35", height=60)
        header.pack(fill="x")
        tk.Label(header, text="Temperatura", font=("Segoe UI", 16, "bold"),
                 fg="white", bg="#096B35").pack(pady=15)

        self.lbl_actual = tk.Label(self, text="", font=("Segoe UI", 14), bg="#FFFFFF")
        self.lbl_actual.pack(pady=10)

        self.canvas_frame = tk.Frame(self, bg="#FFFFFF")
        self.canvas_frame.pack(pady=10)

        tk.Button(self, text="Volver", bg="#7AC35D", fg="white",
                  font=("Segoe UI", 10), width=12,
                  command=self.volver_callback).pack(pady=10)

    def mostrar_temperatura_actual(self):
        if not os.path.exists(self.archivo):
            self.lbl_actual.config(text="Sin registros disponibles.")
            return

        with open(self.archivo, "r", encoding="utf-8") as f:
            lineas = f.readlines()
        if not lineas:
            self.lbl_actual.config(text="Sin registros disponibles.")
            return

        ultima = lineas[-1].strip().split("|")
        if len(ultima) >= 2:
            temp = ultima[1]
            self.lbl_actual.config(text=f"Temperatura actual: {temp}°C")

    def mostrar_graficos(self):
        if not os.path.exists(self.archivo):
            return

        datos_cerrado = []
        datos_abierto = []

        with open(self.archivo, "r", encoding="utf-8") as f:
            for linea in f:
                partes = linea.strip().split("|")
                if len(partes) < 3:
                    continue
                try:
                    tiempo = datetime.strptime(partes[0], "%Y-%m-%d %H:%M")
                    temp = float(partes[1])
                    estado = partes[2].lower()
                    if estado == "cerrado":
                        datos_cerrado.append((tiempo, temp))
                    elif estado == "abierto":
                        datos_abierto.append((tiempo, temp))
                except:
                    continue

        fig, axs = plt.subplots(2, 1, figsize=(5, 4), dpi=100)
        fig.tight_layout(pad=3.0)

        if datos_cerrado:
            tiempos, temps = zip(*datos_cerrado)
            axs[0].plot(tiempos, temps, marker='o')
            axs[0].set_title("Techo cerrado")
            axs[0].set_ylabel("Temperatura (°C)")
            axs[0].tick_params(axis='x', rotation=45)
            axs[0].set_xlabel("Hora")


        if datos_abierto:
            tiempos, temps = zip(*datos_abierto)
            axs[1].plot(tiempos, temps, marker='o', color='orange')
            axs[1].set_title("Techo abierto")
            axs[1].set_ylabel("Temperatura (°C)")
            axs[1].tick_params(axis='x', rotation=45)
            axs[1].set_xlabel("Hora")


        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()
