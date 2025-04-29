#더하기
import sys

def plus(a: int, b: int):
    print(a + b)

def main():
    args = sys.argv[1:]
    a, b = int(args[0]), int(args[1])
    plus(a, b)

