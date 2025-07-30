# ui/gui.py

import tkinter as tk
from tkinter import messagebox
from calculator_core.engine import CalculatorEngine, CalculatorError

class CalculatorApp(tk.Tk):
    """
    Clase principal para la aplicación de la calculadora con GUI (tkinter).
    """
    def __init__(self, engine: CalculatorEngine):
        super().__init__()
        self.engine = engine
        self.title("Calculadora Profesional")
        self.geometry("400x600")
        self.resizable(False, False)

        # --- Estado de la Calculadora ---
        self._expression = tk.StringVar()
        self._history = []
        self._memory = 0.0
        self._memory_indicator_visible = False
        self._is_result_on_display = False

        self._configure_styles()
        self._create_widgets()

    def _configure_styles(self):
        self.style = {
            'bg': '#2E2E2E',
            'display_bg': '#1C1C1C',
            'display_fg': '#FFFFFF',
            'btn_bg': '#4A4A4A',
            'btn_fg': '#FFFFFF',
            'op_btn_bg': '#FF9500',
            'func_btn_bg': '#3D3D3D'
        }

    def _create_widgets(self):
        """Crea y posiciona todos los widgets en la ventana principal."""
        self.configure(bg=self.style['bg'])

        # --- Pantalla de Visualización ---
        display_frame = tk.Frame(self, bg=self.style['bg'])
        display_frame.pack(pady=20, padx=10, fill='x')
        
        # Indicador de Memoria
        self.memory_indicator = tk.Label(display_frame, text="M", font=('Arial', 12),
                                         bg=self.style['bg'], fg=self.style['op_btn_bg'])

        display_entry = tk.Entry(display_frame, textvariable=self._expression, font=('Arial', 40),
                                 borderwidth=0, relief='flat', justify='right',
                                 bg=self.style['display_bg'], fg=self.style['display_fg'],
                                 readonlybackground=self.style['display_bg'])
        display_entry.configure(state='readonly')
        display_entry.pack(fill='x', ipady=10)

        # --- Botones ---
        button_frame = tk.Frame(self, bg=self.style['bg'])
        button_frame.pack(padx=10, pady=10, fill='both', expand=True)

        buttons = [
            ('sin', 'cos', 'tan', 'CE', 'C'),
            ('sqrt', 'ln', 'log', '^', '/'),
            ('pi', 'e', '(', ')', '*'),
            ('7', '8', '9', '-', '%'),
            ('4', '5', '6', '+', 'M+'),
            ('1', '2', '3', '=', 'M-'),
            ('+/-', '0', '.', 'Hist', 'MR'),
            ('DEL', 'MC', '', '', '') # Algunos vacíos para layout
        ]

        for r, row_list in enumerate(buttons):
            button_frame.grid_rowconfigure(r, weight=1)
            for c, label in enumerate(row_list):
                if not label: continue
                button_frame.grid_columnconfigure(c, weight=1)
                
                # Definir color del botón
                color = self.style['btn_bg']
                if label in ['/', '*', '-', '+', '=']:
                    color = self.style['op_btn_bg']
                elif label not in '0123456789.':
                    color = self.style['func_btn_bg']
                
                # El botón de igual ocupa 2 filas
                rowspan = 2 if label == '=' else 1
                if label == '=':
                    button_frame.grid_rowconfigure(r+1, weight=1)

                btn = tk.Button(button_frame, text=label, font=('Arial', 16),
                                bg=color, fg=self.style['btn_fg'], borderwidth=0,
                                command=lambda l=label: self._on_button_press(l))
                btn.grid(row=r, column=c, rowspan=rowspan, sticky='nsew', padx=5, pady=5)

    def _on_button_press(self, value: str):
        """Manejador central para todos los clics de botones."""
        current_text = self._expression.get()

        # Limpiar la pantalla si hay un resultado y se presiona un número o función
        if self._is_result_on_display and value not in ['+', '-', '*', '/', '^', '%', '=', 'Hist', 'M+', 'M-', 'MR', 'MC']:
            current_text = ""
            self._is_result_on_display = False
        
        # Lógica de los botones
        if value == '=':
            self._calculate()
        elif value == 'C':
            self._clear_all()
        elif value == 'CE':
            self._clear_entry()
        elif value == 'DEL':
            if not self._is_result_on_display:
                self._expression.set(current_text[:-1])
        elif value == '+/-':
            self._toggle_sign()
        elif value == 'Hist':
            self._show_history()
        # Funciones de memoria
        elif value == 'M+': self._memory_add()
        elif value == 'M-': self._memory_subtract()
        elif value == 'MR': self._memory_recall()
        elif value == 'MC': self._memory_clear()
        # Funciones que necesitan paréntesis
        elif value in ['sqrt', 'sin', 'cos', 'tan', 'ln', 'log']:
            self._expression.set(current_text + value + '(')
            self._is_result_on_display = False
        else:
            self._expression.set(current_text + value)
            self._is_result_on_display = False

    def _calculate(self):
        """Calcula la expresión y actualiza la pantalla."""
        expression = self._expression.get()
        if not expression:
            return
        try:
            result = self.engine.calculate(expression)
            # Formatear resultado (entero si no tiene decimales)
            if result == int(result):
                result_str = str(int(result))
            else:
                result_str = f"{result:.8f}".rstrip('0').rstrip('.')

            self._expression.set(result_str)
            self._history.append(f"{expression} = {result_str}")
            self._is_result_on_display = True
        except CalculatorError as e:
            messagebox.showerror("Error de Cálculo", str(e))

    def _clear_all(self):
        self._expression.set("")
        self._is_result_on_display = False

    def _clear_entry(self):
        """Borra la última entrada numérica."""
        if self._is_result_on_display:
            self._clear_all()
            return
        current_text = self._expression.get()
        # Encuentra el último operador para borrar el número que le sigue
        last_op_index = -1
        for op in self.engine.operators.keys() | {'(', ')'}:
            last_op_index = max(last_op_index, current_text.rfind(op))
        if last_op_index != -1:
            self._expression.set(current_text[:last_op_index + 1])
        else:
            self._expression.set("")

    def _toggle_sign(self):
        """Cambia el signo del número actual o del resultado."""
        current_text = self._expression.get()
        if not current_text: return
        
        if self._is_result_on_display or current_text.find('(') == -1: # Si es un solo número
             if current_text.startswith('-'):
                 self._expression.set(current_text[1:])
             else:
                 self._expression.set('-' + current_text)
        else: # Intenta ser más inteligente con expresiones
            # Esta parte puede ser compleja, una implementación simple es añadir '(-'
            self._expression.set(current_text + "(-")
            self._is_result_on_display = False
    
    # --- Funciones de Historial y Memoria ---
    def _update_memory_indicator(self):
        if self._memory != 0 and not self._memory_indicator_visible:
            self.memory_indicator.pack(side='left', padx=(5,0))
            self._memory_indicator_visible = True
        elif self._memory == 0 and self._memory_indicator_visible:
            self.memory_indicator.pack_forget()
            self._memory_indicator_visible = False

    def _memory_add(self):
        try:
            value = float(self._expression.get())
            self._memory += value
            self._is_result_on_display = True
            self._update_memory_indicator()
        except (ValueError, CalculatorError):
            messagebox.showwarning("Memoria", "Valor en pantalla no es un número válido.")
    
    def _memory_subtract(self):
        try:
            value = float(self._expression.get())
            self._memory -= value
            self._is_result_on_display = True
            self._update_memory_indicator()
        except (ValueError, CalculatorError):
            messagebox.showwarning("Memoria", "Valor en pantalla no es un número válido.")

    def _memory_recall(self):
        self._expression.set(str(self._memory))
        self._is_result_on_display = True
    
    def _memory_clear(self):
        self._memory = 0.0
        self._update_memory_indicator()

    def _show_history(self):
        history_window = tk.Toplevel(self)
        history_window.title("Historial")
        history_window.geometry("300x400")
        history_window.configure(bg=self.style['bg'])
        
        listbox = tk.Listbox(history_window, bg=self.style['display_bg'], 
                             fg=self.style['display_fg'], font=('Arial', 14),
                             borderwidth=0, selectbackground=self.style['op_btn_bg'])
        for item in reversed(self._history):
            listbox.insert(tk.END, item)
        listbox.pack(fill='both', expand=True, padx=10, pady=10)

        def reuse_history(event):
            selection = listbox.get(listbox.curselection())
            expression, result = selection.split(' = ')
            # Opción 1: Reusar la expresión
            self._expression.set(expression)
            # Opción 2: Reusar el resultado (descomentar si se prefiere)
            # self._expression.set(result)
            self._is_result_on_display = False
            history_window.destroy()

        listbox.bind("<<ListboxSelect>>", reuse_history)