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

        self._expression = tk.StringVar()
        self._history = []
        self._memory = 0.0
        self._memory_indicator_visible = False
        self._is_result_on_display = False

        self._configure_styles()
        self._create_widgets()
        self._setup_button_commands()
        self._bind_keyboard()

    def _configure_styles(self):
        self.style = {
            'bg': '#2E2E2E', 'display_bg': '#1C1C1C', 'display_fg': '#FFFFFF',
            'btn_bg': '#4A4A4A', 'btn_fg': '#FFFFFF', 'op_btn_bg': '#FF9500',
            'func_btn_bg': '#3D3D3D', 'eq_btn_bg': '#FFB000' # Color diferente para '='
        }

    def _create_widgets(self):
        """
        [GUI MEJORADA] Crea y posiciona todos los widgets en una parrilla uniforme.
        """
        self.configure(bg=self.style['bg'])

        display_frame = tk.Frame(self, bg=self.style['bg'])
        display_frame.pack(pady=20, padx=10, fill='x')
        
        self.memory_indicator = tk.Label(display_frame, text="M", font=('Arial', 12),
                                         bg=self.style['bg'], fg=self.style['op_btn_bg'])

        display_entry = tk.Entry(display_frame, textvariable=self._expression, font=('Arial', 40),
                                 borderwidth=0, relief='flat', justify='right',
                                 bg=self.style['display_bg'], fg=self.style['display_fg'],
                                 readonlybackground=self.style['display_bg'])
        display_entry.configure(state='readonly')
        display_entry.pack(fill='x', ipady=10)

        button_frame = tk.Frame(self, bg=self.style['bg'])
        button_frame.pack(padx=10, pady=10, fill='both', expand=True)

        # Diseño de botones en una parrilla uniforme de 5 columnas
        buttons = [
            ('sin', 'cos', 'tan', 'CE', 'C'),
            ('sqrt', 'ln', 'log', '^', '%'),
            ('pi', 'e', '(', ')', '/'),
            ('7', '8', '9', '*', 'M+'),
            ('4', '5', '6', '-', 'M-'),
            ('1', '2', '3', '+', 'MR'),
            ('0', '+/-', '.', 'Hist', 'MC'),
            ('=',) # Fila especial para el botón '=' ancho
        ]

        for r, row_list in enumerate(buttons):
            button_frame.grid_rowconfigure(r, weight=1)
            for c, label in enumerate(row_list):
                if not label: continue
                button_frame.grid_columnconfigure(c, weight=1)
                
                color = self.style['btn_bg']
                if label == '=': color = self.style['eq_btn_bg']
                elif label in ['/', '*', '-', '+', '^', '%']: color = self.style['op_btn_bg']
                elif label not in '0123456789.': color = self.style['func_btn_bg']
                
                # Botón '=' ancho que ocupa toda la fila
                if label == '=':
                    columnspan = 5
                    btn = tk.Button(button_frame, text=label, font=('Arial', 20, 'bold'),
                                    bg=color, fg=self.style['btn_fg'], borderwidth=0,
                                    command=lambda l=label: self._on_button_press(l))
                    btn.grid(row=r, column=0, columnspan=columnspan, sticky='nsew', padx=5, pady=5)
                else:
                    btn = tk.Button(button_frame, text=label, font=('Arial', 16),
                                    bg=color, fg=self.style['btn_fg'], borderwidth=0,
                                    command=lambda l=label: self._on_button_press(l))
                    btn.grid(row=r, column=c, sticky='nsew', padx=5, pady=5)

    def _setup_button_commands(self):
        self.commands = {
            '=': self._calculate, 'C': self._clear_all, 'CE': self._clear_entry,
            'DEL': self._delete_last_char, '+/-': self._toggle_sign, 'Hist': self._show_history,
            'M+': self._memory_add, 'M-': self._memory_subtract, 'MR': self._memory_recall,
            'MC': self._memory_clear,
        }
        self.functions_with_parenthesis = {'sqrt', 'sin', 'cos', 'tan', 'ln', 'log'}
        # [CORRECCIÓN LÓGICA] Operadores que pueden seguir a un resultado
        self.continuing_operators = {'+', '-', '*', '/', '^', '%'}

    def _on_button_press(self, value: str):
        """[LÓGICA CORREGIDA] Manejador central para clics y continuación de cálculos."""
        current_text = self._expression.get()

        if self._is_result_on_display:
            # Si hay un resultado y se pulsa algo que no sea un operador o un comando, se limpia la pantalla
            if value not in self.commands and value not in self.continuing_operators:
                current_text = ""
            self._is_result_on_display = False

        if value in self.commands:
            self.commands[value]()
        elif value in self.functions_with_parenthesis:
            self._expression.set(current_text + value + '(')
        else:
            self._expression.set(current_text + value)

    def _calculate(self):
        expression = self._expression.get()
        if not expression: return
        try:
            result = self.engine.calculate(expression)
            result_str = f"{result:.8f}".rstrip('0').rstrip('.') if result != int(result) else str(int(result))
            self._expression.set(result_str)
            self._history.append(f"{expression} = {result_str}")
            self._is_result_on_display = True
        except CalculatorError as e:
            messagebox.showerror("Error de Cálculo", str(e))

    def _clear_all(self):
        self._expression.set("")
        self._is_result_on_display = False

    def _clear_entry(self):
        if self._is_result_on_display: self._clear_all(); return
        current_text = self._expression.get()
        last_op_index = -1
        for op in self.engine.operators.keys() | {'(', ')'}:
            last_op_index = max(last_op_index, current_text.rfind(op))
        self._expression.set(current_text[:last_op_index + 1] if last_op_index != -1 else "")

    def _delete_last_char(self):
        if not self._is_result_on_display:
            self._expression.set(self._expression.get()[:-1])

    def _toggle_sign(self):
        current_text = self._expression.get()
        if not current_text: return
        if self._is_result_on_display or all(c in '0123456789.-' for c in current_text):
            self._expression.set(str(float(current_text) * -1))
        else:
            self._expression.set(current_text + "(-")
            self._is_result_on_display = False
    
    def _update_memory_indicator(self):
        if self._memory != 0 and not self._memory_indicator_visible:
            self.memory_indicator.pack(side='left', padx=(5,0)); self._memory_indicator_visible = True
        elif self._memory == 0 and self._memory_indicator_visible:
            self.memory_indicator.pack_forget(); self._memory_indicator_visible = False

    def _memory_add(self):
        try:
            value = self.engine.calculate(self._expression.get())
            self._memory += value
            self._is_result_on_display = True
            self._update_memory_indicator()
        except CalculatorError as e:
            messagebox.showwarning("Memoria", f"No se pudo añadir a la memoria: {e}")

    def _memory_subtract(self):
        try:
            value = self.engine.calculate(self._expression.get())
            self._memory -= value
            self._is_result_on_display = True
            self._update_memory_indicator()
        except CalculatorError as e:
            messagebox.showwarning("Memoria", f"No se pudo restar de la memoria: {e}")

    def _memory_recall(self):
        self._expression.set(str(self._memory))
        self._is_result_on_display = True
    
    def _memory_clear(self):
        self._memory = 0.0; self._update_memory_indicator()

    def _show_history(self):
        history_window = tk.Toplevel(self); history_window.title("Historial")
        history_window.geometry("300x400"); history_window.configure(bg=self.style['bg'])
        listbox = tk.Listbox(history_window, bg=self.style['display_bg'], fg=self.style['display_fg'],
                             font=('Arial', 14), borderwidth=0, selectbackground=self.style['op_btn_bg'])
        for item in reversed(self._history): listbox.insert(tk.END, item)
        listbox.pack(fill='both', expand=True, padx=10, pady=10)
        
        def reuse_history(event):
            selection = listbox.get(listbox.curselection())
            expression, _ = selection.split(' = ')
            self._expression.set(expression)
            self._is_result_on_display = False
            history_window.destroy()
        listbox.bind("<<ListboxSelect>>", reuse_history)

    def _bind_keyboard(self):
        self.focus_set()
        self.bind('<KeyPress>', self._on_key_press)
        
    def _on_key_press(self, event: tk.Event):
        key = event.keysym
        char = event.char
        
        if key == 'Return' or key == 'KP_Enter': self._on_button_press('=')
        elif key == 'BackSpace': self._on_button_press('DEL')
        elif key == 'Escape': self._on_button_press('C')
        elif key == 'Delete': self._on_button_press('CE')
        elif char in '0123456789.+-*/()^%': self._on_button_press(char)
        elif key.lower() in ('p',): self._on_button_press('pi')
        elif key.lower() in ('e',): self._on_button_press('e')