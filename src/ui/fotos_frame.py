import tkinter as tk
from tkinter import messagebox
import os
import cv2
import time
from threading import Timer
from PIL import Image, ImageTk

class FotosFrame(tk.Frame):
    def __init__(self, master, volver_callback, serial_manager, indice_camara=1):
        super().__init__(master, bg="#FFFFFF")
        self.volver_callback = volver_callback
        self.serial_manager = serial_manager
        self.indice_camara = indice_camara  # 1 = DroidCam, 0 = webcam integrada
        self.programa_activa = False
        self.intervalo = 600  # 600 segundos = 10 minutos
        self.crear_interfaz()

        # Crear carpeta si no existe
        os.makedirs("fotos", exist_ok=True)

    def crear_interfaz(self):
        header = tk.Frame(self, bg="#096B35", height=60)
        header.pack(fill="x")
        tk.Label(header, text="Captura de Fotos", font=("Segoe UI", 16, "bold"),
                 fg="white", bg="#096B35").pack(pady=15)

        tk.Button(self, text="Tomar Foto", font=("Segoe UI", 12),
                  bg="#7AC35D", fg="white", width=22, height=2,
                  command=self.tomar_foto).pack(pady=10)

        tk.Button(self, text="Ver Última Foto", font=("Segoe UI", 12),
                  bg="#7AC35D", fg="white", width=22, height=2,
                  command=self.ver_ultima_foto).pack(pady=10)

        self.boton_programa = tk.Button(self, text="Iniciar Captura Automática", font=("Segoe UI", 12),
                                        bg="#7AC35D", fg="white", width=22, height=2,
                                        command=self.toggle_programacion)
        self.boton_programa.pack(pady=10)

        tk.Button(self, text="Volver", bg="#7AC35D", fg="white",
                  font=("Segoe UI", 10), width=12,
                  command=self.volver_callback).pack(pady=30)

    def tomar_foto(self):
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        nombre_archivo = os.path.join("fotos", f"foto_{timestamp}.jpg")

        cap = cv2.VideoCapture(self.indice_camara)
        time.sleep(1)  # Esperar estabilización
        ret, frame = cap.read()
        cap.release()

        if ret:
            cv2.imwrite(nombre_archivo, frame)
            messagebox.showinfo("Foto tomada", f"Foto guardada como:\n{nombre_archivo}")
        else:
            messagebox.showerror("Error", "No se pudo capturar la imagen. Verifica la conexión con DroidCam o cambia el índice de cámara.")

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

    def toggle_programacion(self):
        self.programa_activa = not self.programa_activa
        if self.programa_activa:
            self.boton_programa.config(text="Detener Captura Automática")
            self.programar_foto()
        else:
            self.boton_programa.config(text="Iniciar Captura Automática")

    def programar_foto(self):
        if self.programa_activa:
            self.tomar_foto()
            Timer(self.intervalo, self.programar_foto).start()
