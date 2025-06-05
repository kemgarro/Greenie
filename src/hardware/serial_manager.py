import serial
import time

class SerialManager:
    def __init__(self, puerto="COM14", baudrate=9600, pines=None):
        self.pines = pines or {}
        try:
            self.arduino = serial.Serial(puerto, baudrate, timeout=1)
            time.sleep(2)  # Esperar a que el Arduino se reinicie
            print(f"Arduino conectado en {puerto}")
        except serial.SerialException:
            self.arduino = None
            print("Error: No se pudo abrir el puerto serial.")

    def enviar(self, comando):
        if self.arduino and self.arduino.is_open:
            try:
                self.arduino.write((comando.strip() + "\n").encode())
            except serial.SerialException:
                print("Error al enviar comando al Arduino.")
        else:
            print("Arduino no conectado.")

    def activar(self, componente):
        self.enviar(f"ACTIVAR:{componente.upper()}")

    def desactivar(self, componente):
        self.enviar(f"DESACTIVAR:{componente.upper()}")

    def mover_servo(self, angulo):
        self.enviar(f"SERVO:{angulo}")

    def leer_dht(self):
        self.enviar("LEER:DHT")
        return self.leer_linea()

    def leer_nivel_agua(self):
        self.enviar("LEER:NIVEL")
        return self.leer_linea()

    def leer_linea(self):
        if self.arduino and self.arduino.in_waiting:
            try:
                return self.arduino.readline().decode().strip()
            except:
                return None
        return None

    def cerrar(self):
        if self.arduino and self.arduino.is_open:
            self.arduino.close()
