# ui/gui.py

import os
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent

from calculator_core.engine import CalculatorEngine, CalculatorError

# Determina la ruta al archivo .ui de forma robusta
# Esto es crucial para que PyInstaller encuentre el archivo
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
    
class CalculatorApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Carga el diseño desde el archivo .ui usando la ruta correcta
        uic.loadUi(resource_path('ui/main_window.ui'), self)
        
        # Carga la hoja de estilos
        try:
            with open(resource_path('ui/style.qss'), 'r') as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print("Advertencia: No se encontró el archivo style.qss.")

        # Inicializa el motor de cálculo
        self.engine = CalculatorEngine()
        self._is_result_on_display = False

        # Conecta los widgets y las señales
        self.display = self.findChild(QtWidgets.QLineEdit, 'display_output')
        self._connect_signals()
        
        self.show()

    def _connect_signals(self):
        """Conecta las señales de clic de los botones a los métodos correspondientes."""
        # Itera sobre todos los botones en la ventana
        for button in self.findChildren(QtWidgets.QPushButton):
            object_name = button.objectName()
            
            # Conexiones para botones especiales
            if object_name == 'btn_equals':
                button.clicked.connect(self._calculate_result)
            elif object_name == 'btn_c':
                button.clicked.connect(self._clear_all)
            elif object_name == 'btn_ce':
                button.clicked.connect(self._clear_entry)
            elif object_name == 'btn_del':
                button.clicked.connect(self._delete_last_char)
            elif object_name == 'btn_pm':
                button.clicked.connect(self._toggle_sign)
            # Para todos los demás botones (números, operadores, etc.)
            else:
                button.clicked.connect(self._append_to_display)
    
    def _append_to_display(self):
        """Añade el texto del botón presionado a la pantalla."""
        if self._is_result_on_display:
            self.display.setText("")
            self._is_result_on_display = False
        
        button = self.sender()
        current_text = self.display.text()
        button_text = button.text()

        if current_text == '0' and button_text != '.':
            self.display.setText(button_text)
        else:
            self.display.setText(current_text + button_text)
            
    def _calculate_result(self):
        """Calcula la expresión en la pantalla y muestra el resultado."""
        try:
            expression = self.display.text()
            result = self.engine.calculate(expression)
            
            # Formatea el resultado para no mostrar ".0" en enteros
            if result == int(result):
                result_str = str(int(result))
            else:
                result_str = f"{result:.8f}".rstrip('0').rstrip('.')
            
            self.display.setText(result_str)
            self._is_result_on_display = True
        except CalculatorError as e:
            self._show_error_message("Error de Cálculo", str(e))
        except Exception:
            self._show_error_message("Error Inesperado", "La expresión no es válida.")

    def _clear_all(self):
        self.display.setText("0")
        self._is_result_on_display = False

    def _clear_entry(self):
        if self._is_result_on_display:
            self._clear_all()
        else:
            # Esta es una versión simplificada de 'CE'.
            # Para una implementación completa, se necesitaría más lógica de parsing.
            self.display.setText("0")

    def _delete_last_char(self):
        if not self._is_result_on_display:
            current_text = self.display.text()
            new_text = current_text[:-1]
            if not new_text:
                self.display.setText("0")
            else:
                self.display.setText(new_text)

    def _toggle_sign(self):
        if not self._is_result_on_display:
            return # Implementación más compleja requerida para expresiones
            
        current_text = self.display.text()
        if current_text.startswith('-'):
            self.display.setText(current_text[1:])
        else:
            self.display.setText('-' + current_text)

    def _show_error_message(self, title, message):
        """Muestra un cuadro de diálogo de error."""
        msg_box = QtWidgets.QMessageBox(self)
        msg_box.setIcon(QtWidgets.QMessageBox.Icon.Critical)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec()

    def keyPressEvent(self, event: QKeyEvent):
        """Maneja las pulsaciones de teclado."""
        key = event.key()
        text = event.text()

        if Qt.Key.Key_0 <= key <= Qt.Key.Key_9 or text in '+-*/.()^':
            self._append_from_key(text)
        elif key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self._calculate_result()
        elif key == Qt.Key.Key_Backspace:
            self._delete_last_char()
        elif key == Qt.Key.Key_Escape:
            self._clear_all()
        elif key == Qt.Key.Key_Delete:
             self._clear_entry()
             
    def _append_from_key(self, text: str):
        if self._is_result_on_display:
            self.display.setText("")
            self._is_result_on_display = False
        
        current_text = self.display.text()
        if current_text == '0' and text != '.':
            self.display.setText(text)
        else:
            self.display.setText(current_text + text)