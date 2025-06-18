import serial
import time

class SerialManager:
    def __init__(self, puerto="COM5", baudrate=9600, pines=None):
        self.pines = pines or {}
        try:
            self.arduino = serial.Serial(puerto, baudrate, timeout=1)
            time.sleep(2)  # Esperar que el Arduino se reinicie
            print(f"[SerialManager] Conectado a {puerto}")

            # 🛑 Apagar todo por defecto al iniciar
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

    # ✅ Alias para usar write() directamente
    write = enviar

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
        if self.arduino and self.arduino.is_open:
            try:
                time.sleep(2)  # Tiempo suficiente para que Arduino responda
                linea = self.arduino.readline().decode(errors="ignore").strip()
                if linea:
                    print(f"[SerialManager] Recibido: {linea}")
                    return linea
                else:
                    print("[SerialManager] No se recibió ninguna línea.")
            except serial.SerialException as e:
                print(f"[SerialManager] Error al leer línea: {e}")
        return None

    def cerrar(self):
        if self.arduino and self.arduino.is_open:
            self.arduino.close()
            print("[SerialManager] Puerto cerrado correctamente.")
