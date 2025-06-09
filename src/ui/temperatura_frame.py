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

        # Botón para leer del Arduino
        tk.Button(self, text="Leer del Arduino", bg="#7AC35D", fg="white",
                  command=self.leer_temperatura_desde_arduino).pack(pady=5)

        self.canvas_frame = tk.Frame(self, bg="#FFFFFF")
        self.canvas_frame.pack(pady=10)

        tk.Button(self, text="Volver", bg="#7AC35D", fg="white",
                  font=("Segoe UI", 10), width=12,
                  command=self.volver_callback).pack(pady=10)

    def leer_temperatura_desde_arduino(self):
        try:
            self.serial_manager.write("LEER:DHT")
            respuesta = self.serial_manager.leer_linea()

            if respuesta is not None and respuesta.startswith("T:") and "H:" in respuesta:
                # Extraer temperatura
                partes = respuesta.replace("T:", "").replace("H:", "").split()
                temp = float(partes[0])

                estado = "abierto" if self.obtener_estado_techo() else "cerrado"

                # Guardar registro
                os.makedirs("data", exist_ok=True)
                with open(self.archivo, "a", encoding="utf-8") as f:
                    f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M')}|{temp}|{estado}\n")

                self.lbl_actual.config(text=f"Temperatura actual: {temp}°C")
                self.mostrar_graficos()
            else:
                self.lbl_actual.config(text="No se recibió una respuesta válida del Arduino.")
        except Exception as e:
            self.lbl_actual.config(text=f"Error: {e}")

    def obtener_estado_techo(self):
        # Simulación: podrías almacenar el estado real en un archivo o variable
        # Si deseas leer del Arduino, podrías usar otro comando serial
        return False  # Por ahora se asume cerrado

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

        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

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
