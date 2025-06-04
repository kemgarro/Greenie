
import tkinter as tk
import os
import subprocess
import sys
from src.ui.usuarios_frame import UsuariosFrame

class PanelAdmin:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Greenie - Panel Administrador")
        self.root.geometry("400x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#F7F7F7")

        self.frames = {}
        self.crear_frames()
        self.mostrar_frame("principal")
        self.root.mainloop()

    def crear_frames(self):
        self.frames["principal"] = self.crear_principal()
        secciones = ["usuarios", "productos", "llamadas", "seguimiento", "historial"]

        for s in secciones:
            if s == "usuarios":
                self.frames[s] = UsuariosFrame(self.root, self.volver_a_principal)
            else:
                self.frames[s] = self.crear_seccion(s.capitalize())

        for frame in self.frames.values():
            frame.place(x=0, y=0, relwidth=1, relheight=1)

    def mostrar_frame(self, nombre):
        self.frames[nombre].tkraise()

    def crear_principal(self):
        frame = tk.Frame(self.root, bg="#F7F7F7")

        header = tk.Frame(frame, bg="#096B35", height=60)
        header.pack(fill="x")
        tk.Label(header, text="Greenie - Admin", font=("Segoe UI", 18, "bold"),
                 fg="white", bg="#096B35").pack(pady=10)

        acciones = [
            ("Usuarios", "usuarios"),
            ("Productos", "productos"),
            ("Llamadas", "llamadas"),
            ("Seguimiento", "seguimiento"),
            ("Historial", "historial")
        ]

        for texto, clave in acciones:
            tk.Button(frame, text=texto,
                      font=("Segoe UI", 12),
                      bg="#7AC35D", fg="white",
                      width=30, height=2,
                      command=lambda k=clave: self.mostrar_frame(k)).pack(pady=10)

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
        tk.Label(header, text=titulo, font=("Segoe UI", 16, "bold"),
                 fg="white", bg="#096B35").pack(pady=15)

        tk.Button(frame, text="Volver", bg="#7AC35D", fg="white",
                  font=("Segoe UI", 10), width=12,
                  command=lambda: self.mostrar_frame("principal")).pack(pady=20)
        return frame

    def volver_a_principal(self):
        self.mostrar_frame("principal")

    def cerrar_sesion(self):
        self.root.destroy()
        subprocess.Popen(["python", "main.py"])
        sys.exit()
