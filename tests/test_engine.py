# tests/test_engine.py

import unittest
import math
from calculator_core.engine import CalculatorEngine, SyntaxError, DivisionByZeroError, MathDomainError

class TestCalculatorEngine(unittest.TestCase):
    
    def setUp(self):
        """Crea una instancia del motor para cada prueba."""
        self.engine = CalculatorEngine()
        self.delta = 1e-9 # Tolerancia para comparaciones de flotantes

    def test_basic_operations(self):
        self.assertAlmostEqual(self.engine.calculate("5 + 3"), 8.0, delta=self.delta)
        self.assertAlmostEqual(self.engine.calculate("10 - 4"), 6.0, delta=self.delta)
        self.assertAlmostEqual(self.engine.calculate("6 * 7"), 42.0, delta=self.delta)
        self.assertAlmostEqual(self.engine.calculate("10 / 2"), 5.0, delta=self.delta)

    def test_precedence(self):
        self.assertAlmostEqual(self.engine.calculate("2 + 3 * 4"), 14.0, delta=self.delta)
        self.assertAlmostEqual(self.engine.calculate("10 / 2 * 5"), 25.0, delta=self.delta)
    
    def test_parentheses(self):
        self.assertAlmostEqual(self.engine.calculate("(2 + 3) * 4"), 20.0, delta=self.delta)
        self.assertAlmostEqual(self.engine.calculate("10 / (2 * 5)"), 1.0, delta=self.delta)
        
    def test_floats_and_negatives(self):
        self.assertAlmostEqual(self.engine.calculate("1.5 + 2.5"), 4.0, delta=self.delta)
        self.assertAlmostEqual(self.engine.calculate("-5 + 3"), -2.0, delta=self.delta)
        self.assertAlmostEqual(self.engine.calculate("5 * -2"), -10.0, delta=self.delta)
        self.assertAlmostEqual(self.engine.calculate("(-2 + 1) * 5"), -5.0, delta=self.delta)

    def test_advanced_functions(self):
        self.assertAlmostEqual(self.engine.calculate("2^3"), 8.0, delta=self.delta)
        self.assertAlmostEqual(self.engine.calculate("3^2^2"), 81.0, delta=self.delta) # Asociatividad a la derecha
        self.assertAlmostEqual(self.engine.calculate("sqrt(16)"), 4.0, delta=self.delta)
        self.assertAlmostEqual(self.engine.calculate("50%"), 0.5, delta=self.delta)
        self.assertAlmostEqual(self.engine.calculate("sin(0)"), 0.0, delta=self.delta)
        self.assertAlmostEqual(self.engine.calculate("cos(pi)"), -1.0, delta=self.delta)
        self.assertAlmostEqual(self.engine.calculate("ln(e)"), 1.0, delta=self.delta)

    def test_error_handling(self):
        with self.assertRaises(DivisionByZeroError):
            self.engine.calculate("1 / 0")
        with self.assertRaises(SyntaxError):
            self.engine.calculate("5 * + 3")
        with self.assertRaises(SyntaxError):
            self.engine.calculate("(5 + 2")
        with self.assertRaises(MathDomainError):
            self.engine.calculate("sqrt(-1)")
        with self.assertRaises(SyntaxError):
            self.engine.calculate("logg(10)")

if __name__ == '__main__':
    unittest.main()