lookup_table = [0]*200
def factorial(number):
    if number <= 1:
        return 1
    return number * factorial(number-1)

def fibonacci(number):
    if number == 1:
        return 1
    if number == 2:
        return 1
    return fibonacci(number-1) + fibonacci(number-2)

def fib_with_cache(number):
    if number == 1:
        return 1
    if number == 2:
        return 1
    if lookup_table[number] != 0:
        return lookup_table[number]
    result = fib_with_cache(number-1) + fib_with_cache(number-2)
    lookup_table[number] = result
    return result
def main():
    number = int(input("Enter a number: "))
    print(f"Factorial of {number} is {factorial(number)}")
    print(f"fibonacci of {number} is {fib_with_cache(number)}")

if __name__ == '__main__':
    main()
