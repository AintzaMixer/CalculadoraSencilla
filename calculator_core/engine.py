# calculator_core/engine.py

import math
import re

# --- Excepciones Personalizadas ---
class CalculatorError(Exception):
    """Clase base para errores en la calculadora."""
    pass

class DivisionByZeroError(CalculatorError):
    """Lanzada al intentar dividir por cero."""
    pass

class SyntaxError(CalculatorError):
    """Lanzada por expresiones mal formadas."""
    pass

class MathDomainError(CalculatorError):
    """Lanzada por operaciones matemáticas en dominios inválidos (ej. sqrt(-1))."""
    pass

class CalculatorEngine:
    """
    Motor de cálculo que parsea y evalúa expresiones matemáticas.
    Implementa el algoritmo Shunting-yard para convertir a notación polaca inversa (RPN)
    y luego evalúa la RPN.
    """
    def __init__(self):
        self.functions = {
            'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
            'sqrt': math.sqrt, 'ln': math.log, 'log': math.log10
        }
        self.constants = {'pi': math.pi, 'e': math.e}
        self.operators = {
            '+': {'precedence': 2, 'assoc': 'L', 'func': lambda a, b: a + b},
            '-': {'precedence': 2, 'assoc': 'L', 'func': lambda a, b: a - b},
            '*': {'precedence': 3, 'assoc': 'L', 'func': lambda a, b: a * b},
            '/': {'precedence': 3, 'assoc': 'L', 'func': lambda a, b: a / b},
            '^': {'precedence': 4, 'assoc': 'R', 'func': lambda a, b: a ** b},
            '%': {'precedence': 4, 'assoc': 'L', 'func': lambda a: a / 100}, # Unary
            '_': {'precedence': 5, 'assoc': 'R', 'func': lambda a: -a} # Unary minus
        }

    def _tokenize(self, expression: str) -> list:
        """
        Convierte la cadena de entrada en una lista de tokens usando expresiones regulares.
        [MEJORA] Más robusto que el parseo manual.
        """
        expression = expression.replace(" ", "").lower()
        for name, value in self.constants.items():
            expression = expression.replace(name, str(value))

        # Regex para encontrar: números (incl. flotantes), nombres de funciones, o cualquier operador/paréntesis
        token_regex = r"(\d*\.\d+|\d+|[a-z]+|[+\-*/^%()])"
        raw_tokens = re.findall(token_regex, expression)
        
        tokens = []
        for i, token in enumerate(raw_tokens):
            if token.replace('.', '', 1).isdigit():
                tokens.append(float(token))
            # Detectar menos unario: al inicio o después de un operador o paréntesis izquierdo
            elif token == '-' and (i == 0 or (isinstance(tokens[-1], str) and tokens[-1] in '(*^/+-')):
                tokens.append('_') # Token especial para menos unario
            elif token in self.operators or token in self.functions or token in '()':
                tokens.append(token)
            else:
                raise SyntaxError(f"Token desconocido: '{token}'")
                
        return tokens

    def _shunting_yard(self, tokens: list) -> list:
        """
        Convierte una lista de tokens de notación infija a notación polaca inversa (RPN)
        usando el algoritmo Shunting-yard.
        """
        output_queue = []
        operator_stack = []

        for token in tokens:
            if isinstance(token, (float, int)):
                output_queue.append(token)
            elif token in self.functions:
                operator_stack.append(token)
            elif token in self.operators:
                while (operator_stack and operator_stack[-1] in self.operators and
                       ((self.operators[operator_stack[-1]]['precedence'] > self.operators[token]['precedence']) or
                        (self.operators[operator_stack[-1]]['precedence'] == self.operators[token]['precedence'] and
                         self.operators[token]['assoc'] == 'L'))):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if not operator_stack or operator_stack.pop() != '(':
                    raise SyntaxError("Paréntesis desbalanceados")
            
        while operator_stack:
            op = operator_stack.pop()
            if op == '(':
                raise SyntaxError("Paréntesis desbalanceados")
            output_queue.append(op)

        return output_queue

    def _evaluate_rpn(self, rpn_queue: list) -> float:
        """Evalúa una cola de tokens en RPN."""
        stack = []
        for token in rpn_queue:
            if isinstance(token, (float, int)):
                stack.append(token)
            else:
                try:
                    if token in ('%', '_'): # Operadores unarios
                        operand = stack.pop()
                        result = self.operators[token]['func'](operand)
                        stack.append(result)
                    elif token in self.functions: # Funciones
                        operand = stack.pop()
                        result = self.functions[token](operand)
                        stack.append(result)
                    else: # Operadores binarios
                        op2 = stack.pop()
                        op1 = stack.pop()
                        if token == '/' and op2 == 0:
                            raise DivisionByZeroError("División por cero")
                        result = self.operators[token]['func'](op1, op2)
                        stack.append(result)
                except IndexError:
                    raise SyntaxError("Expresión inválida, faltan operandos")
                except ValueError:
                    raise MathDomainError("Error de dominio matemático (ej. sqrt(-1))")

        if len(stack) != 1:
            raise SyntaxError("La expresión es inválida")
        
        return stack[0]

    def calculate(self, expression: str) -> float:
        """
        Punto de entrada principal. Tokeniza, convierte a RPN y evalúa la expresión.
        """
        if not expression:
            return 0.0
        try:
            tokens = self._tokenize(expression)
            rpn_queue = self._shunting_yard(tokens)
            result = self._evaluate_rpn(rpn_queue)
            return 0.0 if result == -0.0 else result
        except CalculatorError:
            raise
        except Exception as e:
            raise SyntaxError(f"Error de sintaxis: {e}")