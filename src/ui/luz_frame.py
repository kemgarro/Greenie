
import tkinter as tk
from tkinter import messagebox
import os
import datetime
import serial

class LuzFrame(tk.Frame):
    def __init__(self, master, volver_callback):
        super().__init__(master, bg="#FFFFFF")
        self.volver_callback = volver_callback
        self.estado_luz = False
        self.estado_techo = False
        self.crear_interfaz()

    def crear_interfaz(self):
        # Encabezado
        header = tk.Frame(self, bg="#096B35", height=60)
        header.pack(fill="x")
        tk.Label(header, text="Luz y Techo", font=("Segoe UI", 16, "bold"),
                 fg="white", bg="#096B35").pack(pady=15)

        # Sección Luz
        luz_frame = tk.LabelFrame(self, text="Luz Artificial", bg="#FFFFFF", padx=10, pady=10)
        luz_frame.pack(pady=10, fill="x", padx=10)

        self.btn_luz = tk.Button(luz_frame, text="Encender Luz", bg="#7AC35D", fg="white",
                                 command=lambda: enviar_a_arduino("LUZ_ON"))
        self.btn_luz.pack(pady=5)

        ciclo_luz = tk.LabelFrame(luz_frame, text="Ciclo Automático", bg="#FFFFFF", padx=5, pady=5)
        ciclo_luz.pack(pady=5)
        self.luz_cada_h = tk.Entry(ciclo_luz, width=5)
        self.luz_por_m = tk.Entry(ciclo_luz, width=5)
        tk.Label(ciclo_luz, text="Cada (h):", bg="#FFFFFF").grid(row=0, column=0)
        self.luz_cada_h.grid(row=0, column=1)
        tk.Label(ciclo_luz, text="Por (min):", bg="#FFFFFF").grid(row=0, column=2)
        self.luz_por_m.grid(row=0, column=3)
        tk.Button(ciclo_luz, text="Aplicar", command=self.aplicar_ciclo_luz).grid(row=0, column=4, padx=5)

        hora_fija_luz = tk.LabelFrame(luz_frame, text="Encendido Diario", bg="#FFFFFF", padx=5, pady=5)
        hora_fija_luz.pack(pady=5)
        self.hora_fija_luz = tk.Entry(hora_fija_luz, width=7)
        tk.Label(hora_fija_luz, text="Hora (HH:MM):", bg="#FFFFFF").grid(row=0, column=0)
        self.hora_fija_luz.grid(row=0, column=1)
        tk.Button(hora_fija_luz, text="Programar", command=self.programar_hora_luz).grid(row=0, column=2, padx=5)

        # Sección Techo
        techo_frame = tk.LabelFrame(self, text="Techo", bg="#FFFFFF", padx=10, pady=10)
        techo_frame.pack(pady=10, fill="x", padx=10)

        self.btn_techo = tk.Button(techo_frame, text="Abrir Techo", bg="#7AC35D", fg="white",
                                   command=self.toggle_techo)
        self.btn_techo.pack(pady=5)

        ciclo_techo = tk.LabelFrame(techo_frame, text="Ciclo Automático", bg="#FFFFFF", padx=5, pady=5)
        ciclo_techo.pack(pady=5)
        self.techo_cada_h = tk.Entry(ciclo_techo, width=5)
        self.techo_por_m = tk.Entry(ciclo_techo, width=5)
        tk.Label(ciclo_techo, text="Cada (h):", bg="#FFFFFF").grid(row=0, column=0)
        self.techo_cada_h.grid(row=0, column=1)
        tk.Label(ciclo_techo, text="Por (min):", bg="#FFFFFF").grid(row=0, column=2)
        self.techo_por_m.grid(row=0, column=3)
        tk.Button(ciclo_techo, text="Aplicar", command=self.aplicar_ciclo_techo).grid(row=0, column=4, padx=5)

        hora_fija_techo = tk.LabelFrame(techo_frame, text="Apertura Diaria", bg="#FFFFFF", padx=5, pady=5)
        hora_fija_techo.pack(pady=5)
        self.hora_fija_techo = tk.Entry(hora_fija_techo, width=7)
        tk.Label(hora_fija_techo, text="Hora (HH:MM):", bg="#FFFFFF").grid(row=0, column=0)
        self.hora_fija_techo.grid(row=0, column=1)
        tk.Button(hora_fija_techo, text="Programar", command=self.programar_hora_techo).grid(row=0, column=2, padx=5)

        # Historial
        tk.Button(self, text="Ver Historial", bg="#7AC35D", fg="white",
                  command=self.ver_historial).pack(pady=10)

        # Volver
        tk.Button(self, text="Volver", bg="#7AC35D", fg="white",
                  command=self.volver_callback).pack(pady=5)

    def toggle_luz(self):
        self.estado_luz = not self.estado_luz
        estado = "encendida" if self.estado_luz else "apagada"
        self.btn_luz.config(text="Apagar Luz" if self.estado_luz else "Encender Luz")
        self.registrar_evento(f"Luz {estado} manualmente.")

    def toggle_techo(self):
        self.estado_techo = not self.estado_techo
        estado = "abierto" if self.estado_techo else "cerrado"
        self.btn_techo.config(text="Cerrar Techo" if self.estado_techo else "Abrir Techo")
        self.registrar_evento(f"Techo {estado} manualmente.")

    def aplicar_ciclo_luz(self):
        h = self.luz_cada_h.get()
        m = self.luz_por_m.get()
        self.registrar_evento(f"Ciclo luz programado: cada {h}h por {m}min.")

    def aplicar_ciclo_techo(self):
        h = self.techo_cada_h.get()
        m = self.techo_por_m.get()
        self.registrar_evento(f"Ciclo techo programado: cada {h}h por {m}min.")

    def programar_hora_luz(self):
        hora = self.hora_fija_luz.get().strip()
        try:
            datetime.datetime.strptime(hora, "%H:%M")
            self.registrar_evento(f"Encendido luz diario programado a las {hora}")
            messagebox.showinfo("Programado", f"Luz programada para las {hora} diariamente.")
        except ValueError:
            messagebox.showerror("Error", "Formato de hora incorrecto. Usa HH:MM")

    def programar_hora_techo(self):
        hora = self.hora_fija_techo.get().strip()
        try:
            datetime.datetime.strptime(hora, "%H:%M")
            self.registrar_evento(f"Apertura techo diaria programada a las {hora}")
            messagebox.showinfo("Programado", f"Apertura del techo programada para las {hora} diariamente.")
        except ValueError:
            messagebox.showerror("Error", "Formato de hora incorrecto. Usa HH:MM")

    def ver_historial(self):
        top = tk.Toplevel(self)
        top.title("Historial de eventos")
        top.geometry("350x300")
        top.configure(bg="#FFFFFF")

        text = tk.Text(top, wrap="word", bg="#FFFFFF", font=("Segoe UI", 10))
        text.pack(fill="both", expand=True)

        if os.path.exists("data/historial_luz.txt"):
            with open("data/historial_luz.txt", "r") as f:
                contenido = f.read()
                text.insert("1.0", contenido)
        else:
            text.insert("1.0", "No hay historial disponible.")

    def registrar_evento(self, texto):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linea = f"[{timestamp}] {texto}\n"
        with open("data/historial_luz.txt", "a") as f:
            f.write(linea)


def enviar_a_arduino(comando):
    try:
        with serial.Serial("COM4", 9600, timeout=1) as arduino:  # Asegúrate que COM4 es correcto
            arduino.write((comando + "\n").encode())
    except serial.SerialException:
        print("Error: No se pudo comunicar con el Arduino.")
