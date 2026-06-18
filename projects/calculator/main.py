import sys

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b

def main():
    print("Simple Calculator")
    print("Add (2 + 3):", add(2, 3))
    print("Subtract (5 - 2):", subtract(5, 2))

if __name__ == "__main__":
    main()
