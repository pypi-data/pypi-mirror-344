# fibo/cli.py

import argparse
from .fibo import fib, fib2

def main():
    parser = argparse.ArgumentParser(description="Generate Fibonacci numbers up to n.")
    parser.add_argument("n", type=int, help="Upper limit for Fibonacci series")
    parser.add_argument("--print", action="store_true", help="Print Fibonacci numbers one by one (uses fib)")
    
    args = parser.parse_args()
    
    if args.print:
        fib(args.n)
    else:
        print(fib2(args.n))


