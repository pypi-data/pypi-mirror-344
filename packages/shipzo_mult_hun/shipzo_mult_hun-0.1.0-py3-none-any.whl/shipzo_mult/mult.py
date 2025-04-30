#곱셈
import sys

def mult(a: int, b: int):
    print(a * b)

def main():
    args = sys.argv[1:]
    a, b = int(args[0]), int(args[1])
    mult(a, b)
