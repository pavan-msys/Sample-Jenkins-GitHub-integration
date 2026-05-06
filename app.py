"""
Simple calculator module for testing Jenkins-GitHub integration
"""

def add(a, b):
    """Add two numbers"""
    return a + b

def subtract(a, b):
    """Subtract b from a"""
    return a - b

def multiply(a, b):
    """Multiply two numbers"""
    return a * b

def divide(a, b):
    """Divide a by b"""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def greet(name):
    """Return a greeting message"""
    return f"Hello, {name}!"

if __name__ == "__main__":
    print("Testing Jenkins-GitHub integration")
    print(greet("Jenkins"))
    print(f"2 + 3 = {add(2, 3)}")
    print(f"5 * 4 = {multiply(5, 4)}")
