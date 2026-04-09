def get_even_numbers (numbers):
    even_numbers = []
    for num in numbers:
        if num%2==0:
            even_numbers.append(num)
    return even_numbers
print(get_even_numbers([1,2,3,4,5]))

def fibonacci(n):
    if n <= 0:
        return 0
    elif n ==1:
        return 1
    else:
        return fibonacci (n-1)+fibonacci(n-2)
print(fibonacci(10))