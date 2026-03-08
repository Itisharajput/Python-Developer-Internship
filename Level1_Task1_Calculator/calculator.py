# ============================================================
#   SIMPLE CALCULATOR — Level 1, Task 1 (Basic)
#   Operations : Addition, Subtraction, Multiplication, Division
# ============================================================

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "Error: Division by zero is not allowed!"
    return a / b

def calculator():
    print("=" * 40)
    print("      SIMPLE CALCULATOR")
    print("=" * 40)

    while True:
        print("\nSelect Operation:")
        print("  1. Addition       (+)")
        print("  2. Subtraction    (-)")
        print("  3. Multiplication (*)")
        print("  4. Division       (/)")
        print("  5. Exit")

        choice = input("\nEnter choice (1/2/3/4/5): ").strip()

        if choice == "5":
            print("\nThank you for using Simple Calculator! Goodbye!")
            break

        if choice not in ["1", "2", "3", "4"]:
            print("Invalid choice! Please enter 1, 2, 3, 4, or 5.")
            continue

        try:
            num1 = float(input("Enter first number : "))
            num2 = float(input("Enter second number: "))
        except ValueError:
            print("Invalid input! Please enter numbers only.")
            continue

        if choice == "1":
            result = add(num1, num2)
            op = "+"
        elif choice == "2":
            result = subtract(num1, num2)
            op = "-"
        elif choice == "3":
            result = multiply(num1, num2)
            op = "*"
        elif choice == "4":
            result = divide(num1, num2)
            op = "/"

        print(f"\nResult: {num1} {op} {num2} = {result}")
        print("-" * 40)

if name == "main":
    calculator()

