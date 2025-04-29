import sys

def plus(a, b):
    return a + b

def main():
    args = sys.argv[1:]
    a = int(args[0])
    b = int(args[1])
    print(plus(a, b))
