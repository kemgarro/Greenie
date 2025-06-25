import tkinter as tk
from tkinter import ttk
import os
from PIL import Image, ImageTk

from src.ui.temperatura_frame import TemperaturaFrame  
from src.ui.humedad_frame import HumedadFrame
from src.ui.luz_frame import LuzFrame
from src.ui.fotos_frame import FotosFrame
from src.ui.perfil_frame import PerfilFrame
from src.ui.riego_frame import RiegoFrame
from src.ui.ventilacion_frame import VentilacionFrame
from src.ui.soporte_frame import SoporteFrame

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
        self.root.geometry("400x700")
        self.root.resizable(False, False)
        self.root.configure(bg="#F7F7F7")

        self.icon_loader = IconLoader()
        self.iconos = self.icon_loader.cargar_iconos([
            "temperatura", "humedad", "luz", "ventilacion", "riego",
            "fotos", "perfil"
        ])

        self.frames = {}
        self.alerta_agua = None
        self.alerta_temp = None
        self.alerta_humedad = None
        self.after_id_nivel = None
        self.crear_frames()
        self.mostrar_frame("principal")
        self.root.after(2000, self.verificar_alertas)
        self.root.mainloop()

    def crear_frames(self):
        self.frames["principal"] = self.crear_principal()

        clases_especiales = {
            "temperatura": lambda master, volver: TemperaturaFrame(master, volver, self.serial_manager),
            "humedad": lambda master, volver: HumedadFrame(master, volver, self.serial_manager),
            "luz": lambda master, volver: LuzFrame(master, volver, self.serial_manager),
            "fotos": lambda master, volver: FotosFrame(master, volver, self.serial_manager),
            "riego": lambda master, volver: RiegoFrame(master, volver, self.serial_manager),
            "perfil": lambda master, volver: PerfilFrame(master, volver, self.usuario["numero_serie"]),
            "ventilacion": lambda master, volver: VentilacionFrame(master, volver, self.serial_manager),
            "soporte": lambda master, volver: SoporteFrame(master, volver, self.usuario),
        }

        secciones = [
            "luz", "ventilacion", "riego", "fotos", "perfil",
            "temperatura", "humedad", "soporte"
        ]

        for s in secciones:
            self.frames[s] = clases_especiales[s](self.root, self.volver_a_principal)

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
                  command=lambda: self.mostrar_frame(destino)).pack(pady=8)

    def crear_principal(self):
        frame = tk.Frame(self.root, bg="#F7F7F7")

        header = tk.Frame(frame, bg="#096B35", height=60)
        header.pack(fill="x")
        tk.Label(header, text="Greenie", font=("Segoe UI", 18, "bold"),
                 fg="white", bg="#096B35").pack(pady=10)

        contenedor_botones = tk.Frame(frame, bg="#F7F7F7")
        contenedor_botones.pack(pady=15)

        secciones_ordenadas = [
            (" Temperatura", "temperatura"),
            (" Humedad", "humedad"),
            (" Luz", "luz"),
            (" Ventilación", "ventilacion"),
            (" Riego", "riego"),
            (" Fotos", "fotos"),
            (" Perfil", "perfil")
        ]

        for texto, clave in secciones_ordenadas:
            self.crear_boton_info(contenedor_botones, texto, clave, clave)

        # ALERTAS
        self.alerta_agua = tk.Label(frame, text="", bg="#F7F7F7", fg="red",
                                    font=("Segoe UI", 11, "bold"))
        self.alerta_agua.pack(pady=(5, 0))

        self.alerta_temp = tk.Label(frame, text="", bg="#F7F7F7", fg="red",
                                    font=("Segoe UI", 11, "bold"))
        self.alerta_temp.pack(pady=(5, 0))

        self.alerta_humedad = tk.Label(frame, text="", bg="#F7F7F7", fg="red",
                                       font=("Segoe UI", 11, "bold"))
        self.alerta_humedad.pack(pady=(5, 0))

        contenedor_inferior = tk.Frame(frame, bg="#F7F7F7")
        contenedor_inferior.pack(side="bottom", fill="x", pady=10)

        tk.Button(contenedor_inferior, text="Soporte",
                  font=("Segoe UI", 11),
                  bg="#7AC35D", fg="white",
                  width=25, height=1,
                  command=lambda: self.mostrar_frame("soporte")).pack(pady=(0, 15))

        tk.Button(contenedor_inferior, text="Cerrar sesión",
                  font=("Segoe UI", 11),
                  bg="#7AC35D", fg="white",
                  width=25, height=1,
                  command=self.cerrar_sesion).pack(pady=(0, 30))

        return frame

    def verificar_alertas(self):
        try:
            # Nivel de agua
            self.serial_manager.flush()
            respuesta = self.serial_manager.leer_nivel_agua()
            if respuesta and respuesta.strip().upper() == "AGUA:NO_DISPONIBLE":
                self.alerta_agua.config(text="⚠️ No hay agua en el tanque")
            else:
                self.alerta_agua.config(text="")

            # Alerta de temperatura
            ruta_temp = os.path.join("data", "alerta_temperatura.txt")
            if os.path.exists(ruta_temp):
                with open(ruta_temp, "r") as f:
                    contenido = f.read().strip()
                    if contenido:
                        self.alerta_temp.config(text="⚠️ Temperatura fuera del rango definido")
                    else:
                        self.alerta_temp.config(text="")
            else:
                self.alerta_temp.config(text="")

            # Alerta de humedad
            ruta_humedad = os.path.join("data", "alerta_humedad.txt")
            if os.path.exists(ruta_humedad):
                with open(ruta_humedad, "r") as f:
                    contenido = f.read().strip()
                    if contenido:
                        self.alerta_humedad.config(text="⚠️ Humedad fuera del rango definido")
                    else:
                        self.alerta_humedad.config(text="")
            else:
                self.alerta_humedad.config(text="")

        except Exception as e:
            print(f"[Error en verificación de alertas] {e}")

        self.after_id_nivel = self.root.after(5000, self.verificar_alertas)

    def volver_a_principal(self):
        self.mostrar_frame("principal")

    def cerrar_sesion(self):
        if self.after_id_nivel:
            self.root.after_cancel(self.after_id_nivel)
        self.root.destroy()
        import subprocess, sys
        subprocess.Popen(["python", "main.py"])
        sys.exit()
