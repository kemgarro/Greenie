import tkinter as tk
import os
import subprocess
import sys
from PIL import Image, ImageTk
from src.ui.usuarios_frame import UsuariosFrame
from src.ui.llamadas_frame import LlamadasFrame
from src.ui.seguimiento_frame import SeguimientoFrame

class PanelAdmin:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Greenie - Panel Administrador")
        self.root.geometry("420x620")
        self.root.resizable(False, False)
        self.root.configure(bg="#F7F7F7")

        self.frames = {}
        self.crear_frames()
        self.mostrar_frame("principal")
        self.root.mainloop()

    def crear_frames(self):
        self.frames["principal"] = self.crear_principal()

        clases_especiales = {
            "usuarios": UsuariosFrame,
            "llamadas": LlamadasFrame,
            "seguimiento": SeguimientoFrame,
        }

        for clave, clase in clases_especiales.items():
            self.frames[clave] = clase(self.root, self.volver_a_principal)

        for frame in self.frames.values():
            frame.place(x=0, y=0, relwidth=1, relheight=1)

    def mostrar_frame(self, nombre):
        self.frames[nombre].tkraise()

    def crear_principal(self):
        frame = tk.Frame(self.root, bg="#F7F7F7")

        # Header con título y logo
        header = tk.Frame(frame, bg="#096B35", height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        # Contenedor del título y logo
        titulo_logo_frame = tk.Frame(header, bg="#096B35")
        titulo_logo_frame.pack(fill="both", expand=True, padx=10)

        # Título a la izquierda
        tk.Label(titulo_logo_frame, text="Panel Administrador", font=("Segoe UI", 18, "bold"),
                 fg="white", bg="#096B35").pack(side="left", anchor="w")

        # Logo a la derecha
        logo_path = os.path.join("assets", "logos", "logo.png")
        if os.path.exists(logo_path):
            img = Image.open(logo_path).resize((60, 50))
            self.logo_img = ImageTk.PhotoImage(img)
            tk.Label(titulo_logo_frame, image=self.logo_img, bg="#096B35").pack(side="right")

        # Botones principales
        botones_frame = tk.Frame(frame, bg="#F7F7F7")
        botones_frame.pack(expand=True, pady=40)

        acciones = [
            ("Gestión de Usuarios", "usuarios"),
            ("Llamadas de Servicio", "llamadas"),
            ("Seguimiento de Atención", "seguimiento"),
        ]

        for texto, clave in acciones:
            tk.Button(botones_frame, text=texto,
                      font=("Segoe UI", 12),
                      bg="#7AC35D", fg="white",
                      width=30, height=2,
                      relief="flat",
                      command=lambda k=clave: self.mostrar_frame(k)).pack(pady=12)

        # Botón cerrar sesión
        tk.Button(frame, text="Cerrar sesión",
                  font=("Segoe UI", 12),
                  bg="#D9534F", fg="white",
                  width=30, height=2,
                  relief="flat",
                  command=self.cerrar_sesion).pack(pady=20)

        return frame

    def volver_a_principal(self):
        self.mostrar_frame("principal")

    def cerrar_sesion(self):
        self.root.destroy()
        subprocess.Popen(["python", "main.py"])
        sys.exit()
