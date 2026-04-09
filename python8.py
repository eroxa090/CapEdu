import random
number = random.randint(1, 100)

guess = int(input("Угадайте число от 1 до 100: "))

while guess != number:
    if guess < number:
        print("Загаданное число больше")
    else:
        print("Загаданное число меньше")
    guess = int(input("Попробуйте снова: "))

print("Поздравляем, вы угадали!")




n = int(input("Введите высоту пирамиды: "))

for i in range(1, n + 1):      
    for j in range(1, i + 1): 
        print(j, end=" ")
    print()