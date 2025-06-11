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

        tk.Button(self, text="Ver Historial", bg="#7AC35D", fg="white", command=self.ver_historial).pack(pady=10)
        tk.Button(self, text="Volver", bg="#7AC35D", fg="white", command=self.volver_callback).pack(pady=5)

    def crear_seccion_luz(self):
        luz_frame = tk.LabelFrame(self, text="Luz Artificial", bg="#FFFFFF", padx=10, pady=10)
        luz_frame.pack(pady=10, fill="x", padx=10)

        self.btn_luz = tk.Button(luz_frame, text="Encender Luz", bg="#7AC35D", fg="white", command=lambda: self.controlar_luz(True))
        self.btn_luz.pack(pady=5)

        self.btn_luz_apagar = tk.Button(luz_frame, text="Apagar Luz", bg="#7AC35D", fg="white", command=lambda: self.controlar_luz(False))
        self.btn_luz_apagar.pack(pady=5)

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
        tk.Label(hora_fija, text="Hora (HH:MM):", bg="#FFFFFF").grid(row=0, column=0)
        self.hora_fija_luz.grid(row=0, column=1)
        tk.Button(hora_fija, text="Programar", command=self.programar_hora_luz).grid(row=0, column=2, padx=5)

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
        tk.Label(hora_fija, text="Hora (HH:MM):", bg="#FFFFFF").grid(row=0, column=0)
        self.hora_fija_techo.grid(row=0, column=1)
        tk.Button(hora_fija, text="Programar", command=self.programar_hora_techo).grid(row=0, column=2, padx=5)

    def controlar_luz(self, encender):
        try:
            comando = "ACTIVAR:LEDS" if encender else "DESACTIVAR:LEDS"
            self.serial_manager.enviar(comando)
            estado = "encendida" if encender else "apagada"
            self.registrar_evento(f"Luz {estado} manualmente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo controlar la luz: {e}")

    def toggle_techo(self):
        self.estado_techo = not self.estado_techo
        estado = "abierto" if self.estado_techo else "cerrado"
        if self.winfo_exists():
            self.btn_techo.config(text="Cerrar Techo" if self.estado_techo else "Abrir Techo")
        comando = "SERVO:180" if self.estado_techo else "SERVO:0"
        self.serial_manager.enviar(comando)
        self.registrar_evento(f"Techo {estado} manualmente.")

    def aplicar_ciclo_luz(self):
        try:
            h = float(self.luz_cada_h.get())
            m = float(self.luz_por_m.get())
            if h <= 0 or m <= 0 or m >= h * 60:
                raise ValueError
            if self.timer_ciclo_luz:
                self.timer_ciclo_luz.cancel()
            self.registrar_evento(f"Ciclo luz programado: cada {h}h por {m}min.")
            self.iniciar_ciclo_luz(horas=h, minutos=m)
        except ValueError:
            messagebox.showerror("Error", "Valores inválidos. Usa números positivos y asegúrate de que minutos < horas*60.")

    def aplicar_ciclo_techo(self):
        try:
            h = float(self.techo_cada_h.get())
            m = float(self.techo_por_m.get())
            if h <= 0 or m <= 0 or m >= h * 60:
                raise ValueError
            if self.timer_ciclo_techo:
                self.timer_ciclo_techo.cancel()
            self.registrar_evento(f"Ciclo techo programado: cada {h}h por {m}min.")
            self.iniciar_ciclo_techo(horas=h, minutos=m)
        except ValueError:
            messagebox.showerror("Error", "Valores inválidos. Usa números positivos y asegúrate de que minutos < horas*60.")

    def programar_hora_luz(self):
        hora = self.hora_fija_luz.get().strip()
        try:
            datetime.datetime.strptime(hora, "%H:%M")
            self.registrar_evento(f"Encendido luz diario programado a las {hora}")
            with open("data/hora_luz.txt", "w") as f:
                f.write(hora)
            self.verificar_hora_luz()
            messagebox.showinfo("Programado", f"Luz programada para las {hora} diariamente.")
        except ValueError:
            messagebox.showerror("Error", "Formato de hora incorrecto. Usa HH:MM")

    def programar_hora_techo(self):
        hora = self.hora_fija_techo.get().strip()
        try:
            datetime.datetime.strptime(hora, "%H:%M")
            self.registrar_evento(f"Apertura techo diaria programada a las {hora}")
            with open("data/hora_techo.txt", "w") as f:
                f.write(hora)
            self.verificar_hora_techo()
            messagebox.showinfo("Programado", f"Apertura del techo programada para las {hora} diariamente.")
        except ValueError:
            messagebox.showerror("Error", "Formato de hora incorrecto. Usa HH:MM")

    def iniciar_ciclo_luz(self, horas, minutos):
        def ciclo():
            try:
                self.controlar_luz(True)
                self.registrar_evento("Encendido automático de luz (ciclo)")
            except:
                pass

            def apagar():
                try:
                    self.controlar_luz(False)
                    self.registrar_evento("Apagado automático de luz (ciclo)")
                except:
                    pass
                total_segundos = horas * 3600
                espera_restante = max(0, total_segundos - minutos * 60)
                self.timer_ciclo_luz = threading.Timer(espera_restante, ciclo)
                self.timer_ciclo_luz.start()

            self.timer_ciclo_luz = threading.Timer(minutos * 60, apagar)
            self.timer_ciclo_luz.start()

        ciclo()

    def iniciar_ciclo_techo(self, horas, minutos):
        def ciclo():
            try:
                self.estado_techo = True
                if self.winfo_exists():
                    self.btn_techo.config(text="Cerrar Techo")
                self.serial_manager.enviar("SERVO:180")
                self.registrar_evento("Techo abierto automáticamente (ciclo)")
            except:
                pass

            def cerrar():
                try:
                    self.estado_techo = False
                    if self.winfo_exists():
                        self.btn_techo.config(text="Abrir Techo")
                    self.serial_manager.enviar("SERVO:0")
                    self.registrar_evento("Techo cerrado automáticamente (ciclo)")
                except:
                    pass
                total_segundos = horas * 3600
                espera_restante = max(0, total_segundos - minutos * 60)
                self.timer_ciclo_techo = threading.Timer(espera_restante, ciclo)
                self.timer_ciclo_techo.start()

            self.timer_ciclo_techo = threading.Timer(minutos * 60, cerrar)
            self.timer_ciclo_techo.start()

        ciclo()

    def verificar_hora_luz(self):
        try:
            with open("data/hora_luz.txt", "r") as f:
                hora_programada = f.read().strip()
            ahora = datetime.datetime.now().strftime("%H:%M")
            if ahora == hora_programada:
                self.controlar_luz(True)
                self.registrar_evento("Luz encendida automáticamente por hora programada")
                self.after_id_luz = self.after(61000, self.verificar_hora_luz)
                return
        except:
            pass
        self.after_id_luz = self.after(10000, self.verificar_hora_luz)

    def verificar_hora_techo(self):
        try:
            with open("data/hora_techo.txt", "r") as f:
                hora_programada = f.read().strip()
            ahora = datetime.datetime.now().strftime("%H:%M")
            if ahora == hora_programada and not self.estado_techo:
                self.estado_techo = True
                if self.winfo_exists():
                    self.btn_techo.config(text="Cerrar Techo")
                self.serial_manager.enviar("SERVO:180")
                self.registrar_evento("Techo abierto automáticamente por hora programada")
                self.after_id_techo = self.after(61000, self.verificar_hora_techo)
                return
        except:
            pass
        self.after_id_techo = self.after(10000, self.verificar_hora_techo)

    def ver_historial(self):
        top = tk.Toplevel(self)
        top.title("Historial de eventos")
        top.geometry("350x300")
        top.configure(bg="#FFFFFF")
        text = tk.Text(top, wrap="word", bg="#FFFFFF", font=("Segoe UI", 10))
        text.pack(fill="both", expand=True)
        if os.path.exists("data/historial_luz.txt"):
            with open("data/historial_luz.txt", "r") as f:
                text.insert("1.0", f.read())
        else:
            text.insert("1.0", "No hay historial disponible.")

    def registrar_evento(self, texto):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linea = f"[{timestamp}] {texto}\n"
        os.makedirs("data", exist_ok=True)
        with open("data/historial_luz.txt", "a") as f:
            f.write(linea)
