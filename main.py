# main.py

from ui.gui import CalculatorApp
from calculator_core.engine import CalculatorEngine

def main():
    """
    Punto de entrada principal de la aplicación.
    Inicializa el motor de cálculo y la interfaz de usuario.
    """
    # 1. Crear una instancia del motor de cálculo
    engine = CalculatorEngine()
    
    # 2. Crear una instancia de la aplicación GUI, pasándole el motor
    app = CalculatorApp(engine)
    
    # 3. Iniciar el bucle principal de la aplicación
    app.mainloop()

if __name__ == "__main__":
    main()