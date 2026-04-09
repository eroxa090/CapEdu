def subtract_numbers(a, b):
    return a - b 
result = subtract_numbers(10, 4)
print("Разность чисел:", result)


def check_age():
    age = int(input("Введите ваш возраст: "))
    if age >= 18:
        print("Вы совершеннолетний")
    else:
        print("Вы несовершеннолетний")
check_age()