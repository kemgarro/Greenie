import tkinter as tk
from tkinter import messagebox
import os
import cv2
import time
from threading import Timer
from PIL import Image, ImageTk

class FotosFrame(tk.Frame):
    def __init__(self, master, volver_callback, serial_manager):
        super().__init__(master, bg="#FFFFFF")
        self.volver_callback = volver_callback
        self.serial_manager = serial_manager
        self.ciclo_activo = False
        self.diario_activo = False
        self.timer_ciclo = None
        self.timer_diario = None

        os.makedirs("fotos", exist_ok=True)
        self.crear_interfaz()

    def crear_interfaz(self):
        header = tk.Frame(self, bg="#096B35", height=60)
        header.pack(fill="x")
        tk.Label(header, text="Captura de Fotos", font=("Segoe UI", 16, "bold"),
                 fg="white", bg="#096B35").pack(pady=15)

        tk.Button(self, text="Tomar Foto", font=("Segoe UI", 12),
                  bg="#7AC35D", fg="white", width=22, height=2,
                  command=self.tomar_foto).pack(pady=10)

        ciclo_frame = tk.LabelFrame(self, text="Ciclo Automático", bg="#FFFFFF", font=("Segoe UI", 10))
        ciclo_frame.pack(pady=10)
        tk.Label(ciclo_frame, text="Cada (h):", bg="#FFFFFF").grid(row=0, column=0, padx=5, pady=5)
        self.entry_cada_h = tk.Entry(ciclo_frame, width=5)
        self.entry_cada_h.grid(row=0, column=1)
        tk.Button(ciclo_frame, text="Aplicar", command=self.aplicar_ciclo).grid(row=0, column=2, padx=5)

        diario_frame = tk.LabelFrame(self, text="Foto Diaria", bg="#FFFFFF", font=("Segoe UI", 10))
        diario_frame.pack(pady=10)
        tk.Label(diario_frame, text="Hora (HH:MM):", bg="#FFFFFF").grid(row=0, column=0, padx=5, pady=5)
        self.entry_hora = tk.Entry(diario_frame, width=7)
        self.entry_hora.grid(row=0, column=1)
        tk.Button(diario_frame, text="Programar", command=self.programar_diario).grid(row=0, column=2, padx=5)

        tk.Button(self, text="Detener Ciclos", font=("Segoe UI", 12),
                  bg="#7AC35D", fg="white", width=22, height=2,
                  command=self.detener_ciclos).pack(pady=10)

        tk.Button(self, text="Ver Última Foto", font=("Segoe UI", 12),
                  bg="#7AC35D", fg="white", width=22, height=2,
                  command=self.ver_ultima_foto).pack(pady=10)

        tk.Button(self, text="Eliminar Todas las Fotos", font=("Segoe UI", 12),
                  bg="#D9534F", fg="white", width=22, height=2,
                  command=self.eliminar_fotos).pack(pady=10)

        tk.Button(self, text="Crear Timelapse", font=("Segoe UI", 12),
                  bg="#5BC0DE", fg="white", width=22, height=2,
                  command=self.crear_timelapse).pack(pady=10)

        tk.Button(self, text="Volver", bg="#7AC35D", fg="white",
                  font=("Segoe UI", 10), width=12,
                  command=self.volver_callback).pack(pady=30)

    def tomar_foto(self):
        cap = cv2.VideoCapture(2)  # Índice 2 (Iriun o dispositivo externo)
        time.sleep(1)
        ret, frame = cap.read()
        cap.release()
        if ret and frame is not None and frame.mean() > 10:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            ruta = os.path.join("fotos", f"foto_{timestamp}.jpg")
            cv2.imwrite(ruta, frame)
            print(f"[✅] Foto guardada: {ruta}")
        else:
            print("[❌] No se pudo capturar imagen válida.")

    def aplicar_ciclo(self):
        try:
            horas = float(self.entry_cada_h.get())
            if horas < 0.001:
                raise ValueError
            intervalo = horas * 3600
            self.ciclo_activo = True
            if self.timer_ciclo:
                self.timer_ciclo.cancel()
            self.timer_ciclo = Timer(intervalo, self.ejecutar_ciclo, [intervalo])
            self.timer_ciclo.start()
            messagebox.showinfo("Ciclo Activado", f"Se tomará una foto cada {horas} h.")
        except ValueError:
            messagebox.showerror("Error", "Ingrese un número válido mayor a 0 (ej: 0.01).")

    def ejecutar_ciclo(self, intervalo):
        if self.ciclo_activo:
            self.tomar_foto()
            self.timer_ciclo = Timer(intervalo, self.ejecutar_ciclo, [intervalo])
            self.timer_ciclo.start()

    def programar_diario(self):
        hora_str = self.entry_hora.get()
        try:
            h, m = map(int, hora_str.split(":"))
            if not (0 <= h <= 23 and 0 <= m <= 59):
                raise ValueError
            ahora = time.localtime()
            segundos_actuales = ahora.tm_hour * 3600 + ahora.tm_min * 60 + ahora.tm_sec
            segundos_objetivo = h * 3600 + m * 60
            espera = (segundos_objetivo - segundos_actuales) % 86400
            self.diario_activo = True
            if self.timer_diario:
                self.timer_diario.cancel()
            self.timer_diario = Timer(espera, self.ejecutar_diario, [h, m])
            self.timer_diario.start()
            messagebox.showinfo("Foto Diaria Programada", f"Se tomará una foto todos los días a las {hora_str}.")
        except:
            messagebox.showerror("Error", "Formato inválido. Usa HH:MM (ej. 14:30)")

    def ejecutar_diario(self, h, m):
        if self.diario_activo:
            self.tomar_foto()
            self.timer_diario = Timer(86400, self.ejecutar_diario, [h, m])
            self.timer_diario.start()

    def detener_ciclos(self):
        self.ciclo_activo = False
        self.diario_activo = False
        if self.timer_ciclo:
            self.timer_ciclo.cancel()
        if self.timer_diario:
            self.timer_diario.cancel()
        messagebox.showinfo("Ciclos detenidos", "Se han detenido todos los ciclos de fotos.")

    def ver_ultima_foto(self):
        fotos = sorted([f for f in os.listdir("fotos") if f.endswith(".jpg")])
        if not fotos:
            messagebox.showinfo("Sin fotos", "No hay fotos disponibles.")
            return
        ruta = os.path.join("fotos", fotos[-1])
        ventana = tk.Toplevel(self)
        ventana.title("Última Foto")
        img = Image.open(ruta)
        img.thumbnail((600, 400))
        foto = ImageTk.PhotoImage(img)
        lbl = tk.Label(ventana, image=foto)
        lbl.image = foto
        lbl.pack()

    def eliminar_fotos(self):
        confirmacion = messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas eliminar todas las fotos?")
        if confirmacion:
            ruta_fotos = "fotos"
            fotos = [f for f in os.listdir(ruta_fotos) if f.endswith(".jpg")]
            for foto in fotos:
                try:
                    os.remove(os.path.join(ruta_fotos, foto))
                except Exception as e:
                    print(f"Error al eliminar {foto}: {e}")
            messagebox.showinfo("Eliminado", "Todas las fotos han sido eliminadas.")

    def crear_timelapse(self):
        fotos = sorted([f for f in os.listdir("fotos") if f.endswith(".jpg")])
        if not fotos:
            messagebox.showinfo("Sin fotos", "No hay fotos para crear el timelapse.")
            return

        ruta = "timelapse.avi"
        img_path = os.path.join("fotos", fotos[0])
        frame = cv2.imread(img_path)
        alto, ancho, _ = frame.shape

        out = cv2.VideoWriter(ruta, cv2.VideoWriter_fourcc(*'XVID'), 5, (ancho, alto))

        for foto in fotos:
            img = cv2.imread(os.path.join("fotos", foto))
            if img is not None:
                resized = cv2.resize(img, (ancho, alto))
                out.write(resized)

        out.release()
        self.ver_timelapse(ruta)

    def ver_timelapse(self, ruta):
        ventana = tk.Toplevel(self)
        ventana.title("Timelapse")
        lbl = tk.Label(ventana)
        lbl.pack()

        def reproducir():
            cap = cv2.VideoCapture(ruta)
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                img = img.resize((600, 400))
                imgtk = ImageTk.PhotoImage(image=img)
                lbl.config(image=imgtk)
                lbl.image = imgtk
                ventana.update()
                time.sleep(0.2)

            cap.release()

        ventana.after(100, reproducir)
