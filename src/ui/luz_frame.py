import tkinter as tk
from tkinter import messagebox
import os
import datetime
import threading

class LuzFrame(tk.Frame):
    def __init__(self, master, volver_callback, serial_manager):
        super().__init__(master, bg="#FFFFFF")
        self.volver_callback = volver_callback
        self.serial_manager = serial_manager
        self.estado_luz = False
        self.estado_techo = False
        self.timer_ciclo_luz = None
        self.timer_ciclo_techo = None
        self.after_id_luz = None
        self.after_id_techo = None
        self.crear_interfaz()

    def crear_interfaz(self):
        header = tk.Frame(self, bg="#096B35", height=60)
        header.pack(fill="x")
        tk.Label(header, text="Luz y Techo", font=("Segoe UI", 16, "bold"), fg="white", bg="#096B35").pack(pady=15)

        self.crear_seccion_luz()
        self.crear_seccion_techo()

        tk.Button(self, text="Detener ciclos", bg="#C34F4F", fg="white", command=self.detener_todos_los_ciclos).pack(pady=5)
        tk.Button(self, text="Ver Historial", bg="#7AC35D", fg="white", command=self.ver_historial).pack(pady=5)
        tk.Button(self, text="Volver", bg="#7AC35D", fg="white", command=self.volver_callback).pack(pady=10)

    def crear_seccion_luz(self):
        luz_frame = tk.LabelFrame(self, text="Luz Artificial", bg="#FFFFFF", padx=10, pady=10)
        luz_frame.pack(pady=10, fill="x", padx=10)

        self.btn_toggle_luz = tk.Button(luz_frame, text="Encender Luz", bg="#7AC35D", fg="white", command=self.toggle_luz)
        self.btn_toggle_luz.pack(pady=5)

        self.crear_ciclo_luz(luz_frame)
        self.crear_hora_fija_luz(luz_frame)

    def crear_ciclo_luz(self, parent):
        ciclo_luz = tk.LabelFrame(parent, text="Ciclo Automático", bg="#FFFFFF", padx=5, pady=5)
        ciclo_luz.pack(pady=5)
        self.luz_cada_h = tk.Entry(ciclo_luz, width=5)
        self.luz_por_m = tk.Entry(ciclo_luz, width=5)
        tk.Label(ciclo_luz, text="Cada (h):", bg="#FFFFFF").grid(row=0, column=0)
        self.luz_cada_h.grid(row=0, column=1)
        tk.Label(ciclo_luz, text="Por (min):", bg="#FFFFFF").grid(row=0, column=2)
        self.luz_por_m.grid(row=0, column=3)
        tk.Button(ciclo_luz, text="Aplicar", command=self.aplicar_ciclo_luz).grid(row=0, column=4, padx=5)

    def crear_hora_fija_luz(self, parent):
        hora_fija = tk.LabelFrame(parent, text="Encendido Diario", bg="#FFFFFF", padx=5, pady=5)
        hora_fija.pack(pady=5)
        self.hora_fija_luz = tk.Entry(hora_fija, width=7)
        self.duracion_luz = tk.Entry(hora_fija, width=5)
        tk.Label(hora_fija, text="Hora (HH:MM):", bg="#FFFFFF").grid(row=0, column=0)
        self.hora_fija_luz.grid(row=0, column=1)
        tk.Label(hora_fija, text="Por (min):", bg="#FFFFFF").grid(row=0, column=2)
        self.duracion_luz.grid(row=0, column=3)
        tk.Button(hora_fija, text="Programar", command=self.programar_hora_luz).grid(row=0, column=4, padx=5)

    def crear_seccion_techo(self):
        techo_frame = tk.LabelFrame(self, text="Techo", bg="#FFFFFF", padx=10, pady=10)
        techo_frame.pack(pady=10, fill="x", padx=10)

        self.btn_techo = tk.Button(techo_frame, text="Abrir Techo", bg="#7AC35D", fg="white", command=self.toggle_techo)
        self.btn_techo.pack(pady=5)

        self.crear_ciclo_techo(techo_frame)
        self.crear_hora_fija_techo(techo_frame)

    def crear_ciclo_techo(self, parent):
        ciclo_techo = tk.LabelFrame(parent, text="Ciclo Automático", bg="#FFFFFF", padx=5, pady=5)
        ciclo_techo.pack(pady=5)
        self.techo_cada_h = tk.Entry(ciclo_techo, width=5)
        self.techo_por_m = tk.Entry(ciclo_techo, width=5)
        tk.Label(ciclo_techo, text="Cada (h):", bg="#FFFFFF").grid(row=0, column=0)
        self.techo_cada_h.grid(row=0, column=1)
        tk.Label(ciclo_techo, text="Por (min):", bg="#FFFFFF").grid(row=0, column=2)
        self.techo_por_m.grid(row=0, column=3)
        tk.Button(ciclo_techo, text="Aplicar", command=self.aplicar_ciclo_techo).grid(row=0, column=4, padx=5)

    def crear_hora_fija_techo(self, parent):
        hora_fija = tk.LabelFrame(parent, text="Apertura Diaria", bg="#FFFFFF", padx=5, pady=5)
        hora_fija.pack(pady=5)
        self.hora_fija_techo = tk.Entry(hora_fija, width=7)
        self.duracion_techo = tk.Entry(hora_fija, width=5)
        tk.Label(hora_fija, text="Hora (HH:MM):", bg="#FFFFFF").grid(row=0, column=0)
        self.hora_fija_techo.grid(row=0, column=1)
        tk.Label(hora_fija, text="Por (min):", bg="#FFFFFF").grid(row=0, column=2)
        self.duracion_techo.grid(row=0, column=3)
        tk.Button(hora_fija, text="Programar", command=self.programar_hora_techo).grid(row=0, column=4, padx=5)

    def toggle_techo(self):
        self.estado_techo = not self.estado_techo
        comando = "SERVO:180" if self.estado_techo else "SERVO:0"
        texto = "Cerrar Techo" if self.estado_techo else "Abrir Techo"
        self.btn_techo.config(text=texto)
        self.serial_manager.enviar(comando)
        self.registrar_evento(f"Techo {'abierto' if self.estado_techo else 'cerrado'} manualmente.")

    def toggle_luz(self):
        self.estado_luz = not self.estado_luz
        comando = "ACTIVAR:LEDS" if self.estado_luz else "DESACTIVAR:LEDS"
        texto = "Apagar Luz" if self.estado_luz else "Encender Luz"
        self.btn_toggle_luz.config(text=texto)
        self.serial_manager.enviar(comando)
        self.registrar_evento(f"Luz {'encendida' if self.estado_luz else 'apagada'} manualmente.")

    def aplicar_ciclo_luz(self):
        try:
            h = float(self.luz_cada_h.get())
            m = float(self.luz_por_m.get())
            if h <= 0 or m <= 0 or m >= h * 60:
                raise ValueError
            if self.timer_ciclo_luz:
                self.timer_ciclo_luz.cancel()
            self.registrar_evento(f"Ciclo luz programado: cada {h}h por {m}min.")
            self.iniciar_ciclo_luz(h, m)
        except ValueError:
            messagebox.showerror("Error", "Valores inválidos. Usa decimales positivos y minutos < horas*60.")

    def iniciar_ciclo_luz(self, horas, minutos):
        def ciclo():
            self.toggle_luz()
            self.registrar_evento("Encendido automático de luz (ciclo)")

            def apagar():
                self.toggle_luz()
                self.registrar_evento("Apagado automático de luz (ciclo)")
                espera_restante = max(0, horas * 3600 - minutos * 60)
                self.timer_ciclo_luz = threading.Timer(espera_restante, ciclo)
                self.timer_ciclo_luz.start()

            self.timer_ciclo_luz = threading.Timer(minutos * 60, apagar)
            self.timer_ciclo_luz.start()

        ciclo()

    def aplicar_ciclo_techo(self):
        try:
            h = float(self.techo_cada_h.get())
            m = float(self.techo_por_m.get())
            if h <= 0 or m <= 0 or m >= h * 60:
                raise ValueError
            if self.timer_ciclo_techo:
                self.timer_ciclo_techo.cancel()
            self.registrar_evento(f"Ciclo techo programado: cada {h}h por {m}min.")
            self.iniciar_ciclo_techo(h, m)
        except ValueError:
            messagebox.showerror("Error", "Valores inválidos. Usa decimales positivos y minutos < horas*60.")

    def iniciar_ciclo_techo(self, horas, minutos):
        def ciclo():
            self.toggle_techo()
            self.registrar_evento("Techo abierto automáticamente (ciclo)")

            def cerrar():
                self.toggle_techo()
                self.registrar_evento("Techo cerrado automáticamente (ciclo)")
                espera_restante = max(0, horas * 3600 - minutos * 60)
                self.timer_ciclo_techo = threading.Timer(espera_restante, ciclo)
                self.timer_ciclo_techo.start()

            self.timer_ciclo_techo = threading.Timer(minutos * 60, cerrar)
            self.timer_ciclo_techo.start()

        ciclo()

    def programar_hora_luz(self):
        try:
            hora = self.hora_fija_luz.get().strip()
            duracion = float(self.duracion_luz.get())
            datetime.datetime.strptime(hora, "%H:%M")
            if duracion <= 0:
                raise ValueError
            with open("data/hora_luz.txt", "w") as f:
                f.write(f"{hora}|{duracion}")
            self.verificar_hora_luz()
            self.registrar_evento(f"Encendido luz diario programado a las {hora} por {duracion} minutos.")
        except ValueError:
            messagebox.showerror("Error", "Formato incorrecto o duración inválida.")

    def verificar_hora_luz(self):
        try:
            with open("data/hora_luz.txt", "r") as f:
                contenido = f.read().strip()
            hora, duracion = contenido.split("|")
            ahora = datetime.datetime.now().strftime("%H:%M")
            if ahora == hora:
                self.toggle_luz()
                self.registrar_evento("Luz encendida automáticamente (diario)")
                threading.Timer(float(duracion) * 60, lambda: [self.toggle_luz(), self.registrar_evento("Luz apagada automáticamente (diario)")]).start()
            self.after_id_luz = self.after(60000, self.verificar_hora_luz)
        except:
            pass

    def programar_hora_techo(self):
        try:
            hora = self.hora_fija_techo.get().strip()
            duracion = float(self.duracion_techo.get())
            datetime.datetime.strptime(hora, "%H:%M")
            if duracion <= 0:
                raise ValueError
            with open("data/hora_techo.txt", "w") as f:
                f.write(f"{hora}|{duracion}")
            self.verificar_hora_techo()
            self.registrar_evento(f"Apertura techo diaria programada a las {hora} por {duracion} minutos.")
        except ValueError:
            messagebox.showerror("Error", "Formato incorrecto o duración inválida.")

    def verificar_hora_techo(self):
        try:
            with open("data/hora_techo.txt", "r") as f:
                contenido = f.read().strip()
            hora, duracion = contenido.split("|")
            ahora = datetime.datetime.now().strftime("%H:%M")
            if ahora == hora:
                self.toggle_techo()
                self.registrar_evento("Techo abierto automáticamente (diario)")
                threading.Timer(float(duracion) * 60, lambda: [self.toggle_techo(), self.registrar_evento("Techo cerrado automáticamente (diario)")]).start()
            self.after_id_techo = self.after(60000, self.verificar_hora_techo)
        except:
            pass

    def detener_todos_los_ciclos(self):
        if self.timer_ciclo_luz:
            self.timer_ciclo_luz.cancel()
        if self.timer_ciclo_techo:
            self.timer_ciclo_techo.cancel()
        if self.after_id_luz:
            self.after_cancel(self.after_id_luz)
        if self.after_id_techo:
            self.after_cancel(self.after_id_techo)
        self.registrar_evento("Todos los ciclos y horarios detenidos.")

    def ver_historial(self):
        top = tk.Toplevel(self)
        top.title("Historial de Luz")
        top.geometry("400x300")
        top.configure(bg="#FFFFFF")

        scrollbar = tk.Scrollbar(top)
        scrollbar.pack(side="right", fill="y")

        text = tk.Text(top, wrap="word", bg="#FFFFFF", font=("Segoe UI", 10), yscrollcommand=scrollbar.set)
        text.pack(fill="both", expand=True)
        scrollbar.config(command=text.yview)

        if os.path.exists("data/historial_luz.txt"):
            with open("data/historial_luz.txt", "r") as f:
                text.insert("1.0", f.read())
        else:
            text.insert("1.0", "No hay historial disponible.")

    def registrar_evento(self, texto):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("data/historial_luz.txt", "a") as f:
            f.write(f"[{now}] {texto}\n")
