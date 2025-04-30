# test_fibo.py for pytest


from fibo import fib2, fib
from io import StringIO
import sys

def test_fib2_basic():
    assert fib2(0) == []
    assert fib2(1) == [0]
    assert fib2(2) == [0, 1, 1]
    assert fib2(10) == [0, 1, 1, 2, 3, 5, 8]

def test_fib_print_output(monkeypatch):
    captured = StringIO()
    monkeypatch.setattr(sys, "stdout", captured)
    fib(10)
    assert captured.getvalue().strip() == "0 1 1 2 3 5 8"
