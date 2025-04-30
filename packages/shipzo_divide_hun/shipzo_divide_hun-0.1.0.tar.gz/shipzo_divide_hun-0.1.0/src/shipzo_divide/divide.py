#나눗셈
import sys

def divide(a: int, b: int):
    result = a / b
    print(f"{result:.3f}")  # 소수점 3자리까지 포맷팅

def main():
    args = sys.argv[1:]
    a, b = int(args[0]), int(args[1])
    divide(a, b)
