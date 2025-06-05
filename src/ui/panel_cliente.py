import tkinter as tk
from tkinter import ttk
import os
from PIL import Image, ImageTk

from src.ui.temperatura_frame import TemperaturaFrame  
from src.ui.humedad_frame import HumedadFrame
from src.ui.ph_frame import PHFrame
from src.ui.luz_frame import LuzFrame
from src.ui.actualizar_frame import ActualizarFrame
from src.ui.fotos_frame import FotosFrame
from src.ui.perfil_frame import PerfilFrame
from src.ui.riego_frame import RiegoFrame
from src.ui.ventilacion_frame import VentilacionFrame

class IconLoader:
    def __init__(self, icon_dir="assets/icons", size=(24, 24)):
        self.icon_dir = icon_dir
        self.size = size
        self.iconos = {}

    def cargar_iconos(self, nombres):
        for nombre in nombres:
            ruta = os.path.join(self.icon_dir, f"{nombre}.png")
            if os.path.exists(ruta):
                img = Image.open(ruta).resize(self.size)
                self.iconos[nombre] = ImageTk.PhotoImage(img)
            else:
                self.iconos[nombre] = None
        return self.iconos

class PanelCliente:
    def __init__(self, usuario, serial_manager):
        self.usuario = usuario
        self.serial_manager = serial_manager
        self.root = tk.Tk()
        self.root.title("Greenie - Panel Cliente")
        self.root.geometry("400x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#F7F7F7")

        self.icon_loader = IconLoader()
        self.iconos = self.icon_loader.cargar_iconos([
            "temperatura", "humedad", "ph",
            "luz", "ventilacion", "riego",
            "fotos", "actualizar", "perfil"
        ])

        self.frames = {}
        self.crear_frames()
        self.mostrar_frame("principal")
        self.root.mainloop()

    def crear_frames(self):
        self.frames["principal"] = self.crear_principal()

        clases_especiales = {
            "temperatura": lambda master, volver: TemperaturaFrame(master, volver, self.serial_manager),
            "humedad": lambda master, volver: HumedadFrame(master, volver, self.serial_manager),
            "ph": lambda master, volver: PHFrame(master, volver),
            "luz": lambda master, volver: LuzFrame(master, volver, self.serial_manager),
            "fotos": lambda master, volver: FotosFrame(master, volver, self.serial_manager),
            "actualizar": lambda master, volver: ActualizarFrame(master, volver, self.serial_manager),
            "riego": lambda master, volver: RiegoFrame(master, volver, self.serial_manager),
            "perfil": lambda master, volver: PerfilFrame(master, volver),
            "ventilacion": lambda master, volver: VentilacionFrame(master, volver, self.serial_manager),
        }

        secciones = [
            "luz", "ventilacion", "riego", "fotos", "actualizar", "perfil",
            "temperatura", "humedad", "ph"
        ]

        for s in secciones:
            if s in clases_especiales:
                self.frames[s] = clases_especiales[s](self.root, self.volver_a_principal)
            else:
                self.frames[s] = self.crear_seccion(s.capitalize())

        for frame in self.frames.values():
            frame.place(x=0, y=0, relwidth=1, relheight=1)

    def mostrar_frame(self, nombre):
        self.frames[nombre].tkraise()

    def crear_boton_info(self, frame, texto, icono_clave, destino):
        tk.Button(frame, text=texto,
                  image=self.iconos[icono_clave],
                  compound="left", anchor="w",
                  font=("Segoe UI", 12),
                  bg="#DDDDDD", relief="flat", width=260,
                  command=lambda: self.mostrar_frame(destino)).pack(pady=10)

    def crear_principal(self):
        frame = tk.Frame(self.root, bg="#F7F7F7")

        header = tk.Frame(frame, bg="#096B35", height=60)
        header.pack(fill="x")
        tk.Label(header, text="Greenie", font=("Segoe UI", 18, "bold"),
                 fg="white", bg="#096B35").pack(pady=10)

        # Lecturas
        lecturas = [
            (" Temperatura: 24.5°C", "temperatura"),
            (" Humedad: 70%", "humedad"),
            (" pH: 8", "ph")
        ]
        for texto, clave in lecturas:
            self.crear_boton_info(frame, texto, clave, clave)

        # Botones de acción
        grid = tk.Frame(frame, bg="#F7F7F7")
        grid.pack(pady=20)

        botones = [
            ("Luz", "luz"),
            ("Ventilación", "ventilacion"),
            ("Riego", "riego"),
            ("Fotos", "fotos"),
            ("Actualizar", "actualizar"),
            ("Perfil", "perfil")
        ]

        for i, (texto, clave) in enumerate(botones):
            tk.Button(grid, text=texto,
                      font=("Segoe UI", 10), width=10, height=2,
                      bg="#7AC35D", fg="white",
                      command=lambda k=clave: self.mostrar_frame(k)).grid(row=i//3, column=i%3, padx=10, pady=10)

        tk.Button(frame, text="Cerrar sesión",
                  font=("Segoe UI", 12),
                  bg="#7AC35D", fg="white",
                  width=30, height=2,
                  command=self.cerrar_sesion).pack(pady=10)

        return frame

    def crear_seccion(self, titulo):
        frame = tk.Frame(self.root, bg="#FFFFFF")
        header = tk.Frame(frame, bg="#096B35", height=60)
        header.pack(fill="x")
        tk.Label(header, text=f"{titulo}", font=("Segoe UI", 16, "bold"),
                 fg="white", bg="#096B35").pack(pady=15)

        tk.Button(frame, text="Volver", bg="#7AC35D", fg="white",
                  font=("Segoe UI", 10), width=12,
                  command=lambda: self.mostrar_frame("principal")).pack(pady=20)

        return frame

    def volver_a_principal(self):
        self.mostrar_frame("principal")

    def cerrar_sesion(self):
        self.root.destroy()
        import subprocess, sys
        subprocess.Popen(["python", "main.py"])
        sys.exit()
