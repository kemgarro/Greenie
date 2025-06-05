from src.ui.login import LoginUI
from src.hardware.serial_manager import SerialManager



if __name__ == "__main__":
    app = LoginUI()
    app.mostrar()
    serial_manager = SerialManager()