import serial
import time

class SerialManager:
    def __init__(self, puerto="COM5", baudrate=9600, pines=None):
        self.pines = pines or {}
        try:
            self.arduino = serial.Serial(puerto, baudrate, timeout=1)
            time.sleep(2)
            print(f"[SerialManager] Conectado a {puerto}")
            time.sleep(1)
            self.enviar("DESACTIVAR:LEDS")
            self.enviar("DESACTIVAR:BOMBA")
            self.enviar("DESACTIVAR:VENTILADOR")
            self.mover_servo(0)
        except serial.SerialException as e:
            self.arduino = None
            print(f"[SerialManager] Error al abrir el puerto serial: {e}")

    def enviar(self, comando):
        if self.arduino and self.arduino.is_open:
            try:
                comando_str = comando.strip() + "\n"
                self.arduino.write(comando_str.encode())
                print(f"[SerialManager] Enviado: {comando_str.strip()}")
            except serial.SerialException as e:
                print(f"[SerialManager] Error al enviar comando: {e}")
        else:
            print("[SerialManager] Arduino no conectado o puerto cerrado.")

    write = enviar

    def activar(self, componente):
        self.enviar(f"ACTIVAR:{componente.upper()}")

    def desactivar(self, componente):
        self.enviar(f"DESACTIVAR:{componente.upper()}")

    def mover_servo(self, angulo):
        self.enviar(f"SERVO:{angulo}")

    def leer_dht(self):
        self.enviar("LEER:DHT")
        return self.leer_linea(timeout=4)

    def leer_nivel_agua(self):
        self.enviar("CONSULTAR:NIVEL_AGUA")
        return self.leer_linea(timeout=2)

    def leer_linea(self, timeout=3):
        if self.arduino and self.arduino.is_open:
            try:
                print("[SerialManager] Esperando respuesta del Arduino...")
                inicio = time.time()
                while time.time() - inicio < timeout:
                    if self.arduino.in_waiting:
                        linea = self.arduino.readline().decode(errors="ignore").strip()
                        if linea:
                            print(f"[SerialManager] Recibido: {linea}")
                            return linea
                print("[SerialManager] No se recibió ninguna línea en el tiempo esperado.")
            except serial.SerialException as e:
                print(f"[SerialManager] Error al leer línea: {e}")
        return None

    def flush(self):
        if self.arduino and self.arduino.is_open:
            self.arduino.reset_input_buffer()
            print("[SerialManager] Buffer de entrada limpiado.")

    def cerrar(self):
        if self.arduino and self.arduino.is_open:
            self.arduino.close()
            print("[SerialManager] Puerto cerrado correctamente.")
