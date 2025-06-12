import tkinter as tk
from tkinter import messagebox
import datetime
import os
import threading

class VentilacionFrame(tk.Frame):
    def __init__(self, master, volver_callback, serial_manager):
        super().__init__(master, bg="#FFFFFF")
        self.volver_callback = volver_callback
        self.serial_manager = serial_manager
        self.estado_ventilador = False
        self.timer_ciclo = None
        self.after_id_horario = None
        self.hora_programada = None

        self.crear_interfaz()

    def crear_interfaz(self):
        header = tk.Frame(self, bg="#096B35", height=60)
        header.pack(fill="x")
        tk.Label(header, text="Ventilación", font=("Segoe UI", 16, "bold"),
                 fg="white", bg="#096B35").pack(pady=15)

        manual = tk.LabelFrame(self, text="Manual", bg="#FFFFFF", padx=10, pady=10)
        manual.pack(pady=10)

        self.btn_toggle_ventilador = tk.Button(manual, text="Encender", bg="#7AC35D", fg="white",command=self.toggle_ventilador)
        self.btn_toggle_ventilador.pack(pady=5)


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

        horario = tk.LabelFrame(self, text="Encendido Diario", bg="#FFFFFF", padx=10, pady=10)
        horario.pack(pady=10)

        tk.Label(horario, text="Hora (HH:MM):", bg="#FFFFFF").grid(row=0, column=0)
        self.hora_fija = tk.Entry(horario, width=7)
        self.hora_fija.grid(row=0, column=1)

        tk.Button(horario, text="Programar horario", bg="#7AC35D", fg="white",
                  command=self.programar_horario).grid(row=1, column=0, columnspan=2, pady=5)

        auto = tk.LabelFrame(self, text="Encendido Automático", bg="#FFFFFF", padx=10, pady=10)
        auto.pack(pady=10)

        tk.Label(auto, text="Umbral (°C):", bg="#FFFFFF").grid(row=0, column=0)
        self.umbral_temp = tk.Entry(auto, width=7)
        self.umbral_temp.grid(row=0, column=1)

        tk.Button(auto, text="Establecer umbral", bg="#7AC35D", fg="white",
                  command=self.establecer_umbral).grid(row=1, column=0, columnspan=2, pady=5)

        tk.Button(self, text="Ver historial", bg="#7AC35D", fg="white",
                  command=self.ver_historial).pack(pady=5)

        tk.Button(self, text="Volver", bg="#7AC35D", fg="white",
                  command=self.volver_callback).pack(pady=10)

    def controlar_ventilador(self, encender):
        try:
            comando = "ACTIVAR:VENTILADOR" if encender else "DESACTIVAR:VENTILADOR"
            self.serial_manager.enviar(comando)
            estado = "encendido" if encender else "apagado"
            self.registrar_evento(f"Ventilador {estado}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo controlar el ventilador: {e}")

    def establecer_umbral(self):
        try:
            umbral = float(self.umbral_temp.get())
            self.registrar_evento(f"Ventilación se activará si la temperatura supera {umbral}°C")
            os.makedirs("data", exist_ok=True)
            with open("data/umbral_ventilacion.txt", "w") as f:
                f.write(str(umbral))
            self.serial_manager.enviar(f"UMBRAL:TEMP:{umbral}")
        except ValueError:
            messagebox.showerror("Error", "El valor debe ser un número.")

    def programar_ciclo(self):
        try:
            h = float(self.ciclo_horas.get())
            m = float(self.ciclo_minutos.get())
            if h <= 0 or m <= 0 or m >= h * 60:
                raise ValueError
            if self.timer_ciclo:
                self.timer_ciclo.cancel()
            self.registrar_evento(f"Ventilación programada cada {h}h por {m}min")
            self.iniciar_ciclo_ventilador(h, m)
        except ValueError:
            messagebox.showerror("Error", "Valores inválidos para el ciclo")

             

    def iniciar_ciclo_ventilador(self, horas, minutos):
        def ciclo():
            try:
                self.controlar_ventilador(True)
                self.registrar_evento("Ventilador encendido (ciclo)")
            except:
                pass

            def apagar():
                try:
                    self.controlar_ventilador(False)
                    self.registrar_evento("Ventilador apagado (ciclo)")
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
            self.hora_programada = hora
            self.verificar_hora_diaria()
            self.registrar_evento(f"Encendido diario programado a las {hora}")
            os.makedirs("data", exist_ok=True)
            with open("data/hora_ventilacion.txt", "w") as f:
                f.write(hora)
        except ValueError:
            messagebox.showerror("Error", "Formato de hora incorrecto. Usa HH:MM")

    def verificar_hora_diaria(self):
        try:
            ahora = datetime.datetime.now().strftime("%H:%M")
            if ahora == self.hora_programada:
                self.controlar_ventilador(True)
                self.registrar_evento("Ventilador encendido automáticamente por horario")
                self.after_id_horario = self.after(61000, self.verificar_hora_diaria)
                return
        except:
            pass
        self.after_id_horario = self.after(10000, self.verificar_hora_diaria)

    def ver_historial(self):
        top = tk.Toplevel(self)
        top.title("Historial de Ventilación")
        top.geometry("400x300")
        top.configure(bg="#FFFFFF")

        text = tk.Text(top, wrap="word", bg="#FFFFFF", font=("Segoe UI", 10))
        text.pack(fill="both", expand=True)

        path = "data/historial_ventilacion.txt"
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                text.insert("1.0", f.read())
        else:
            text.insert("1.0", "No hay historial disponible.")

    def registrar_evento(self, texto):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        evento = f"[{now}] {texto}\n"
        os.makedirs("data", exist_ok=True)
        with open("data/historial_ventilacion.txt", "a", encoding="utf-8") as f:
            f.write(evento)
        #messagebox.showinfo("Evento registrado", texto)

    def toggle_ventilador(self):
        self.estado_ventilador = not self.estado_ventilador
        encender = self.estado_ventilador

        try:
            comando = "ACTIVAR:VENTILADOR" if encender else "DESACTIVAR:VENTILADOR"
            self.serial_manager.enviar(comando)

            texto = "Apagar" if encender else "Encender"
            self.btn_toggle_ventilador.config(text=texto)

            estado_txt = "encendido" if encender else "apagado"
            self.registrar_evento(f"Ventilador {estado_txt}")
        except Exception as e:
            print(f"[VentilacionFrame] Error al alternar ventilador: {e}")
            self.estado_ventilador = not self.estado_ventilador  # Revertir estado si falla

