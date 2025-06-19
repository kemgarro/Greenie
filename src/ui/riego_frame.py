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
        self.after_id_horario = None
        self.hora_programada = None
        self.duracion_programada = None

        self.crear_interfaz()

    def crear_interfaz(self):
        header = tk.Frame(self, bg="#096B35", height=60)
        header.pack(fill="x")
        tk.Label(header, text="Riego", font=("Segoe UI", 16, "bold"), fg="white", bg="#096B35").pack(pady=15)

        manual = tk.LabelFrame(self, text="Manual", bg="#FFFFFF", padx=10, pady=10)
        manual.pack(pady=10)
        self.btn_toggle_riego = tk.Button(manual, text="Encender", bg="#7AC35D", fg="white", command=self.toggle_riego)
        self.btn_toggle_riego.pack(pady=5)

        ciclo = tk.LabelFrame(self, text="Ciclo Automático", bg="#FFFFFF", padx=10, pady=10)
        ciclo.pack(pady=10)
        tk.Label(ciclo, text="Cada (min):", bg="#FFFFFF").grid(row=0, column=0)
        self.ciclo_min_intervalo = tk.Entry(ciclo, width=5)
        self.ciclo_min_intervalo.grid(row=0, column=1, padx=5)
        tk.Label(ciclo, text="Por (min):", bg="#FFFFFF").grid(row=0, column=2)
        self.ciclo_min_duracion = tk.Entry(ciclo, width=5)
        self.ciclo_min_duracion.grid(row=0, column=3, padx=5)
        tk.Button(ciclo, text="Programar ciclo", bg="#7AC35D", fg="white", command=self.programar_ciclo).grid(row=1, column=0, columnspan=4, pady=5)

        horario = tk.LabelFrame(self, text="Encendido Diario", bg="#FFFFFF", padx=10, pady=10)
        horario.pack(pady=10)
        tk.Label(horario, text="Hora (HH:MM):", bg="#FFFFFF").grid(row=0, column=0)
        self.hora_fija = tk.Entry(horario, width=7)
        self.hora_fija.grid(row=0, column=1)
        tk.Label(horario, text="Por (min):", bg="#FFFFFF").grid(row=1, column=0)
        self.duracion_fija = tk.Entry(horario, width=5)
        self.duracion_fija.grid(row=1, column=1)
        tk.Button(horario, text="Programar horario", bg="#7AC35D", fg="white", command=self.programar_horario).grid(row=2, column=0, columnspan=2, pady=5)

        tk.Button(self, text="Detener ciclos", bg="red", fg="white", command=self.detener_ciclos).pack(pady=5)
        tk.Button(self, text="Ver historial", bg="#7AC35D", fg="white", command=self.ver_historial).pack(pady=5)
        tk.Button(self, text="Volver", bg="#7AC35D", fg="white", font=("Segoe UI", 10), width=20, command=self.volver_callback).pack(pady=20)

    def toggle_riego(self):
        if self.estado_riego:
            self.apagar_riego()
        else:
            self.encender_riego()

    def encender_riego(self):
        try:
            if self.serial_manager and self.serial_manager.arduino and self.serial_manager.arduino.is_open:
                self.serial_manager.enviar("ACTIVAR:BOMBA")
                self.registrar_evento("Riego encendido")
                self.estado_riego = True
                self.btn_toggle_riego.config(text="Apagar")
        except Exception as e:
            print(f"Error al encender riego: {e}")

    def apagar_riego(self):
        try:
            if self.serial_manager and self.serial_manager.arduino and self.serial_manager.arduino.is_open:
                self.serial_manager.enviar("DESACTIVAR:BOMBA")
                self.registrar_evento("Riego apagado")
                self.estado_riego = False
                self.btn_toggle_riego.config(text="Encender")
                if self.timer_ciclo:
                    self.timer_ciclo.cancel()
                    self.timer_ciclo = None
        except Exception as e:
            print(f"Error al apagar riego: {e}")

    def programar_ciclo(self):
        try:
            intervalo = float(self.ciclo_min_intervalo.get())
            duracion = float(self.ciclo_min_duracion.get())
            if intervalo <= 0 or duracion <= 0 or duracion >= intervalo:
                raise ValueError
            if self.timer_ciclo:
                self.timer_ciclo.cancel()
            self.registrar_evento(f"Ciclo riego cada {intervalo}min por {duracion}min")
            self.iniciar_ciclo(intervalo, duracion)
        except:
            messagebox.showerror("Error", "Valores inválidos para el ciclo")

    def iniciar_ciclo(self, intervalo, duracion):
        def ciclo():
            try:
                self.encender_riego()
                self.registrar_evento("Riego encendido (ciclo)")
            except:
                pass

            def apagar():
                try:
                    self.apagar_riego()
                    self.registrar_evento("Riego apagado (ciclo)")
                except:
                    pass
                espera = max(0, intervalo * 60 - duracion * 60)
                self.timer_ciclo = threading.Timer(espera, ciclo)
                self.timer_ciclo.start()

            self.timer_ciclo = threading.Timer(duracion * 60, apagar)
            self.timer_ciclo.start()

        ciclo()

    def programar_horario(self):
        hora = self.hora_fija.get().strip()
        try:
            duracion = float(self.duracion_fija.get())
            datetime.datetime.strptime(hora, "%H:%M")
            self.hora_programada = hora
            self.duracion_programada = duracion
            self.registrar_evento(f"Riego programado a las {hora} por {duracion} minutos")
            if self.after_id_horario:
                self.after_cancel(self.after_id_horario)
            self.verificar_hora_diaria()
        except:
            messagebox.showerror("Error", "Formato de hora incorrecto o duración inválida.")

    def verificar_hora_diaria(self):
        try:
            ahora = datetime.datetime.now().strftime("%H:%M")
            if ahora == self.hora_programada:
                self.encender_riego()
                self.registrar_evento("Riego encendido automáticamente (hora fija)")
                def apagar():
                    self.apagar_riego()
                    self.registrar_evento("Riego apagado automáticamente (hora fija)")
                threading.Timer(float(self.duracion_programada) * 60, apagar).start()
        except Exception as e:
            print(f"Error verificación horario: {e}")
        self.after_id_horario = self.after(60000, self.verificar_hora_diaria)

    def detener_ciclos(self):
        if self.timer_ciclo:
            self.timer_ciclo.cancel()
            self.timer_ciclo = None
        if self.after_id_horario:
            self.after_cancel(self.after_id_horario)
            self.after_id_horario = None
        self.registrar_evento("Todos los ciclos y horarios de riego detenidos")

    def ver_historial(self):
        top = tk.Toplevel(self)
        top.title("Historial de Riego")
        top.geometry("400x300")
        top.configure(bg="#FFFFFF")

        frame = tk.Frame(top, bg="#FFFFFF")
        frame.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        text = tk.Text(frame, wrap="word", yscrollcommand=scrollbar.set,
                       bg="#FFFFFF", font=("Segoe UI", 10))
        text.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=text.yview)

        ruta = "data/historial_riego.txt"
        if os.path.exists(ruta):
            with open(ruta, "r", encoding="utf-8") as f:
                text.insert("1.0", f.read())
        else:
            text.insert("1.0", "No hay historial disponible.")

    def registrar_evento(self, texto):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        evento = f"[{now}] {texto}\n"
        os.makedirs("data", exist_ok=True)
        with open("data/historial_riego.txt", "a", encoding="utf-8") as f:
            f.write(evento)
