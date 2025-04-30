# test_fibo.py

import unittest
from fibo import fib2, fib
from io import StringIO
import sys

class TestFiboFunctions(unittest.TestCase):
    
    def test_fib2_basic(self):
        self.assertEqual(fib2(0), [])
        self.assertEqual(fib2(1), [0])
        self.assertEqual(fib2(2), [0, 1, 1])
        self.assertEqual(fib2(10), [0, 1, 1, 2, 3, 5, 8])
    
    def test_fib_print_output(self):
        captured = StringIO()
        sys.stdout = captured  # redirect stdout
        fib(10)
        sys.stdout = sys.__stdout__  # restore stdout
        self.assertEqual(captured.getvalue().strip(), "0 1 1 2 3 5 8")

if __name__ == "__main__":
    unittest.main()
