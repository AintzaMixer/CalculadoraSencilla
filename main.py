# main.py

import sys
from PyQt6 import QtWidgets
from ui.gui import CalculatorApp

def main():
    """
    Punto de entrada principal de la aplicación.
    Inicializa y ejecuta la aplicación PyQt6.
    """
    app = QtWidgets.QApplication(sys.argv)
    window = CalculatorApp()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()