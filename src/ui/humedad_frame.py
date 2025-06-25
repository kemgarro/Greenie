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
        self.archivo_alerta = os.path.join("data", "alerta_humedad.txt")
        self.rango_definido = False
        self.ciclo_id = None
        self.programacion_id = None
        self.tipo_grafico = "cerrado"

        self.crear_ui()
        self.mostrar_humedad_actual()
        self.mostrar_grafico()

    def crear_ui(self):
        top_frame = tk.Frame(self, bg="#FFFFFF")
        top_frame.pack(fill="x", pady=5)

        header = tk.Frame(top_frame, bg="#096B35", height=60)
        header.pack(fill="x")

        tk.Label(header, text="Humedad", font=("Segoe UI", 16, "bold"),
                 fg="white", bg="#096B35").pack(side="left", padx=15, pady=15)

        tk.Button(header, text="Volver", command=self.volver_callback,
                  bg="white", fg="#096B35", font=("Segoe UI", 10, "bold"),
                  relief="flat", padx=10, pady=2).pack(side="right", padx=10, pady=10)

        self.lbl_actual = tk.Label(top_frame, text="", font=("Segoe UI", 14), bg="#FFFFFF")
        self.lbl_actual.pack(pady=10)

        # Rango aceptable
        rango_frame = tk.Frame(top_frame, bg="#FFFFFF")
        rango_frame.pack(pady=5)
        tk.Label(rango_frame, text="Rango (%):", bg="#FFFFFF").grid(row=0, column=0)
        self.entry_min = tk.Entry(rango_frame, width=5)
        self.entry_min.grid(row=0, column=1)
        self.entry_max = tk.Entry(rango_frame, width=5)
        self.entry_max.grid(row=0, column=2)

        btn_definir = tk.Button(rango_frame, text="✓", width=2, command=self.definir_rango, bg="#7AC35D", fg="white")
        btn_definir.grid(row=0, column=3, padx=(5, 2))
        btn_limpiar = tk.Button(rango_frame, text="✕", width=2, command=self.limpiar_rango, bg="#C94A3D", fg="white")
        btn_limpiar.grid(row=0, column=4, padx=(0, 5))

        self.alerta_local = tk.Label(top_frame, text="", fg="red", bg="#FFFFFF", font=("Segoe UI", 10, "bold"))
        self.alerta_local.pack()

        # Botones de gráfico y lectura
        botones_grafico = tk.Frame(top_frame, bg="#FFFFFF")
        botones_grafico.pack(pady=5)
        tk.Button(botones_grafico, text="Ver datos techo cerrado", bg="#7AC35D", fg="white",
                  command=lambda: self.mostrar_grafico("cerrado")).pack(side="left", padx=10)
        tk.Button(botones_grafico, text="Ver datos techo abierto", bg="#7AC35D", fg="white",
                  command=lambda: self.mostrar_grafico("abierto")).pack(side="left", padx=10)

        tk.Button(top_frame, text="Leer humedad", bg="#7AC35D", fg="white",
                  command=self.leer_humedad_desde_arduino).pack(pady=5)

        # Ciclo automático
        ciclo_frame = tk.Frame(top_frame, bg="#FFFFFF")
        ciclo_frame.pack(pady=5)
        tk.Label(ciclo_frame, text="Ciclo automático (minutos):", bg="#FFFFFF").grid(row=0, column=0, padx=5)
        self.entry_minutos = tk.Entry(ciclo_frame, width=5)
        self.entry_minutos.grid(row=0, column=1, padx=5)
        tk.Button(ciclo_frame, text="Iniciar ciclo", bg="#7AC35D", fg="white",
                  command=self.iniciar_ciclo).grid(row=0, column=2, padx=5)

        # Programación horaria
        prog_frame = tk.Frame(top_frame, bg="#FFFFFF")
        prog_frame.pack(pady=5)
        tk.Label(prog_frame, text="Programar hora (HH:MM):", bg="#FFFFFF").grid(row=0, column=0, padx=5)
        self.entry_hora = tk.Entry(prog_frame, width=6)
        self.entry_hora.grid(row=0, column=1, padx=5)
        tk.Button(prog_frame, text="Programar", bg="#7AC35D", fg="white",
                  command=self.programar_medicion).grid(row=0, column=2, padx=5)

        tk.Button(top_frame, text="Detener ciclos", bg="#C94A3D", fg="white",
                  command=self.detener_todo).pack(pady=5)

        self.canvas_frame = tk.Frame(self, bg="#FFFFFF", height=250)
        self.canvas_frame.pack(fill="x", pady=5)

    def definir_rango(self):
        try:
            min_val = float(self.entry_min.get())
            max_val = float(self.entry_max.get())
            if min_val < max_val:
                self.rango_definido = True
                self.alerta_local.config(text="")
        except:
            self.rango_definido = False
            self.alerta_local.config(text="⚠️ Rango inválido")

    def limpiar_rango(self):
        self.entry_min.delete(0, tk.END)
        self.entry_max.delete(0, tk.END)
        self.alerta_local.config(text="")
        self.rango_definido = False
        if os.path.exists(self.archivo_alerta):
            os.remove(self.archivo_alerta)

    def leer_humedad_desde_arduino(self):
        try:
            self.serial_manager.arduino.reset_input_buffer()
            self.serial_manager.write("LEER:DHT")
            time.sleep(5)
            respuesta = self.serial_manager.leer_linea()

            if respuesta and "H:" in respuesta:
                partes = respuesta.replace("T:", "").replace("H:", "").split()
                humedad = float(partes[1])
                estado = self.obtener_estado_techo()

                os.makedirs("data", exist_ok=True)
                with open(self.archivo, "a", encoding="utf-8") as f:
                    f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M')}|{humedad}|{estado}\n")

                self.lbl_actual.config(text=f"Humedad actual: {humedad}%")
                self.verificar_rango(humedad)
                self.mostrar_grafico(self.tipo_grafico)
            else:
                self.lbl_actual.config(text="No se recibió una respuesta válida del Arduino.")
        except Exception as e:
            self.lbl_actual.config(text=f"Error: {e}")

    def verificar_rango(self, humedad):
        if not self.rango_definido:
            return
        try:
            min_val = float(self.entry_min.get())
            max_val = float(self.entry_max.get())
            if humedad < min_val or humedad > max_val:
                self.alerta_local.config(text="⚠️ Humedad fuera del rango")
                with open(self.archivo_alerta, "w", encoding="utf-8") as f:
                    f.write("ALERTA")
            else:
                self.alerta_local.config(text="")
                if os.path.exists(self.archivo_alerta):
                    os.remove(self.archivo_alerta)
        except:
            self.alerta_local.config(text="")

    def obtener_estado_techo(self):
        try:
            with open("data/estado_techo.txt", "r") as f:
                return f.read().strip().lower()
        except:
            return "cerrado"

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
            valor = ultima[1]
            self.lbl_actual.config(text=f"Humedad actual: {valor}%")

    def mostrar_grafico(self, tipo="cerrado"):
        self.tipo_grafico = tipo
        if not os.path.exists(self.archivo):
            return

        datos = []
        with open(self.archivo, "r", encoding="utf-8") as f:
            for linea in f:
                partes = linea.strip().split("|")
                if len(partes) < 3:
                    continue
                try:
                    tiempo = datetime.strptime(partes[0], "%Y-%m-%d %H:%M")
                    if tiempo.year != 2025:
                        continue
                    val = float(partes[1])
                    estado = partes[2].lower()
                    if estado == tipo:
                        datos.append((tiempo.strftime("%Y-%m-%d"), val))
                except:
                    continue

        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        if not datos:
            tk.Label(self.canvas_frame, text="No hay datos para graficar.", bg="#FFFFFF").pack()
            return

        fig, ax = plt.subplots(figsize=(5, 3.5), dpi=100)
        fechas, vals = zip(*datos)
        ax.plot(fechas, vals, marker='o', color='green')
        ax.set_title(f"Techo {tipo}", fontsize=10)
        ax.set_ylabel("Humedad (%)", fontsize=8)
        ax.set_xlabel("Fecha", fontsize=8)
        ax.tick_params(axis='x', labelsize=8, rotation=45)
        ax.tick_params(axis='y', labelsize=8)

        fig.tight_layout(pad=2.0)
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def iniciar_ciclo(self):
        try:
            minutos = float(self.entry_minutos.get())
            self.leer_humedad_desde_arduino()
            self.ciclo_id = self.after(int(minutos * 60 * 1000), self.iniciar_ciclo)
        except ValueError:
            self.lbl_actual.config(text="Ingrese un número válido de minutos.")

    def programar_medicion(self):
        hora_objetivo = self.entry_hora.get()
        now = datetime.now().strftime("%H:%M")
        if hora_objetivo == now:
            self.leer_humedad_desde_arduino()
        self.programacion_id = self.after(60 * 1000, self.programar_medicion)

    def detener_todo(self):
        if self.ciclo_id:
            self.after_cancel(self.ciclo_id)
            self.ciclo_id = None
        if self.programacion_id:
            self.after_cancel(self.programacion_id)
            self.programacion_id = None
        self.mostrar_humedad_actual()
