"""Tests for calculator module."""

import unittest
from src import calculator
from src.exceptions import CalculationError


class TestCalculator(unittest.TestCase):
    def test_add(self):
        self.assertEqual(calculator.add(5, 7), 12)
        self.assertEqual(calculator.calculate("add", 10, -3), 7)

    def test_subtract(self):
        self.assertEqual(calculator.subtract(10, 4), 6)
        self.assertEqual(calculator.calculate("subtract", 5, 12), -7)

    def test_multiply(self):
        self.assertEqual(calculator.multiply(6, 7), 42)
        self.assertEqual(calculator.multiply(5, 0), 0)
        self.assertEqual(calculator.calculate("multiply", 3.5, 2), 7.0)

    def test_divide(self):
        self.assertEqual(calculator.divide(20, 4), 5.0)
        self.assertEqual(calculator.calculate("divide", 9, 2), 4.5)

    def test_divide_by_zero(self):
        with self.assertRaises(CalculationError):
            calculator.divide(10, 0)
        with self.assertRaises(CalculationError):
            calculator.calculate("divide", 10, 0)

    def test_power(self):
        self.assertEqual(calculator.power(2, 3), 8)
        self.assertEqual(calculator.calculate("power", 5, 2), 25)

    def test_square_root(self):
        self.assertEqual(calculator.square_root(16), 4.0)
        self.assertEqual(calculator.calculate("sqrt", 25), 5.0)

    def test_square_root_negative(self):
        with self.assertRaises(CalculationError):
            calculator.square_root(-9)
        with self.assertRaises(CalculationError):
            calculator.calculate("sqrt", -4)

    def test_invalid_operation(self):
        with self.assertRaises(CalculationError):
            calculator.calculate("modulo", 10, 3)

    def test_invalid_operand_count(self):
        with self.assertRaises(CalculationError):
            calculator.calculate("add", 10)
        with self.assertRaises(CalculationError):
            calculator.calculate("sqrt", 16, 25)


if __name__ == "__main__":
    unittest.main()
