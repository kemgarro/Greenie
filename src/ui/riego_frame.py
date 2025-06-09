import tkinter as tk
from tkinter import messagebox
import datetime
import os

class RiegoFrame(tk.Frame):
    def __init__(self, master, volver_callback, serial_manager):
        super().__init__(master, bg="#FFFFFF")
        self.volver_callback = volver_callback
        self.serial_manager = serial_manager
        self.crear_interfaz()

    def crear_interfaz(self):
        # Encabezado
        header = tk.Frame(self, bg="#096B35", height=60)
        header.pack(fill="x")
        tk.Label(header, text="Riego", font=("Segoe UI", 16, "bold"),
                 fg="white", bg="#096B35").pack(pady=15)

        # Encendido/apagado manual
        manual = tk.LabelFrame(self, text="Manual", bg="#FFFFFF", padx=10, pady=10)
        manual.pack(pady=10)

        tk.Button(manual, text="Encender", bg="#7AC35D", fg="white",
                  command=self.encender_riego).pack(side="left", padx=5)
        tk.Button(manual, text="Apagar", bg="#7AC35D", fg="white",
                  command=self.apagar_riego).pack(side="left", padx=5)

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

        # Historial
        tk.Button(self, text="Ver historial", bg="#7AC35D", fg="white",
                  command=self.ver_historial).pack(pady=5)

        # Volver
        tk.Button(self, text="Volver", bg="#7AC35D", fg="white",
                  font=("Segoe UI", 10), width=20,
                  command=self.volver_callback).pack(pady=20)

    def encender_riego(self):
        try:
            if self.serial_manager and self.serial_manager.arduino and self.serial_manager.arduino.is_open:
                self.serial_manager.enviar("ACTIVAR:BOMBA")
                self.registrar_evento("Riego encendido")

                # ✅ Cancelar temporizador anterior si existe
                after_id = getattr(self, "_riego_after_id", None)
                if after_id:
                    self.after_cancel(after_id)

                # ✅ Programar apagado automático
                self._riego_after_id = self.after(10000, self.apagar_riego)
            else:
                messagebox.showwarning("Desconectado", "Arduino no está conectado.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo encender el riego: {e}")



    def apagar_riego(self):
        try:
            if self.serial_manager and self.serial_manager.arduino and self.serial_manager.arduino.is_open:
                self.serial_manager.write("DESACTIVAR:BOMBA")
                self.registrar_evento("Riego apagado")
            else:
                messagebox.showwarning("Desconectado", "Arduino no está conectado.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo apagar el riego: {e}")


    def registrar_evento(self, texto):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        evento = f"[{now}] {texto}\n"
        os.makedirs("data", exist_ok=True)
        with open("data/historial_riego.txt", "a", encoding="utf-8") as f:
            f.write(evento)
        messagebox.showinfo("Evento registrado", texto)

    def programar_ciclo(self):
        try:
            h = int(self.ciclo_horas.get())
            m = int(self.ciclo_minutos.get())
            self.registrar_evento(f"Riego programado cada {h}h por {m}min")
        except ValueError:
            messagebox.showerror("Error", "Valores inválidos para el ciclo")

    def programar_horario(self):
        hora = self.hora_fija.get().strip()
        try:
            datetime.datetime.strptime(hora, "%H:%M")
            self.registrar_evento(f"Encendido diario programado a las {hora}")
        except ValueError:
            messagebox.showerror("Error", "Formato de hora incorrecto. Usa HH:MM")

    def ver_historial(self):
        ruta = "data/historial_riego.txt"
        if os.path.exists(ruta):
            with open(ruta, "r", encoding="utf-8") as f:
                contenido = f.read()
            messagebox.showinfo("Historial de Riego", contenido or "No hay eventos registrados aún.")
        else:
            messagebox.showinfo("Historial de Riego", "No hay historial disponible.")
