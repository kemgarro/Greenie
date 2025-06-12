import tkinter as tk
from tkinter import messagebox
import datetime
import os
import threading

class RiegoFrame(tk.Frame):
    def __init__(self, master, volver_callback, serial_manager):
        super().__init__(master, bg="#FFFFFF")
        self.volver_callback = volver_callback
        self.serial_manager = serial_manager
        self.timer_ciclo = None
        self.estado_riego = False
        self._riego_after_id = None


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

        self.btn_toggle_riego = tk.Button(manual, text="Encender", bg="#7AC35D", fg="white", command=self.toggle_riego)
        self.btn_toggle_riego.pack(pady=5)

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
                self.estado_riego = True
                self.btn_toggle_riego.config(text="Apagar")

                # Cancelar temporizador anterior si existe
                if self._riego_after_id:
                    self.after_cancel(self._riego_after_id)

                # Apagado automático en 10s
                self._riego_after_id = self.after(10000, self.apagar_riego)
            else:
                print("Arduino no conectado.")
        except Exception as e:
            print(f"Error al encender riego: {e}")




    def apagar_riego(self):
        try:
            if self.serial_manager and self.serial_manager.arduino and self.serial_manager.arduino.is_open:
                self.serial_manager.enviar("DESACTIVAR:BOMBA")
                self.registrar_evento("Riego apagado")
                self.estado_riego = False
                self.btn_toggle_riego.config(text="Encender")

                # Cancelar apagado automático si se apaga manualmente
                if self._riego_after_id:
                    self.after_cancel(self._riego_after_id)
                    self._riego_after_id = None
            else:
                print("Arduino no conectado.")
        except Exception as e:
            print(f"Error al apagar riego: {e}")


    def toggle_riego(self):
        if self.estado_riego:
            self.apagar_riego()
        else:
            self.encender_riego()




    def registrar_evento(self, texto):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        evento = f"[{now}] {texto}\n"
        os.makedirs("data", exist_ok=True)
        with open("data/historial_riego.txt", "a", encoding="utf-8") as f:
            f.write(evento)
        #messagebox.showinfo("Evento registrado", texto)

    def programar_ciclo(self):
        try:
            h = float(self.ciclo_horas.get())
            m = float(self.ciclo_minutos.get())
            if h <= 0 or m <= 0 or m >= h * 60:
                raise ValueError
            if self.timer_ciclo:
                self.timer_ciclo.cancel()
            self.registrar_evento(f"Ciclo de riego programado: cada {h}h por {m}min")
            self.iniciar_ciclo_riego(h, m)
        except ValueError:
            messagebox.showerror("Error", "Valores inválidos. Usa números positivos y minutos < horas*60.")

    def iniciar_ciclo_riego(self, horas, minutos):
        def ciclo():
            try:
                self.encender_riego()
                self.registrar_evento("Riego encendido automáticamente (ciclo)")
            except:
                pass

            def apagar():
                try:
                    self.apagar_riego()
                    self.registrar_evento("Riego apagado automáticamente (ciclo)")
                except:
                    pass
                espera_restante = max(0, horas * 3600 - minutos * 60)
                self.timer_ciclo = threading.Timer(espera_restante, ciclo)
                self.timer_ciclo.start()

            self.timer_ciclo = threading.Timer(minutos * 60, apagar)
            self.timer_ciclo.start()

        ciclo()


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