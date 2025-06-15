import tkinter as tk
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import time

class HumedadFrame(tk.Frame):
    def __init__(self, parent, volver_callback, serial_manager):
        super().__init__(parent, bg="#FFFFFF")
        self.volver_callback = volver_callback
        self.serial_manager = serial_manager 
        self.archivo = os.path.join("data", "humedad_log.txt")

        self.crear_ui()
        self.mostrar_humedad_actual()
        self.mostrar_graficos()

    def crear_ui(self):
        header = tk.Frame(self, bg="#096B35", height=60)
        header.pack(fill="x")
        tk.Label(header, text="Humedad", font=("Segoe UI", 16, "bold"),
                 fg="white", bg="#096B35").pack(pady=15)

        self.lbl_actual = tk.Label(self, text="", font=("Segoe UI", 14), bg="#FFFFFF")
        self.lbl_actual.pack(pady=10)

        tk.Button(self, text="Actualizar", bg="#7AC35D", fg="white",
                  font=("Segoe UI", 10), width=15,
                  command=self.leer_humedad_desde_arduino).pack(pady=5)

        self.canvas_frame = tk.Frame(self, bg="#FFFFFF")
        self.canvas_frame.pack(pady=10)

        tk.Button(self, text="Volver", bg="#7AC35D", fg="white",
                  font=("Segoe UI", 10), width=12,
                  command=self.volver_callback).pack(pady=10)

    def leer_humedad_desde_arduino(self):
        try:
            self.serial_manager.arduino.reset_input_buffer()
            self.serial_manager.write("LEER:HUMEDAD")
            time.sleep(5)
            respuesta = self.serial_manager.leer_linea()

            if respuesta and "|" in respuesta:
                humedad, estado = respuesta.split("|")
                with open(self.archivo, "a", encoding="utf-8") as f:
                    f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M')}|{humedad}|{estado}\n")
                self.lbl_actual.config(text=f"Humedad actual: {humedad}%")
                self.mostrar_graficos()
            else:
                self.lbl_actual.config(text="No se recibió una respuesta válida del Arduino.")
        except Exception as e:
            self.lbl_actual.config(text=f"Error: {e}")

    def mostrar_humedad_actual(self):
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
            humedad = ultima[1]
            self.lbl_actual.config(text=f"Humedad actual: {humedad}%")

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
                    humedad = float(partes[1])
                    estado = partes[2].lower()
                    if estado == "cerrado":
                        datos_cerrado.append((tiempo, humedad))
                    elif estado == "abierto":
                        datos_abierto.append((tiempo, humedad))
                except:
                    continue

        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        fig, axs = plt.subplots(2, 1, figsize=(5, 4), dpi=100)
        fig.tight_layout(pad=3.0)

        if datos_cerrado:
            tiempos, valores = zip(*datos_cerrado)
            axs[0].plot(tiempos, valores, marker='o')
            axs[0].set_title("Techo cerrado")
            axs[0].set_ylabel("Humedad (%)")
            axs[0].tick_params(axis='x', rotation=45)
            axs[0].set_xlabel("Hora")

        if datos_abierto:
            tiempos, valores = zip(*datos_abierto)
            axs[1].plot(tiempos, valores, marker='o', color='orange')
            axs[1].set_title("Techo abierto")
            axs[1].set_ylabel("Humedad (%)")
            axs[1].tick_params(axis='x', rotation=45)
            axs[1].set_xlabel("Hora")

        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()
