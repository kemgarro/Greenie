
import tkinter as tk
from tkinter import messagebox
import datetime
import os

class VentilacionFrame(tk.Frame):
    def __init__(self, master, volver_callback):
        super().__init__(master, bg="#FFFFFF")
        self.volver_callback = volver_callback
        self.crear_interfaz()

    def crear_interfaz(self):
        # Encabezado
        header = tk.Frame(self, bg="#096B35", height=60)
        header.pack(fill="x")
        tk.Label(header, text="Ventilación", font=("Segoe UI", 16, "bold"),
                 fg="white", bg="#096B35").pack(pady=15)

        # Encendido/apagado manual
        manual = tk.LabelFrame(self, text="Manual", bg="#FFFFFF", padx=10, pady=10)
        manual.pack(pady=10)

        tk.Button(manual, text="Encender", bg="#7AC35D", fg="white",
                  command=lambda: self.registrar_evento("Ventilador encendido")).pack(side="left", padx=5)
        tk.Button(manual, text="Apagar", bg="#7AC35D", fg="white",
                  command=lambda: self.registrar_evento("Ventilador apagado")).pack(side="left", padx=5)

        # Ciclo automático
        ciclo = tk.LabelFrame(self, text="Ciclo Automático", bg="#FFFFFF", padx=10, pady=10)
        ciclo.pack(pady=10)

        tk.Label(ciclo, text="Cada (h):", bg="#FFFFFF").grid(row=0, column=0)
        self.ciclo_horas = tk.Entry(ciclo, width=5)
        self.ciclo_horas.grid(row=0, column=1, padx=5)

        tk.Label(ciclo, text="Por (min):", bg="#FFFFFF").grid(row=0, column=2)
        self.ciclo_minutos = tk.Entry(ciclo, width=5)
        self.ciclo_minutos.grid(row=0, column=3, padx=5)

        tk.Button(ciclo, text="Programar ciclo", bg="#7AC35D", fg="white",
                  command=self.programar_ciclo).grid(row=1, column=0, columnspan=4, pady=5)

        # Horario diario
        horario = tk.LabelFrame(self, text="Encendido Diario", bg="#FFFFFF", padx=10, pady=10)
        horario.pack(pady=10)

        tk.Label(horario, text="Hora (HH:MM):", bg="#FFFFFF").grid(row=0, column=0)
        self.hora_fija = tk.Entry(horario, width=7)
        self.hora_fija.grid(row=0, column=1)

        tk.Button(horario, text="Programar horario", bg="#7AC35D", fg="white",
                  command=self.programar_horario).grid(row=1, column=0, columnspan=2, pady=5)

        
        # Encendido automático por temperatura
        auto = tk.LabelFrame(self, text="Encendido Automático", bg="#FFFFFF", padx=10, pady=10)
        auto.pack(pady=10)

        tk.Label(auto, text="Umbral (°C):", bg="#FFFFFF").grid(row=0, column=0)
        self.umbral_temp = tk.Entry(auto, width=7)
        self.umbral_temp.grid(row=0, column=1)

        tk.Button(auto, text="Establecer umbral", bg="#7AC35D", fg="white",
                  command=self.establecer_umbral).grid(row=1, column=0, columnspan=2, pady=5)
        # Botón de volver
        tk.Button(self, text="Volver", bg="#7AC35D", fg="white",
                font=("Segoe UI", 10), width=20,
                command=self.volver_callback).pack(pady=20)


    def establecer_umbral(self):
        try:
            umbral = float(self.umbral_temp.get())
            self.registrar_evento(f"Ventilación se activará si la temperatura supera {umbral}°C")
            with open("data/umbral_ventilacion.txt", "w") as f:
                f.write(str(umbral))
        except ValueError:
            messagebox.showerror("Error", "El valor debe ser un número.")

        # Historial
        tk.Button(self, text="Ver historial", bg="#7AC35D", fg="white",
                  command=self.ver_historial).pack(pady=5)

        # Volver
        tk.Button(self, text="Volver", bg="#7AC35D", fg="white",
                  command=self.volver_callback).pack(pady=10)

    def registrar_evento(self, texto):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        evento = f"[{now}] {texto}\n"
        with open("data/historial_ventilacion.txt", "a") as f:
            f.write(evento)
        messagebox.showinfo("Evento registrado", texto)

    def programar_ciclo(self):
        try:
            h = int(self.ciclo_horas.get())
            m = int(self.ciclo_minutos.get())
            self.registrar_evento(f"Ventilación programada cada {h}h por {m}min")
        except ValueError:
            messagebox.showerror("Error", "Valores inválidos para el ciclo")

    def programar_horario(self):
        hora = self.hora_fija.get().strip()
        try:
            datetime.datetime.strptime(hora, "%H:%M")
            self.registrar_evento(f"Encendido diario programado a las {hora}")
        except ValueError:
            messagebox.showerror("Error", "Formato de hora incorrecto. Usa HH:MM")
